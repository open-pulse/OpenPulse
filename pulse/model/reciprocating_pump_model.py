import numpy as np
from pathlib import Path
import os

kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5
pi = np.pi


def plt():
    '''
    Matplotlib imports usually take a long time to run.
    This is a trick to only import plt when it actually
    need to be used.
    The only difference is that now you need to call plt like a function
    like `plt().plot([1,2,3])` instead of `plt().plot([1,2,3])`
    '''
    import matplotlib.pyplot
    return matplotlib.pyplot

def plot(x, y, x_label, y_label, title, label="", _absolute=False):

    # plt().ion()

    fig = plt().figure(figsize=[8,6])
    ax_ = fig.add_subplot(1,1,1)

    if _absolute:
        y = np.abs(y)

    ax_.plot(x, y, color=[1,0,0], linewidth = 2, label = label)
    ax_.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12, fontweight = 'bold')
    plt().grid()
    plt().show() 

def plot2(x, y, x_label, y_label, title, labels, colors, linestyles):

    # plt().ion()

    fig = plt().figure(figsize=[8,6])
    ax_ = fig.add_subplot(1,1,1)

    for i, label in enumerate(labels): 
        ax_.plot(x[i], y[i], color=colors[i], linewidth=2, linestyle=linestyles[i], label=label)
    
    ax_.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12, fontweight = 'bold')
    plt().legend()
    plt().grid()
    plt().show() 

def plot_2_yaxis(data_to_plot, title):

    plt().ion()
    fig = plt().figure(figsize=[8,6])
    ax_1 = fig.add_subplot(1,1,1)
    ax_2 = ax_1.twinx()
    
    if len(data_to_plot) == 2:
        for key, data in data_to_plot.items():

            if "axis" in data.keys():
                axis_ = data["axis"]
            if "x_data" in data.keys():
                x_data = data["x_data"]
            if"y_data" in data.keys():
                y_data = data["y_data"]
                if data["y_axis_absolute"]:
                    y_data = np.abs(y_data)
            if "x_label" in data.keys():
                x_label = data["x_label"]
            if "y_label" in data.keys():
                y_label = data["y_label"]
            if "legend_label" in data.keys():
                legend_label = data["legend_label"]
            if "color" in data.keys():
                color = data["color"]
            if "linewidth" in data.keys():
                linewidth = data["linewidth"]
            if "linestyle" in data.keys():
                linestyle = data["linestyle"]

            ax_1.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
            plots = []
            legends = []
            if axis_ == "left":
                plot_1, = ax_1.plot(x_data, y_data, color=color, linewidth=linewidth, linestyle=linestyle, label=legend_label)
                ax_1.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
                plots.append(plot_1)
                legends.append(legend_label)
            else:
                plot_2, = ax_2.plot(x_data, y_data, color=color, linewidth=linewidth, linestyle=linestyle, label=legend_label)
                ax_2.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
                plots.append(plot_2)
                legends.append(legend_label)

        ax_1.set_title(title, fontsize = 12, fontweight = 'bold')
        ax_1.grid()
        ax_2.grid()
        fig.legend(bbox_to_anchor=(1,1), bbox_transform=ax_1.transAxes)
        plt().show() 

class ReciprocatingPumpModel:

    '''
    Reciprocating Pump Model                                     

    This class contains an idealized reciprocating pump model for calculating
    the excitation to the acoustic FE model. The main output data is the volumetric 
    flow in m³/s units which is dealt as an equivalent acoustic volume velocity source.

    Assumptions:

    1) Stead flow;
    2) Ideal gas behavior;
    3) Compression and expansion cycles are isentropic processes;
    4) The suction and discharge pressures remains constant during suction and discharge cycles, respectively;
    5) No heat exchange in suction and discharge cycles; 

    '''

    def __init__( self, parameters, **kwargs):

        self._load_compressor_parameters(parameters)
        self.number_points = kwargs.get('number_points', 1000)
        self.max_frequency = kwargs.get('max_frequency', 300)
        # self.number_of_cylinders = kwargs.get('number_of_cylinders', 1)


    def _load_compressor_parameters(self, parameters):
        """
        """
        self.D = parameters['bore_diameter']                            # Cylinder bore diameter [m]
        self.r = parameters['stroke'] / 2                               # Length of compressor full stroke [m]
        self.L = parameters['connecting_rod_length']                    # Connecting rod length [m]
        self.rod_diam = parameters['rod_diameter']                      # Rod diameter [m]
        self.c_HE = parameters['clearance_HE'] / 100                    # Clearance HE volume as percentage of full volume (%)
        self.c_CE = parameters['clearance_CE'] / 100                    # Clearance CE volume as percentage of full volume (%)
        self.crank_angle_1 = parameters['TDC_crank_angle_1']            # Crank angle (degrees) at which piston in the head end chamber is at top dead center
        self.rpm = parameters['rotational_speed']                       # Rotational speed (rpm)
        self.acting_label = parameters['acting_label']                  # Active cylinder(s) key (int)
        self.number_of_cylinders = parameters['number_of_cylinders']    # Number of cylinders

        pressure_at_suction = parameters['pressure_at_suction']              # Pressure at suction
        pressure_at_discharge = parameters['pressure_at_discharge']          # Pressure at discharge
        temperature_at_suction = parameters['temperature_at_suction']        # Temperature at suction
        self.pressure_unit = parameters['pressure_unit']                     # Pressure unit
        self.temperature_unit = parameters['temperature_unit']               # Temperature unit
        self.bulk_modulus = parameters['bulk_modulus']                       # Fluid bulk modulus (isentropic or isothermal)

        if "kgf/cm²" in self.pressure_unit:
            self.p_suc = pressure_at_suction * kgf_cm2_to_Pa
            self.p_disch = pressure_at_discharge * kgf_cm2_to_Pa
            
        elif "bar" in self.pressure_unit:
            self.p_suc = pressure_at_suction * bar_to_Pa
            self.p_disch = pressure_at_discharge * bar_to_Pa

        if "(g)" in self.pressure_unit:
            self.p_suc += 101325
            self.p_disch += 101325

        self.delta_P = self.p_disch - self.p_suc
        self.p_ratio = self.p_disch / self.p_suc

        if self.temperature_unit == "°C":
            self.T_suc = temperature_at_suction + 273.15
        else:
            self.T_suc = temperature_at_suction

        self.area_head_end = pi * (self.D**2) / 4
        self.area_crank_end = pi * ((self.D**2) - (self.rod_diam**2)) / 4

        if self.acting_label == 0:
            self.active_cylinder = 'both ends'
        elif self.acting_label == 1:
            self.active_cylinder = 'head end'
        elif self.acting_label == 2:
            self.active_cylinder = 'crank end'

        self.tdc_1 = self.crank_angle_1 * pi / 180

    def set_fluid_properties(self, fluid_data: dict):
        """ 
            This method sets the process fluid properties and updates the thermodynamic 
            fluid properties for suction and discharge states.

        Parameters:
        -----------
        isentropic_exponent: float number
        molar_mass: a float number in kg/kmol units.
        
        """

        self.bulk_modulus = fluid_data.get('bulk_modulus', None)                # Bulk modulus [Pa]
        # self.density_at_suction = fluid_data.get('density_at_suction', None)    # Density [kg/m³]

    def recip_x(self, tdc=None):
        """ This method returns the reciprocating piston position.

        Parameters:
        -----------
        tdc: float number that corresponding the crankshaft start position.
        
        Returns:
        ----------
        x: array of float numbers relative to piston position.
        """

        N = self.number_points + 1
        if tdc is None:
            tdc = self.tdc_1

        r = self.r
        l = self.L
        x_max = l + r
        theta = np.linspace(0, 2*pi, N)
        d_theta = theta + tdc
        
        # displacement of piston (reciprocating motion)
        x = (r * np.cos(d_theta) + np.sqrt(l**2 - ((r*np.sin(d_theta))**2))) - x_max

        return theta, x 

    def recip_v(self, tdc=None):
        """ This method returns the reciprocating piston velocity.

        Parameters:
        -----------
        tdc: float number that corresponding the crankshaft start position.
        
        Returns:
        ----------
        v: array of float numbers relative to piston velocity.
        """

        N = self.number_points + 1
        if tdc is None:
            tdc = self.tdc_1

        r = self.r
        l = self.L
        theta = np.linspace(0, 2*pi, N)
        d_theta = theta + tdc
        
        # velocity of piston (reciprocating motion)
        v = -(r * np.sin(d_theta)) * (1 + ((r*np.cos(d_theta))/np.sqrt(l**2 - ((r*np.sin(d_theta))**2))))
        v *= self.rpm * (2 * pi / 60)

        return v

    def get_clearance_data(self, acting_label: str):

        if acting_label == "HE":
            h_0 = self.c_HE*(2*self.r) # clearance height head end
            A = self.area_head_end

        elif acting_label == "CE":
            h_0 = self.c_CE*(2*self.r) # clearance height crank end
            A = self.area_crank_end

        else:
            return None, None, None

        return h_0*A, A, h_0

    def get_cycles_boundary_data(self, acting_label="HE", tdc=None):
        """ This method returns the boundary data for each cycle. 
        """

        V0, A, h0 = self.get_clearance_data(acting_label)

        V1 = V0
        V2 = V1 * (1 + self.delta_P / self.bulk_modulus)
        V3 = (2 * self.r + h0) * A
        V4 = V3 * (1 - self.delta_P / self.bulk_modulus)

        if tdc is None:
            tdc = self.tdc_1

        if acting_label == "HE":
            v_piston = self.recip_v(tdc=tdc)
            theta, x_piston = self.recip_x(tdc=tdc)
            volumes = list((h0 - x_piston)*A)
        else:
            v_piston = -self.recip_v(tdc=tdc)
            theta, x_piston = self.recip_x(tdc=tdc)
            volumes = list((h0 + 2*self.r + x_piston)*A)

        # plot(theta, volumes, "Theta [rad]", "Volume [m³]", title="Head end volumes")

        start_data = dict()
        boundary_data = dict()
        labels = ["V1", "V2", "V3", "V4"]

        # Gets the smallest value from volumes relative to V1 point
        value = min(volumes, key=lambda x:abs(x-V1))
        V1_index = volumes.index(value)

        N = len(volumes)
        _indexes = self.get_shifted_vector(np.arange(N), V1_index)
        _thetas = self.get_shifted_vector(theta, V1_index)
        _volumes = self.get_shifted_vector(volumes, V1_index)
        _v_piston = self.get_shifted_vector(v_piston, V1_index)

        # Processing the nearest valid start point for each cycle
        start = 0
        for j, Vj in enumerate([V1, V2, V3, V4]):
            min_dif = 10
            for i, Vi in enumerate(_volumes):
                if i < start:
                    continue
                if abs(Vi-Vj) <= min_dif:
                    min_dif = abs(Vi-Vj)
                    spot_criteria = [_v_piston[i] > 0, Vi-Vj < 0, _v_piston[i] < 0, Vi-Vj > 0]   
                    if spot_criteria[j]:
                        cache_ind = i + 1
                        n_index = int(_indexes[i+1])
                        cache_theta = _thetas[i+1]
                        cache_Vi = _volumes[i+1]
                    else:
                        cache_ind = i
                        n_index = int(_indexes[i])
                        cache_theta = _thetas[i]
                        cache_Vi = _volumes[i]
                else:
                    start_data[labels[j]] = [n_index, cache_Vi, cache_theta]
                    start = cache_ind
                    # print(f"{acting_label}: {labels[j]} {start_data[labels[j]]}")
                    break
        #
        for j, key in enumerate(["V2", "V3", "V4", "V1"]):

            start_index = start_data[labels[j]][0]
            start_volume = start_data[labels[j]][1]
            start_angle = start_data[labels[j]][2]
            end_index = start_data[key][0] - 1

            if end_index == -1:
                end_index = len(volumes) - 1

            end_angle = theta[end_index]
            end_volume = volumes[end_index]

            boundary_data[labels[j]] = {"indexes" : [start_index, end_index],
                                        "angles"  : [start_angle, end_angle],
                                        "volumes" : [start_volume, end_volume]}

            # print(f"{acting_label}: {labels[j]} {boundary_data[labels[j]]}")

        return boundary_data

    def get_shifted_vector(self, data, index):
        N = len(data)
        output = np.zeros(N, dtype=float)
        output[:N-index] = data[index:]
        output[N-index:] = data[:index]
        return output

    def process_head_end_volumes_and_pressures(self, tdc=None, export_data=True):

        V0, A, h0 = self.get_clearance_data("HE")

        V1 = V0
        V2 = V1 * (1 + self.delta_P / self.bulk_modulus)
        V3 = (2 * self.r + h0) * A
        V4 = V3 * (1 - self.delta_P / self.bulk_modulus)

        angle_data = self.get_cycles_boundary_data(acting_label="HE", tdc=tdc)

        if tdc is None:
            tdc = self.tdc_1

        v_piston = self.recip_v(tdc=tdc)
        theta, x_piston = self.recip_x(tdc=tdc)
        angle = theta * 180 / pi

        N = len(x_piston)
        time = np.linspace(0, 60/self.rpm, N)

        volumes = (h0 - x_piston)*A
        pressures = np.zeros(N, dtype=float)

        valves_info = dict()
        open_suc = np.zeros(N, dtype=bool)
        open_disc = np.zeros(N, dtype=bool)

        stage_log = "Head end - volumes and pressures\n\n"

        # Compression cycle (3) -> (4)
        start_index, end_index = angle_data["V3"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)

        for i in indexes:
            V_i = volumes[i]

            if (round(V3, 12) >= round(V_i, 12) >= round(V4, 12)) and (round(v_piston[i], 8) >= 0):  

                P_i = self.p_suc + self.bulk_modulus * (1 - V_i / V3)
                
                if round(V_i, 12) == round(V4, 12):
                    open_disc[i] = True

                pressures[i] = P_i
                stage_log += f"Compression: {i} {round(angle[i], 3)} {V_i} {round(P_i, 1)}\n"

        # Discharge cycle (4) -> (1)
        start_index, end_index = angle_data["V4"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V4,8) > round(V_i,8) >= round(V1,8)) and (round(v_piston[i],8) >= 0):

                P_i = self.p_disch
                open_disc[i] = True

                pressures[i] = P_i
                stage_log += f"  Discharge: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        # Expasion cycle (1) -> (2)
        start_index, end_index = angle_data["V1"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)

        for i in indexes:
            V_i = volumes[i]

            if (round(V1, 12) <= round(V_i, 12) <= round(V2, 12)) and (round(v_piston[i], 8) <= 0):
    
                P_i = self.p_disch + self.bulk_modulus * (1 - V_i / V1)

                if round(V_i, 12) == round(V2, 12):
                    open_suc[i] = True

                pressures[i] = P_i
                stage_log += f"  Expansion: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        # Suction cycle (2) -> (3)
        start_index, end_index = angle_data["V2"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (V2 < round(V_i,8) <= round(V3,8)) and (round(v_piston[i],8) <= 0):
                P_i = self.p_suc
                open_suc[i] = True

                pressures[i] = P_i
                stage_log += f"    Suction: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        stage_log += "\n"
        valves_info["open suction"] = open_suc
        valves_info["open discharge"] = open_disc

        if export_data:

            fname = f"temporary_data\PV_diagram_head_end_crank_angle_{self.crank_angle_1}.dat"
            fname_log = f"temporary_data\log_info_head_end_{self.crank_angle_1}.txt"
            if not os.path.exists(os.path.dirname(fname)):
                os.mkdir("temporary_data")

            header = "Index, Time [s], Angle [deg], Velocity [m/s], Volumes [m³], Pressures [Pa], Suction valve open [bool], Discharge valve open [bool]\n\n"
            header += f"V1 = {V1}\n"
            header += f"V2 = {V2}\n"
            header += f"V3 = {V3}\n"
            header += f"V4 = {V4}\n"
            indexes = np.arange(N)

            data = np.array([   indexes,
                                time,
                                angle,
                                v_piston,
                                volumes,
                                pressures,
                                open_suc,
                                open_disc   ])

            np.savetxt(fname, data.T, delimiter=",", header=header, fmt="%i, %.14e, %.14e, %.14e, %.14e, %.14e, %i, %i")

            with open(fname_log, 'w+') as f:
                f.write(stage_log)

        return volumes, pressures, valves_info


    def process_crank_end_volumes_and_pressures(self, tdc=None, export_data=True):

        print(f"Bulk modulus: {round(self.bulk_modulus, 6)} [Pa]")

        V0, A, h0 = self.get_clearance_data("CE")

        V1 = V0
        V2 = V1 * (1 + self.delta_P / self.bulk_modulus)
        V3 = (2 * self.r + h0) * A
        V4 = V3 * (1 - self.delta_P / self.bulk_modulus)
        
        angle_data = self.get_cycles_boundary_data(acting_label="CE", tdc=tdc)

        if tdc is None:
            tdc = self.tdc_1

        v_piston = -self.recip_v(tdc=tdc)
        theta, x_piston = self.recip_x(tdc=tdc)
        angle = theta*180/pi
        
        N = len(x_piston)
        time = np.linspace(0, 60/self.rpm, N)

        volumes = (h0 + 2*self.r + x_piston)*A
        pressures = np.zeros(N, dtype=float)

        valves_info = dict()
        open_suc = np.zeros(N, dtype=bool)
        open_disc = np.zeros(N, dtype=bool)

        stage_log = "Crank end - volumes and pressures\n\n"

        # Compression cycle (3) -> (4)
        start_index, end_index = angle_data["V3"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)

        for i in indexes:
            V_i = volumes[i]

            if (round(V3, 12) >= round(V_i, 12) >= round(V4, 12)) and (round(v_piston[i], 8) >= 0):  

                P_i = self.p_suc + self.bulk_modulus * (1 - V_i / V3)
                
                if round(V_i, 12) == round(V4, 12):
                    open_disc[i] = True

                pressures[i] = P_i
                stage_log += f"Compression: {i} {round(angle[i], 3)} {V_i} {round(P_i, 1)}\n"

        # Discharge cycle (4) -> (1)
        start_index, end_index = angle_data["V4"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V4,8) > round(V_i,8) >= round(V1,8)) and (round(v_piston[i],8) >= 0):

                P_i = self.p_disch
                open_disc[i] = True

                pressures[i] = P_i
                stage_log += f"  Discharge: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        # Expasion cycle (1) -> (2)
        start_index, end_index = angle_data["V1"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)

        for i in indexes:
            V_i = volumes[i]

            if (round(V1, 12) <= round(V_i, 12) <= round(V2, 12)) and (round(v_piston[i], 8) <= 0):
    
                P_i = self.p_disch + self.bulk_modulus * (1 - V_i / V1)

                if round(V_i, 12) == round(V2, 12):
                    open_suc[i] = True

                pressures[i] = P_i
                stage_log += f"  Expansion: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        # Suction cycle (2) -> (3)
        start_index, end_index = angle_data["V2"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (V2 < round(V_i,8) <= round(V3,8)) and (round(v_piston[i],8) <= 0):
                P_i = self.p_suc
                open_suc[i] = True

                pressures[i] = P_i
                stage_log += f"    Suction: {i} {round(angle[i], 3)} {V_i} {round(P_i,1)}\n"

        stage_log += "\n"
        valves_info["open suction"] = open_suc
        valves_info["open discharge"] = open_disc

        if export_data:

            fname = f"temporary_data\PV_diagram_crank_end_crank_angle_{self.crank_angle_1}.dat"
            fname_log = f"temporary_data\log_info_crank_end_{self.crank_angle_1}.txt"
            if not os.path.exists(os.path.dirname(fname)):
                os.mkdir("temporary_data")
            
            header = "Index, Time [s], Angle [deg], Velocity [m/s], Volumes [m³], Pressures [Pa], Suction valve open [bool], Discharge valve open [bool]\n\n"
            header += f"V1 = {V1}\n"
            header += f"V2 = {V2}\n"
            header += f"V3 = {V3}\n"
            header += f"V4 = {V4}\n"
            indexes = np.arange(N)
            data = np.array([   indexes,
                                time,
                                angle,
                                v_piston,
                                volumes,
                                pressures,
                                open_suc,
                                open_disc   ])

            np.savetxt(fname, data.T, delimiter=",", header=header, fmt="%i, %.14e, %.14e, %.14e, %.14e, %.14e, %i, %i")
   
            with open(fname_log, 'w+') as f:
                f.write(stage_log)

        return volumes, pressures, valves_info

    def get_cycle_indexes(self, start_index, end_index, N):
        """
        """
        if end_index > start_index:
            indexes = np.arange(start_index, end_index+1, 1)
        else:
            left_ind = np.arange(start_index, N, 1)
            right_ind = np.arange(0, end_index+1, 1)
            indexes = np.append(left_ind, right_ind)
        return indexes


    def flow_head_end(self, tdc=None):

        _, _, valves_info = self.process_head_end_volumes_and_pressures(tdc=tdc)
        if valves_info is None:
            return None

        v_piston = self.recip_v(tdc=tdc)
        #
        N = len(v_piston)
        flow_in = np.zeros(N, dtype=float)
        flow_out = np.zeros(N, dtype=float)

        for i, v in enumerate(v_piston):

            if valves_info["open suction"][i]:
                flow_in[i] = v * self.area_head_end

            if valves_info["open discharge"][i]:
                flow_out[i] = v * self.area_head_end
        
        output_data = dict()
        output_data["in_flow"] = flow_in
        output_data["out_flow"] = flow_out

        return output_data

    def flow_crank_end(self, tdc=None):

        _, _, valves_info = self.process_crank_end_volumes_and_pressures(tdc=tdc)
        if valves_info is None:
            return None

        v_piston = -self.recip_v(tdc=tdc)
        #
        N = len(v_piston)
        flow_in = np.zeros(N, dtype=float)
        flow_out = np.zeros(N, dtype=float)

        for i, v in enumerate(v_piston):

            if valves_info["open suction"][i]:
                flow_in[i] = v*self.area_crank_end

            if valves_info["open discharge"][i]:
                flow_out[i] = v*self.area_crank_end
        
        output_data = dict()
        output_data["in_flow"] = flow_in
        output_data["out_flow"] = flow_out

        return output_data

    def mass_flow_crank_end(self):
        vf = self.flow_crank_end()
        mf = -vf['in_flow']*self.rho_suc
        return mf

    def mass_flow_head_end(self):
        vf = self.flow_head_end(aux_process=True)
        mf = -vf['in_flow']*self.rho_suc
        return mf
    
    def total_mass_flow(self):
        N = self.number_points
        f_he = np.sum(self.mass_flow_head_end())/N
        f_ce = np.sum(self.mass_flow_crank_end())/N
        return f_he + f_ce

    def process_sum_of_volumetric_flow_rate(self, key: str):

        try:

            flow_rate = 0.
            tdc_base = (2 * pi) / self.number_of_cylinders

            for i in range(self.number_of_cylinders):

                tdc = tdc_base * i
                # print(f"Top dead center angle {[i]}: {round(tdc, 6)} [rad]")

                if self.active_cylinder == 'both ends':
                    flow_rate += self.flow_crank_end(tdc=tdc)[key]
                    flow_rate += self.flow_head_end(tdc=tdc)[key]

                elif self.active_cylinder == 'head end':
                    flow_rate += self.flow_head_end(tdc=tdc)[key]

                elif self.active_cylinder == 'crank end':
                    flow_rate += self.flow_crank_end(tdc=tdc)[key]

        except Exception as error:
            print(str(error))
            return None

        return flow_rate

    def get_in_mass_flow(self):
        in_flow = self.process_sum_of_volumetric_flow_rate('in_flow')
        if in_flow is None:
            return None
        else:
            return -np.mean(in_flow) * self.rho_suc

    def get_out_mass_flow(self):
        out_flow = self.process_sum_of_volumetric_flow_rate('out_flow')
        if out_flow is None:
            return None
        else:
            return np.mean(out_flow) * self.rho_disc

    def linear_interpolation(self, x1, x2, y1, y2, y):
        A = y-y1
        B = y2-y
        if y1==y2:
            if y>y1:
                x = ((x1 + x2)/2)*1.01
            else:
                x = ((x1 + x2)/2)*0.99
        else:
            x = (A*x2 + B*x1)/(A+B)
        return x

    def FFT_periodic(self, x_t, one_sided = True):
        N = x_t.shape[0]
        if one_sided: # One-sided spectrum
            Xf = 2*np.fft.fft(x_t)
            Xf[0] = Xf[0]/2
        else: # Two-sided spectrum
            Xf = np.fft.fft(x_t)
        return Xf/N

    def extend_signals(self, data, revolutions):
        Trev = 60/self.rpm
        T = revolutions*Trev
        values_time = np.tile(data[:-1], revolutions) # extending signals
        return values_time, T

    def process_FFT_of_(self, values, revolutions):

        values_time, T = self.extend_signals(values, revolutions)
        values_freq = self.FFT_periodic(values_time)
        df = 1/T
        
        size = len(values_freq)
        if np.remainder(size, 2)==0:
            N = int(size/2)
        else:
            N = int((size + 1)/2)
        frequencies = np.arange(0, N+1, 1)*df

        return frequencies, values_freq[0:N+1]

    def process_FFT_of_volumetric_flow_rate(self, revolutions: int, key: str):

        flow_rate = self.process_sum_of_volumetric_flow_rate(key)

        if flow_rate is None:
            return None, None
        
        freq, flow_rate = self.process_FFT_of_(flow_rate, revolutions)
        mask = freq <= self.max_frequency

        freq = freq[mask]
        flow_rate = flow_rate[mask]

        return freq, flow_rate

    def plot_PV_diagram_both_ends(self):

        volume_HE, pressure_HE, _ = self.process_head_end_volumes_and_pressures()
        volume_CE, pressure_CE, _ = self.process_crank_end_volumes_and_pressures()

        if volume_HE is None:
            return
        if self.pressure_unit == "kgf/cm²":
            pressure_HE /= kgf_cm2_to_Pa
            pressure_CE /= kgf_cm2_to_Pa
        else:
            pressure_HE /= bar_to_Pa
            pressure_CE /= bar_to_Pa

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Reciprocating Pump P-V Diagram"

        volumes = [volume_HE, volume_CE]
        pressures = [pressure_HE, pressure_CE]
        labels = ["Head End", "Crank End"]
        colors = [(1,0,0), (0,0,1)]
        linestyles = ["-", "--"]

        plot2(volumes, pressures, x_label, y_label, title, labels, colors, linestyles)

    def plot_PV_diagram_head_end(self):

        volume_HE, pressure_HE, _ = self.process_head_end_volumes_and_pressures()

        if volume_HE is None:
            return

        if self.pressure_unit == "kgf/cm²":
            pressure_HE /= kgf_cm2_to_Pa
        else:
            pressure_HE /= bar_to_Pa

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V diagram (head end)"

        plot(volume_HE, pressure_HE, x_label, y_label, title)

    def plot_PV_diagram_crank_end(self):

        volume_CE, pressure_CE, _ = self.process_crank_end_volumes_and_pressures()

        if volume_CE is None:
            return
        if self.pressure_unit == "kgf/cm²":
            pressure_CE /= kgf_cm2_to_Pa
        else:
            pressure_CE /= bar_to_Pa
        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V diagram (crank end)"

        plot(volume_CE, pressure_CE, x_label, y_label, title)

    def plot_pressure_vs_time(self):

        _, pressure_HE, _ = self.process_head_end_volumes_and_pressures()
        _, pressure_CE, _ = self.process_crank_end_volumes_and_pressures()
        
        Trev = 60/self.rpm
        N = len(pressure_HE)
        time = np.linspace(0, Trev, N)

        if pressure_HE is None:
            return

        if self.pressure_unit == "kgf/cm²":
            pressure_HE /= kgf_cm2_to_Pa
            pressure_CE /= kgf_cm2_to_Pa
        else:
            pressure_HE /= bar_to_Pa
            pressure_CE /= bar_to_Pa

        x_label = "Time [s]"
        y_label = f"Pressure [{self.pressure_unit}]"
        x_data = [time, time]
        y_data = [pressure_HE, pressure_CE]
        labels = ["Head End", "Crank End"]
        title = "PRESSURES vs TIME PLOT"
        colors = [(1,0,0),(0,0,1)]
        linestyles = ["-","--"]

        plot2(x_data, y_data, x_label, y_label, title, labels, colors, linestyles)

    def plot_volume_vs_time(self):

        volume_HE, _, _ = self.process_head_end_volumes_and_pressures()
        volume_CE, _, _ = self.process_crank_end_volumes_and_pressures()
        Trev = 60/self.rpm
        N = len(volume_HE)

        time = np.linspace(0, Trev, N)

        x_label = "Time [s]"
        y_label = f"Volume [m³]"
        x_data = [time, time]
        y_data = [volume_HE, volume_CE]
        labels = ["Head End", "Crank End"]
        title = "PRESSURES vs TIME PLOT"
        colors = [(1,0,0),(0,0,1)]
        linestyles = ["-","--"]

        plot2(x_data, y_data, x_label, y_label, title, labels, colors, linestyles)

    def plot_volumetric_flow_rate_at_suction_time(self):

        flow_rate = self.process_sum_of_volumetric_flow_rate('in_flow')
        if flow_rate is None:
            return

        avg_flow_rate = np.average(flow_rate)
        print(f"Average flow rate at suction: {round(avg_flow_rate, 6)} [m³/h]")

        Trev = 60/self.rpm
        N = len(flow_rate)

        time = np.linspace(0, Trev, N)
        # angle = np.linspace(0, 2*pi, N)

        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at suction"
        plot(time, flow_rate, x_label, y_label, title)

    def plot_volumetric_flow_rate_at_discharge_time(self):

        flow_rate = self.process_sum_of_volumetric_flow_rate('out_flow')
        if flow_rate is None:
            return

        avg_flow_rate = np.average(flow_rate)
        print(f"Average flow rate at discharge: {round(avg_flow_rate, 6)} [m³/h]")

        Trev = 60/self.rpm
        N = len(flow_rate)

        time = np.linspace(0, Trev, N)
        # angle = np.linspace(0, 2*pi, N)

        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at discharge"
        plot(time, flow_rate, x_label, y_label, title)

    def plot_rod_pressure_load_frequency(self, revolutions):

        _, pressure_head, _ = self.process_head_end_volumes_and_pressures()
        _, pressure_crank, _ = self.process_crank_end_volumes_and_pressures()

        load_head = pressure_head*self.area_head_end
        load_crank = -pressure_crank*self.area_crank_end
        rod_pressure_load_time = (load_head + load_crank) / 1000

        freq, rod_pressure_load = self.process_FFT_of_(rod_pressure_load_time, revolutions)
        mask = freq <= self.max_frequency
        freq = freq[mask]
        rod_pressure_load = rod_pressure_load[mask]

        x_label = "Frequency [Hz]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"
        
        plot(freq, rod_pressure_load, x_label, y_label, title, _absolute=True)  

    def plot_rod_pressure_load_time(self):

        _, pressure_head, _ = self.process_head_end_volumes_and_pressures()
        _, pressure_crank, _ = self.process_crank_end_volumes_and_pressures()

        load_head = pressure_head*self.area_head_end
        load_crank = -pressure_crank*self.area_crank_end
        rod_pressure_load_time = (load_head + load_crank)/1000

        Trev = 60/self.rpm
        N = len(rod_pressure_load_time)
        time = np.linspace(0, Trev, N)
        
        x_label = "Time [s]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"
        
        plot(time, rod_pressure_load_time, x_label, y_label, title, _absolute=True) 

    def plot_piston_position_and_velocity(self, tdc=None, domain="time"):

        _, x = self.recip_x(tdc=tdc)
        v = self.recip_v(tdc=tdc)
        Trev = 60/self.rpm
        N = len(x)

        if domain == "time":
            x_label = "Time [s]"
            x_data = np.linspace(0, Trev, N)
        else:
            x_label = "Angle [deg]"
            x_data = np.linspace(0, 360, N)

        data = dict()
        data["Piston position"] = { "axis" : "left",
                                    "x_data" : x_data,
                                    "y_data" : x,
                                    "x_label" : x_label,
                                    "y_label" : "Piston relative displacement [m]",
                                    "legend_label" : "Piston position",
                                    "color" : [0,0,0],
                                    "linestyle" : "-",
                                    "linewidth" : 2,
                                    "y_axis_absolute" : False }

        data["Piston velocity"] = { "axis" : "right",
                                    "x_data" : x_data,
                                    "y_data" : v,
                                    "x_label" : x_label,
                                    "y_label" : "Piston velocity [m/s]",
                                    "legend_label" : "Piston velocity",
                                    "color" : [0,0,1],
                                    "linestyle" : "-",
                                    "linewidth" : 2,
                                    "y_axis_absolute" : False }

        title = "Piston displacement and velocity during a complete cycle"

        plot_2_yaxis(data, title)

    def plot_volumetric_flow_rate_at_suction_frequency(self, revolutions):
        freq, flow_rate = self.process_FFT_of_volumetric_flow_rate(revolutions, 'in_flow')
        if flow_rate is None:
            return
        x_label = "Frequency [Hz]"
        y_label = "Volumetric head flow rate [m³/s]"
        title = "Volumetric flow rate at suction"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)

    def plot_volumetric_flow_rate_at_discharge_frequency(self, revolutions: int):
        freq, flow_rate = self.process_FFT_of_volumetric_flow_rate(revolutions, 'out_flow')
        if flow_rate is None:
            return
        x_label = "Frequency [Hz]"
        y_label = "Volumetric crank flow rate [m³/s]"
        title = "Volumetric flow rate at discharge"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)

    def plot_head_end_pressure_vs_angle(self):
        
        _, pressure_HE, _ = self.process_head_end_volumes_and_pressures()

        if self.pressure_unit == "kgf/cm²":
            pressure_HE /= kgf_cm2_to_Pa
        else:
            pressure_HE /= bar_to_Pa
        
        N = len(pressure_HE)
        angle = np.linspace(0, 360, N)

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Head end pressure vs Angle"

        plot(angle, pressure_HE, x_label, y_label, title)

    def plot_head_end_volume_vs_angle(self):

        volume_HE, _, _ = self.process_head_end_volumes_and_pressures()

        N = len(volume_HE)
        angle = np.linspace(0, 360, N)

        x_label = "Crank angle [degree]"
        y_label = "Volume [m³]"
        title = "Head end volume vs Angle"

        plot(angle, volume_HE, x_label, y_label, title)

    def plot_crank_end_pressure_vs_angle(self):

        _, pressure_CE, _ = self.process_crank_end_volumes_and_pressures()

        if self.pressure_unit == "kgf/cm²":
            pressure_CE /= kgf_cm2_to_Pa
        else:
            pressure_CE /= bar_to_Pa

        N = len(pressure_CE)
        angle = np.linspace(0, 360, N)

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Crank end pressure vs Angle"

        plot(angle, pressure_CE, x_label, y_label, title)

    def plot_crank_end_volume_vs_angle(self):

        volume_CE, _, _ = self.process_crank_end_volumes_and_pressures(acting_label="CE")

        N = len(volume_CE)
        angle = np.linspace(0, 360, N)

        x_label = "Crank angle [degree]"
        y_label = "Volume [m³]"
        title = "Crank end volume vs Angle"

        plot(angle, volume_CE, x_label, y_label, title)

    def plot_convergence(self, x, y):
        x_label = "Iteration"
        y_label = "Ratio"
        title = "Convergence plot"
        plot(x, y, x_label, y_label, title)

    def plot_convergence_cap(self, x, y):
        x_label = "Iteration"
        y_label = "Capacity parameter"
        title = "Convergence plot"
        plot(x, y, x_label, y_label, title)

    def import_measured_PV_data(self, id_1, id_2, comp):

        paths = list()
        paths.append(Path(f"C:/Repositorios/OpenPulse/measured_data/unidades_C32313/Compressor_{comp}/PT_{id_1}_{id_2}/PT_{id_1}{comp}.txt"))
        paths.append(Path(f"C:/Repositorios/OpenPulse/measured_data/unidades_C32313/Compressor_{comp}/PT_{id_1}_{id_2}/PT_{id_2}{comp}.txt"))
        # paths.append(Path(f"C:/Repositorios/OpenPulse/measured_data/unidades_C32313/Compressor_A/PT_{id_1}_{id_2}/PT_{id_1}A_adiabatic.txt"))
        # paths.append(Path(f"C:/Repositorios/OpenPulse/measured_data/unidades_C32313/Compressor_A/PT_{id_1}_{id_2}/PT_{id_2}A_adiabatic.txt"))

        data = dict()
        for i, path in enumerate(paths):
            basename = os.path.basename(path)[:-4]
            data[basename] = np.loadtxt(path, delimiter=";", skiprows=10)
        
        return data


if __name__ == "__main__":

    parameters = {  
                    'bore_diameter' : 0.105,
                    'stroke' : 0.205,
                    'connecting_rod_length' : 0.50,
                    'rod_diameter' : 0.045,
                    'pressure_ratio' : 1.90788804,
                    'clearance_HE' : 15.8,
                    'clearance_CE' : 18.39,
                    'TDC_crank_angle_1' : 0,
                    'rotational_speed' : 178,
                    'number_of_cylinders' : 5,
                    'acting_label' : 1,
                    'pressure_at_suction' : 2.18 + 1.01325,
                    'pressure_at_discharge' : 322.18 + 1.01325,
                    'temperature_at_suction' : 45,
                    'pressure_unit' : "bar",
                    'temperature_unit' : "°C",
                    'bulk_modulus' : 2.1e9
                    }

    pump = ReciprocatingPumpModel(parameters)

    pump.number_points = 3600
    # pump.plot_rod_pressure_load_frequency(6)

    # pump.plot_PV_diagram_head_end()
    # pump.plot_PV_diagram_crank_end()
    # pump.plot_PV_diagram_both_ends()

    pump.plot_volumetric_flow_rate_at_discharge_time()
    pump.plot_volumetric_flow_rate_at_discharge_frequency(3)

    # mass_in = pump.get_in_mass_flow()
    # mass_out = pump.get_out_mass_flow()
    # total_mass = pump.total_mass_flow()
    # print(mass_in, mass_out, 200*(mass_in-mass_out)/(mass_in+mass_out))
    # print(total_mass)