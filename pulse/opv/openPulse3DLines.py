"""
* OpenPulse Project - LVA UFSC
* Multidisciplinary Optimization Group
*
* openPulse3DLines.py
* <file description>
*
*
* Written by José Luiz de Souza <joseloolo@hotmail.com>
* Modified by <>
"""

import vtk
import numpy as np
from random import randint

class OpenPulse3DLines():
    
    def __init__(self, vertex = None, edges = None):
        self.__vertex = []
        self.__edges = []
        self.__colors_r = []#np.array(np.loadtxt('u_sum.dat'))
        self.teste_cor = vtk.vtkScalarsToColors()
        self.teste_cor.SetRange(0,0.5)
        self.teste_cor.Build()

        self.__check_vertex(vertex)
        self.__check_edges(edges)

        self.colors = vtk.vtkFloatArray()
        self.colors.SetNumberOfComponents(3)

        #VTK Variables
        self.__points = vtk.vtkPoints()
        self.__lines = vtk.vtkCellArray()
        self.__linesPolyData = vtk.vtkPolyData()
        self.__mapper = vtk.vtkPolyDataMapper()
        self.__actor = vtk.vtkActor()
        self.__colors = vtk.vtkUnsignedCharArray()
        self.__colors.SetNumberOfComponents(3)
        self.__namedColors = vtk.vtkNamedColors()
        self.__tubeFilter = vtk.vtkTubeFilter()
        self.__axe_transform = vtk.vtkTransform()
        self.__axe = vtk.vtkAxesActor()

        #Control Variables
        self.__current_gradient_color = 0
        self.__default_color = [255,0,0]
        self.__background_color = self.__namedColors.GetColor3d("SlateGray")

        #Custom Variables
        self.__show_lines = False
        self.__show_random_colors = False
        self.__show_single_color = True
        self.__show_gradient_color = False
        self.__create_axe3D = True
        
        #Tube Variables
        self.__tube_Radius = 0.1
        self.__tube_numberOfSides = 50

        #Axe Variables
        self.__axe_initial_position = (5.0, 0.0, 1.0)
        self.__axe_type_cylinder = True
        self.__axe_show_labels = False

    #============
    #Verification
    #============

    def __check_vertex(self, vertex):
        if vertex is not None:
            self.__vertex = vertex

    def __check_edges(self, edges):
        if edges is not None:
            self.__edges = edges

        

    #======================
    #Load files from system
    #======================

    def load_file_vertex(self, path):
        try:
            vertex = np.array(np.loadtxt(path))
            self.__vertex = vertex
        except IOError:
            print("[openPulse3DLines : load_file_vertex]" + path + " não foi encontrado.")
        
    def load_file_edges(self, path):
        try:
            edges = np.array(np.loadtxt(path))
            self.__edges = edges
        except IOError:
            print("[openPulse3DLines : load_file_edges]" + path + " não foi encontrado.")
    


    #=========================
    #Add new vertexs and edges
    #=========================

    def new_vertex(self, vertex):
        if len(vertex) != 3:
            print("Erro1")
            return
        self.__vertex.append(vertex)

    def new_edges(self, edges):
        if len(edges) != 2:
            print("Erro1")
            return
        self.__edges.append(edges)



    #==========================
    #Erase all vertexs or edges
    #==========================

    def erase_vertex_from_id(self, id):
        pass

    def erase_all_vertexs(self):
        self.__vertex = []

    def erase_edges_from_id(self, id):
        pass

    def erase_all_edges(self):
        self.__edges = []


    #======
    #Colors
    #======

    def __create_random_colors(self):
        color_temp = [randint(0,255),randint(0,255),randint(0,255)]
        self.__colors.InsertNextTypedTuple(color_temp)

    def __create_gradient_color(self, a, b):
        
        #colors.InsertNextTypedTuple(self.teste_cor.GetColor(1))
        #colors = vtk.vtkFloatArray()
        #colors.SetNumberOfComponents(3)
        # Add the colors we created to the colors array
        if a >= 1543:
            self.colors.InsertNextTypedTuple(self.teste_cor.GetColor(0.5))
            return
        #print(len(self.__colors_r))
        print(self.teste_cor.GetColor(self.__colors_r[a-1][1]))
        #print(a)
        #print(self.teste_cor.GetColor(self.__colors_r[a-1][1]))
        self.colors.InsertNextTypedTuple(self.teste_cor.GetColor(self.__colors_r[a-1][1]))
        #self.colors.InsertNextTypedTuple(self.teste_cor.GetColor(b))
        #self.__linesPolyData.GetPointData().SetScalars(colors)
        #print(a,b)

    def __create_single_color(self, color):
        self.__colors.InsertNextTypedTuple(color)

    def __set_line_color(self):
        if self.__show_single_color:
            self.__create_single_color(self.__default_color)

        elif self.__show_random_colors:
            self.__create_random_colors()

        #elif self.__show_gradient_color:
        #    self.__create_gradient_color()

    def __paint_lines(self):
        if self.__show_gradient_color:
            self.__linesPolyData.GetCellData().SetScalars(self.colors)
        else:
            self.__linesPolyData.GetCellData().SetScalars(self.__colors)
        #print(self.__linesPolyData.GetCellData())


    #=======================
    #Self Configure and run
    #=======================

    def start(self):
        self.__data_settings()
        self.__vtk_settings()

    def __data_settings(self):
        self.__add_points()   #Create vertex
        self.__add_edges()    #Create edges

    def __vtk_settings(self):
        self.__init_polyData()
        self.__paint_lines()
        self.__transform_tube()
        self.__init_mapper()
        self.__init_axe()
        self.__init_actor()


    #=============
    #Data Settings
    #=============

    def __add_points(self):
        for points in self.__vertex:
            self.__points.InsertPoint(int(points[0]), points[1]/1000, points[2]/1000, points[3]/1000)

    def __add_edges(self):
        for edges in self.__edges:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, edges[1])
            line.GetPointIds().SetId(1, edges[2])
            self.__lines.InsertNextCell(line)
            if self.__show_gradient_color:
                self.__create_gradient_color(edges[1], edges[2])
            else:
                self.__set_line_color() #Create one color for every edge


    #============
    #VTK Settings
    #============

    def __init_polyData(self):
        self.__linesPolyData.SetPoints(self.__points)
        self.__linesPolyData.SetLines(self.__lines)

    def __transform_tube(self):
        if self.__show_lines:
            return
        
        #Transform line into a tube
        self.__tubeFilter.SetInputData(self.__linesPolyData)
        self.__tubeFilter.SetRadius(self.__tube_Radius)
        self.__tubeFilter.SetNumberOfSides(self.__tube_numberOfSides)
        self.__tubeFilter.Update()

    def __init_mapper(self):
        if self.__show_lines:
            if vtk.VTK_MAJOR_VERSION <= 5:
                self.__mapper.SetInput(self.__linesPolyData)
            else:
                self.__mapper.SetInputData(self.__linesPolyData)
        else:
            if vtk.VTK_MAJOR_VERSION <= 5:
                self.__mapper.SetInput(self.__tubeFilter.GetOutput())
            else:
                self.__mapper.SetInputData(self.__tubeFilter.GetOutput())

    def __init_axe(self):
        if self.__create_axe3D:
            self.__axe_transform.Translate(self.__axe_initial_position)
            if not self.__axe_show_labels:
                self.__axe.AxisLabelsOff()
            if self.__axe_type_cylinder:
                self.__axe.SetShaftTypeToCylinder()
            
            self.__axe.SetUserTransform(self.__axe_transform)
            #axes.SetScale(0.2, 0.2, 0.2)

    def __init_actor(self):
        self.__actor.SetMapper(self.__mapper)


    #===================
    #Getters and Setters
    #===================

    def getActor(self):
        return self.__actor

    def setSingleLineColor(self, value):
        self.__default_color = value

    def SetBackgroundColor(self, value):
        self.__background_color = value

    def setShowLines(self, value):
        self.__show_lines = value

    def setShowRandomColors(self, value):
        self.__show_random_colors = value

    def setShowSingleColor(self, value):
        self.__show_single_color = value

    def setShowGradientColor(self, value):
        self.__show_gradient_color = value

    def setCreateAxe3D(self, value):
        self.__create_axe3D = value

    def setTubeRadius(self, value):
        self.__tube_Radius = value

    def setTubeNumberOfSides(self, value):
        self.__tube_numberOfSides = value

    def setAxeTypeCylinder(self, value):
        self.__axe_type_cylinder = value

    def setAxeShowLabels(self, value):
        self.__axe_show_labels = value