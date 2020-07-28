from collections import deque
from random import choice

import gmsh 
import numpy as np
from time import time

from pulse.preprocessing.entity import Entity
from pulse.preprocessing.node import Node, DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.structural_element import StructuralElement, NODES_PER_ELEMENT
from pulse.preprocessing.acoustic_element import AcousticElement, NODES_PER_ELEMENT
from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer, error

class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.nodes = {}
        self.structural_elements = {}
        self.acoustic_elements = {}
        self.neighbours = {}
        self.line_to_elements = {}
        self.entities = []
        self.connectivity_matrix = []
        self.nodal_coordinates_matrix = []
        self.nodes_with_nodal_loads = []
        self.nodes_with_prescribed_dofs = []
        self.nodes_with_constrained_dofs = []
        self.nodes_with_masses = []
        self.nodes_connected_to_springs = []
        self.nodes_connected_to_dampers = []
        self.nodes_with_acoustic_pressure = []
        self.nodes_with_volume_velocity = []
        self.nodes_with_specific_impedance = []
        self.radius = {}
        self.element_type = "pipe_1" # defined as default
        self.all_lines = []
        self.flag_fluid_mass_effect = False

    def generate(self, path, element_size):
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size)
        self._create_entities()
        self._map_lines_to_elements()
        self._finalize_gmsh()
        self._load_neighbours()
        self._order_global_indexes()
    
    def neighbour_elements_diameter(self):
        neighbour_diameters = dict()

        for index, element in self.structural_elements.items():
            first = element.first_node.external_index
            last = element.last_node.external_index
            neighbour_diameters.setdefault(first, [])
            neighbour_diameters.setdefault(last, [])

            external = element.cross_section.external_diameter
            internal = element.cross_section.internal_diameter

            neighbour_diameters[first].append((index, external, internal))
            neighbour_diameters[last].append((index, external, internal))

        return neighbour_diameters

    def neighbor_elements_diameter_global(self):
        neighbor_diameters = dict()

        for index, element in self.acoustic_elements.items():
            first = element.first_node.global_index
            last = element.last_node.global_index
            neighbor_diameters.setdefault(first, [])
            neighbor_diameters.setdefault(last, [])

            external = element.cross_section.external_diameter
            internal = element.cross_section.internal_diameter

            neighbor_diameters[first].append((index, external, internal))
            neighbor_diameters[last].append((index, external, internal))

        return neighbor_diameters    
    
    def _initialize_gmsh(self, path):
        gmsh.initialize('', False)
        gmsh.open(path)

    def _set_gmsh_options(self, element_size):
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Geometry.Tolerance', 1e-06)

    def _create_entities(self):

        gmsh.model.mesh.generate(3)

        for dim, tag in gmsh.model.getEntities(1):
            newEntity = Entity(tag)

            #Element
            _, node_indexes, connectivity = gmsh.model.mesh.getElements(dim, tag) 
            node_indexes = node_indexes[0]
            connectivity = split_sequence(connectivity[0], 2)

            for index, (start, end) in zip(node_indexes, connectivity):
                edges = index, start, end
                newEntity.insertEdge(edges)

            #Nodes
            element_indexes, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            coordinates = split_sequence(coordinates, 3)

            for index, (x, y, z) in zip(element_indexes, coordinates):
                node = index, mm_to_m(x), mm_to_m(y), mm_to_m(z)
                newEntity.insertNode(node)
                
            self.all_lines.append(tag)
            self.entities.append(newEntity)

        gmsh.model.mesh.removeDuplicateNodes()

        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivity = gmsh.model.mesh.getElements()

        self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
        self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))
        
        self._create_nodes(node_indexes, coords, self.map_nodes)
        self._create_structural_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)
        self._create_acoustic_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements) 
        
    def _create_nodes(self, indexes, coords, map_nodes):
        for i, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[map_nodes[i]] = Node(x, y, z, external_index=int(map_nodes[i]))

    def _create_structural_elements(self, indexes, connectivities, map_nodes, map_elements):
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.structural_elements[map_elements[i]] = StructuralElement(first_node, last_node)

    def _create_acoustic_elements(self, indexes, connectivities, map_nodes, map_elements):
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.acoustic_elements[map_elements[i]] = AcousticElement(first_node, last_node)

    def _map_lines_to_elements(self, mesh_loaded=False):
        if mesh_loaded:
            self.line_to_elements[1] = list(self.structural_elements.keys())
        else:    
            mapping = self.map_elements
            for dim, tag in gmsh.model.getEntities(1):
                elements_of_entity = gmsh.model.mesh.getElements(dim, tag)[1][0]
                self.line_to_elements[tag] = np.array([mapping[element] for element in elements_of_entity], dtype=int)

    def _finalize_gmsh(self):
        gmsh.finalize()

    def _load_neighbours(self):
        self.neighbours = {}
        for element in self.structural_elements.values():
            if element.first_node not in self.neighbours:
                self.neighbours[element.first_node] = []

            if element.last_node not in self.neighbours:
                self.neighbours[element.last_node] = []

            self.neighbours[element.first_node].append(element.last_node)
            self.neighbours[element.last_node].append(element.first_node)

    def _order_global_indexes(self):
        stack = deque()
        index = 0
        start_node = list(self.nodes.values())[0]
        stack.appendleft(start_node)
        while stack:
            top = stack.pop()
            
            if top.global_index is None:
                top.global_index = index
                index += 1
            else:
                continue
            
            for neighbour in self.neighbours[top]:
                if neighbour.global_index is None:
                    stack.appendleft(neighbour)
        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()

    def load_mesh(self, coordinates, connectivity):

        coordinates = np.loadtxt(coordinates)
        connectivity = np.loadtxt(connectivity, dtype=int).reshape(-1,3)

        newEntity = Entity(1)
        map_indexes = dict(zip(coordinates[:,0], np.arange(1, len(coordinates[:,0])+1, 1)))

        for i, x, y, z in coordinates:
            self.nodes[int(map_indexes[i])] = Node(x, y, z, external_index = int(map_indexes[i]))
            node = int(map_indexes[i]), x, y, z
            newEntity.insertNode(node)

        for i, nodes in enumerate(connectivity[:,1:]):
            first_node = self.nodes[map_indexes[nodes[0]]]
            last_node  = self.nodes[map_indexes[nodes[1]]]
            self.structural_elements[i+1] = StructuralElement(first_node, last_node)
            self.acoustic_elements[i+1] = AcousticElement(first_node, last_node)
            edges = i+1, map_indexes[nodes[0]], map_indexes[nodes[1]]
            newEntity.insertEdge(edges)
            
        self.entities.append(newEntity)
        #Ordering global indexes
        for index, node in enumerate(self.nodes.values()):
            node.global_index = index

        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        self.all_lines.append(1)
        self._map_lines_to_elements(mesh_loaded=True)

    def get_nodal_coordinates_matrix(self, reordering=True):
    # Process the coordinates matrix for all nodes
    # if reordering=True  -> [index(internal), coord_x, coord_y, coord_z] 
    # if reordering=False -> [index(external), coord_x, coord_y, coord_z] 
        number_nodes = len(self.nodes)
        nodal_coordinates = np.zeros((number_nodes, 4))
        if reordering:
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                nodal_coordinates[index,:] = index, node.x, node.y, node.z
        else:               
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                nodal_coordinates[index,:] = external_index, node.x, node.y, node.z
        self.nodal_coordinates_matrix = nodal_coordinates
        return

    def get_connectivity_matrix(self, reordering=True):
        # process the connectivity matrix for all elements
        # if reordering=True  -> [index, first_node(internal), last_node(internal)] 
        # if reordering=False -> [index, first_node(external), last_node(external)]  
        number_elements = len(self.structural_elements)
        connectivity = np.zeros((number_elements, NODES_PER_ELEMENT+1))
        if reordering:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.global_index
                last  = element.last_node.global_index
                connectivity[index,:] = index+1, first, last
        else:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.external_index
                last  = element.last_node.external_index
                connectivity[index,:] = index+1, first, last
        self.connectivity_matrix = connectivity.astype(int) 
        return 

    def get_global_structural_indexes(self):
        # Process the I and J indexes vector for assembly process
        rows, cols = len(self.structural_elements), DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)*DOF_PER_NODE_STRUCTURAL + np.arange(6, dtype=int)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()
    
    def get_global_acoustic_indexes(self):
        # Returns the I and J indexes vector for assembly process
        rows, cols = len(self.acoustic_elements), DOF_PER_NODE_ACOUSTIC*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()

    def get_dict_of_entities(self):
        dict_tag_entity={}
        for entity in self.entities:
            dict_tag_entity[entity.tag] = entity
        return dict_tag_entity

    def _reset_global_indexes(self):
        for node in self.nodes.values():
            node.global_index = None

    def set_element_type_by_element(self, elements, element_type):
        self.element_type = element_type
        for element in slicer(self.structural_elements, elements):
            element.element_type = element_type
    
    def set_cross_section_by_element(self, elements, cross_section, update_cross_section=False):
        if update_cross_section:
            t0 = time()
            cross_section.update_properties()
            dt = time() - t0
            print("Time to process Cross-section: {} [s]".format(round(dt, 6)))
        for element in slicer(self.structural_elements, elements):
            element.cross_section = cross_section
        for element in slicer(self.acoustic_elements, elements):
            element.cross_section = cross_section

    def set_cross_section_by_line(self, lines, cross_section):
        for elements in slicer(self.line_to_elements, lines):
            self.set_cross_section_by_element(elements, cross_section)
    
    def set_element_type_by_line(self, lines, element_type):
        for elements in slicer(self.line_to_elements, lines):
            self.set_element_type_by_element(elements, element_type)

    # Structural physical quantities
    def set_material_by_element(self, elements, material):       
        for element in slicer(self.structural_elements, elements):
            element.material = material
        for element in slicer(self.acoustic_elements, elements):
            element.material = material

    def set_material_by_line(self, lines, material):
        for elements in slicer(self.line_to_elements, lines):
            self.set_material_by_element(elements, material)

    def set_force_by_element(self, elements, loads):
        for element in slicer(self.structural_elements, elements):
            element.loaded_forces = loads
    
    def set_structural_load_bc_by_node(self, nodes_id, values):
        for node in slicer(self.nodes, nodes_id):
            node.loads = values
            node.prescribed_dofs = [None,None,None,None,None,None]
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_nodal_loads = True
                node.there_are_nodal_loads = True
                if not node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.append(node)
                return
            else:
                node.loaded_table_for_nodal_loads = False
            # Checking complex single values    
            check_values = [isinstance(bc, complex) for bc in values]
            if True in check_values:
                node.there_are_nodal_loads = True
                if not node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.append(node)
            else:
                node.there_are_nodal_loads = False
                if node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.remove(node)

    def add_mass_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_masses = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_masses = True
                node.there_are_lumped_masses = True
                if not node in self.nodes_with_masses:
                    self.nodes_with_masses.append(node)
                return
            else:
                node.loaded_table_for_lumped_masses = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_masses = True
                if not node in self.nodes_with_masses:
                    self.nodes_with_masses.append(node)
            else:
                node.there_are_lumped_masses = False
                if node in self.nodes_with_masses:
                    self.nodes_with_masses.remove(node)

    def add_spring_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_stiffness = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_stiffness = True
                node.there_are_lumped_stiffness = True
                if not node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.append(node)
                return
            else:
                node.loaded_table_for_lumped_stiffness = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_stiffness = True
                if not node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.append(node)
            else:
                node.there_are_lumped_stiffness = False
                if node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.remove(node)
    
    def add_damper_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_dampings = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_dampings = True
                node.there_are_lumped_dampings = True
                if not node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.append(node)
                return
            else:
                node.loaded_table_for_lumped_dampings = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_dampings = True
                if not node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.append(node)
            else:
                node.there_are_lumped_dampings = False
                if node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.remove(node)

    def set_prescribed_dofs_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.prescribed_dofs = values
            node.loads = [None,None,None,None,None,None]
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_prescribed_dofs = True
                node.there_are_prescribed_dofs = True
                if not node in self.nodes_with_constrained_dofs:
                    self.nodes_with_constrained_dofs.append(node)
                if not node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.append(node)
                return
            else:
                node.loaded_table_for_prescribed_dofs = False
            # Checking complex single values    
            check_values = [isinstance(bc, complex) for bc in values]
            if True in check_values:
                node.there_are_prescribed_dofs = True
                if complex(0) in values:
                    node.there_are_constrained_dofs = True
                    if not node in self.nodes_with_constrained_dofs:
                        self.nodes_with_constrained_dofs.append(node)
                if not node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.append(node)              
            else:
                node.there_are_prescribed_dofs = False
                node.there_are_constrained_dofs = False
                if node in self.nodes_with_constrained_dofs:
                    self.nodes_with_constrained_dofs.remove(node)
                if node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.remove(node) 

    def enable_fluid_mass_adding_effect(self, reset=False):
        flag = self.flag_fluid_mass_effect
        if reset and flag:
            self.flag_fluid_mass_effect = False
            for element in self.structural_elements.values():
                element.adding_mass_effect = False
        elif not reset:
            self.flag_fluid_mass_effect = True
            for element in self.structural_elements.values():
                element.adding_mass_effect = True

    def set_caped_end_by_element(self, elements, value):       
        for element in slicer(self.structural_elements, elements):
            element.caped_end = value

    def set_caped_end_by_line(self, lines, value):
        for elements in slicer(self.line_to_elements, lines):
            self.set_caped_end_by_element(elements, value)

    def set_stress_intensification_by_element(self, elements, value):       
        for element in slicer(self.structural_elements, elements):
            element.stress_intensification = value

    def set_stress_intensification_by_line(self, lines, value):
        for elements in slicer(self.line_to_elements, lines):
            self.set_stress_intensification_by_element(elements, value)
            
    # Acoustic physical quantities
    def set_fluid_by_element(self, elements, fluid):
        for element in slicer(self.acoustic_elements, elements):
            element.fluid = fluid
        for element in slicer(self.structural_elements, elements):
            element.fluid = fluid
    
    def set_fluid_by_line(self, lines, fluid):
        for elements in slicer(self.line_to_elements, lines):
            self.set_fluid_by_element(elements, fluid)

    def set_acoustic_pressure_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.acoustic_pressure = values
            node.volume_velocity = None
            if not node in self.nodes_with_acoustic_pressure:
                self.nodes_with_acoustic_pressure.append(node)
            if values is None:
                if node in self.nodes_with_acoustic_pressure:
                    self.nodes_with_acoustic_pressure.remove(node)

    def set_volume_velocity_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.volume_velocity = values
            node.acoustic_pressure = None
            if not node in self.nodes_with_volume_velocity:
                self.nodes_with_volume_velocity.append(node)
            if values is None:
                if node in self.nodes_with_volume_velocity:
                    self.nodes_with_volume_velocity.remove(node)

    def set_specific_impedance_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.specific_impedance = values
            if not node in self.nodes_with_specific_impedance:
                self.nodes_with_specific_impedance.append(node)
            if values is None:
                if node in self.nodes_with_specific_impedance:
                    self.nodes_with_specific_impedance.remove(node)
                    
    def set_radiation_impedance_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.radiation_impedance = values

    def get_radius(self):
        for element in self.structural_elements.values():
            first = element.first_node.global_index
            last  = element.last_node.global_index
            radius = element.cross_section.external_radius
            if self.radius.get(first, -1) == -1:
                self.radius[first] = radius
            elif self.radius[first] < radius:
                self.radius[first] = radius
            if self.radius.get(last, -1) == -1:
                self.radius[last] = radius
            elif self.radius[last] < radius:
                self.radius[last] = radius
        return self.radius

    def check_material_all_elements(self):
        self.check_set_material = False
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return

    def check_poisson_all_elements(self):
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material.poisson_ratio == 0:
                self.check_poisson = True
                return

    def check_material_and_cross_section_in_all_elements(self):
        self.check_set_material = False
        self.check_set_crossSection = False
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return
            if element.cross_section is None:
                self.check_set_crossSection = True
                return

    def check_fluid_and_cross_section_in_all_elements(self):
        self.check_set_fluid = False
        self.check_set_crossSection = False
        for element in self.acoustic_elements.values():
            if element.fluid is None:
                self.check_set_fluid = True
                return
            if element.cross_section is None:
                self.check_set_crossSection = True
                return
    
    def check_nodes_attributes(self, acoustic=False, structural=False, coupled=False):
        self.is_there_loads = False
        self.is_there_prescribed_dofs = False
        self.is_there_acoustic_pressure = False
        self.is_there_volume_velocity = False
        for node in self.nodes.values():

            if structural:
                if node.there_are_nodal_loads:
                    self.is_there_loads = True
                    return

                if node.there_are_prescribed_dofs:
                    if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                        self.is_there_prescribed_dofs = True
                        return

                    elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                        self.is_there_prescribed_dofs = True
                        return

            if acoustic or coupled:
                if node.acoustic_pressure is not None:
                    self.is_there_acoustic_pressure = True
                    return

                if node.volume_velocity is not None:
                    self.is_there_volume_velocity = True
                    return    