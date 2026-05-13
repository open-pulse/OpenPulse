import logging
import numpy as np
import os

from dataclasses import dataclass, fields
from enum import IntEnum
from functools import wraps
from pathlib import Path
from scipy.signal import butter, filtfilt

from pulse import OPEN_PULSE_DIR
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_pressure_unit, convert_temperature_unit


class CylindersActingMode(IntEnum):
    BOTH_ENDS = 0
    HEAD_END = 1
    CRANK_END = 2


pi = np.pi


def ignore_extra_kwargs(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        
        # expected fields of original dataclass
        expected_fields = {f.name for f in fields(cls)}

        # filter the unnecessary kwargs
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in expected_fields}

        original_init(self, *args, **filtered_kwargs)

    cls.__init__ = new_init
    return cls


@ignore_extra_kwargs
@dataclass
class ReciprocatingCompressorModel:

    '''
    COMPRESSOR MODEL                                     

    This class contains a simplified reciprocating compressor model for calculating
    the excitation to the acoustic FE model. The main output data is the volumetric 
    flow in m³/s units which is dealt as an equivalent acoustic volume velocity source.

    Assumptions:

    1) Stead flow;
    2) Ideal gas behavior;
    3) Compression and expansion cycles are isentropic processes;
    4) The suction and discharge pressures remains constant during suction and discharge cycles, respectively;
    5) No heat exchange in suction and discharge cycles; 

    '''

    # compressor configuration
    acting_mode : int = CylindersActingMode.BOTH_ENDS                       # Active cylinder(s) key
    number_of_cylinders : int = 1                                           # Number of cylinders

    # geometric parameters
    bore_diameter : float = 0.                                              # Cylinder bore diameter [m]
    stroke : float = 0.                                                     # Stoke length [m]
    connecting_rod_length : float = 0.                                      # Connecting rod length [m]
    rod_diameter : float = 0.                                               # Rod diameter [m]
    clearance_HE : float = 0.                                               # Clearance HE volume as percentage of HE full volume (%)
    clearance_CE : float = 0.                                               # Clearance CE volume as percentage of CE full volume (%)
    tdc_crank_angle_1 : float = 0.                                          # Crank angle (degrees) at which piston in the head-end chamber is at top dead center
    tdc_crank_angle_2 : float | None = None                                 # Crank angle (degrees) at which piston in the head-end chamber is at top dead center
 
    # operational parameters
    capacity : float = 100                                                  # Capacity of compression stage (%)
    rotational_speed : float = 0.                                           # Compressor rotational speed (rpm)

    # fluid properties
    suction_pressure : float = 0.                                           # Suction pressure
    suction_temperature : float = 0.                                        # Suction temperature
    pressure_unit : str = "Pa"                                              # Pressure unit
    temperature_unit : str = "K"                                            # Temperature unit
    pressure_ratio : float = 0.                                              # Compressor pressure ratio Pd/Ps
    isentropic_exponent : float = 1.4                                       # Isentropic exponent (Cp/Cv)
    molar_mass : float = 2.0158                                             # Molar mass [kg/kmol] - hydrogen as default

    # signal processing parameters
    number_points : int = 1000                                              # Number of points considered in one cycle
    max_frequency : float = 300                                             # Maximum frequency of interest

    cap = None

    @property
    def radius(self):
        return self.stroke / 2
    
    @property
    def capacity_fraction(self):
        return self.capacity / 100

    @property
    def clearance_HE_fraction(self):
        return self.clearance_HE / 100
    
    @property
    def clearance_CE_fraction(self):
        return self.clearance_CE / 100
    
    @property
    def tdc_1(self):
        return self.tdc_crank_angle_1 * pi / 180

    @property
    def tdc_2(self):
        if self.tdc_crank_angle_2 is None:
            return None
        return self.tdc_crank_angle_2 * pi / 180

    @property
    def rpm(self):
        return self.rotational_speed

    @property
    def area_head_end(self):
        return pi * (self.bore_diameter**2) / 4

    @property
    def area_crank_end(self):
        return pi * ((self.bore_diameter**2) - (self.rod_diameter**2)) / 4

    def process_remaining_fluid_properties(self):

        # convert suction pressure unit
        self.P_suction = convert_pressure_unit(self.suction_pressure, self.pressure_unit, "Pa")
        
        # convert suction temperature unit
        self.T_suction = convert_temperature_unit(self.suction_temperature, self.temperature_unit, "K")

        self.k = self.isentropic_exponent           # Compressed gas isentropic exponent
        self.vr = (self.P_suction)**(-1/self.k)     # Volume ratio considering isentropic compression
        self.Ru = 8314.4621                         # Universal ideal gas constant [J/kmol.K]
        self.R = self.Ru / self.molar_mass          # Gas constant [J/kg.K]

        # discharge pressure
        self.P_discharge = self.pressure_ratio * self.P_suction

        # discharge temperature
        self.T_discharge = self.T_suction * (self.pressure_ratio**((self.k - 1) / self.k))

        # density at the suction
        self.rho_suc = self.P_suction / (self.R * self.T_suction)

        # density at the discharge
        self.rho_disc = (self.P_suction * self.pressure_ratio) / (self.R * self.T_discharge)

    def update_fluid_properties(self, isentropic_exponent: float, molar_mass: float):
        self.isentropic_exponent = isentropic_exponent
        self.molar_mass = molar_mass
        self.process_remaining_fluid_properties()

    def recip_x(self, tdc : float | None = None):
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

        r = self.radius
        L = self.connecting_rod_length
        x_max = L + r

        theta = np.linspace(0, 2 * pi, N)
        d_theta = theta + tdc

        x = (r * np.cos(d_theta) + np.sqrt(L**2 - ((r * np.sin(d_theta))**2))) - x_max

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

        r = self.radius
        L = self.connecting_rod_length

        theta = np.linspace(0, 2*pi, N)
        d_theta = theta + tdc

        v = -(r * np.sin(d_theta))*(1 + ((r*np.cos(d_theta))/np.sqrt(L**2 - ((r*np.sin(d_theta))**2))))
        v *= self.rpm * (2 * pi / 60)

        return v

    def get_clearance_data(self, acting_label: str):

        if acting_label == "HE":
            # clearance height head-end
            h_0 = self.clearance_HE_fraction * (2 * self.radius)
            A = self.area_head_end

        elif acting_label == "CE":
            # clearance height crank-end
            h_0 = self.clearance_CE_fraction * (2 * self.radius)
            A = self.area_crank_end

        else:
            return None, None, None

        V_0 = h_0 * A

        return V_0, A, h_0

    def get_cycles_boundary_data(self, acting_label : str = "HE", tdc: float | None = None):
        """ This method returns the boundary data for each cycle. 
        """

        V0, A, h0 = self.get_clearance_data(acting_label)

        V1 = V0
        V2 = V1 * (self.pressure_ratio)**(1/self.k)
        V3 = (2 * self.radius + h0) * A
        V4 = V3 * (1 / self.pressure_ratio)**(1/self.k)

        if tdc is None:
            tdc = self.tdc_1

        if acting_label == "HE":
            v_piston = self.recip_v(tdc=tdc)
            theta, x_piston = self.recip_x(tdc=tdc)
            volumes = list((h0 - x_piston)*A)
        else:
            v_piston = -self.recip_v(tdc=tdc)
            theta, x_piston = self.recip_x(tdc=tdc)
            volumes = list((h0 + 2 * self.radius + x_piston) * A)

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

    def process_head_end_volumes_and_pressures(
        self, 
        tdc: float | None = None, 
        capacity: float | None = None, 
        export_data: bool = False,
        ):

        V0, A, h0 = self.get_clearance_data("HE")

        V1 = V0
        V2 = V1 * (self.pressure_ratio)**(1 / self.k)
        V3 = V3c = (2 * self.radius + h0) * A
        V4 = V4c= V3 * (1 / self.pressure_ratio)**(1 / self.k)

        angle_data = self.get_cycles_boundary_data(acting_label="HE", tdc=tdc)
        # [theta_3i, theta_3f] = angle_data["V3"]["angles"]
        # [theta_4i, theta_4f] = angle_data["V4"]["angles"]

        # if capacity is None:
        #     if self.cap is None:
        #         self.cap = self.process_capacity(capacity = self.capacity_fraction)
        #         if self.cap == -1:
        #             return None, None, None
        #     capacity = self.cap

        if tdc is None:
            tdc = self.tdc_1

        v_piston = self.recip_v(tdc=tdc)
        theta, x_piston = self.recip_x(tdc=tdc)
        angle = theta*180/pi
        
        N = len(x_piston)
        time = np.linspace(0, 60 / self.rpm, N)

        volumes = (h0 - x_piston)*A
        pressures = np.zeros(N, dtype=float)

        if capacity is None:
            capacity = self.capacity_fraction

        if capacity < 1:
            start_index, end_index = angle_data["V4"]["indexes"]
            indexes = self.get_cycle_indexes(start_index, end_index, N)
            V4_i = capacity*(V4-V0) + V0
            for i in indexes:
                V_i = volumes[i]
                if V_i >= V4_i:
                    V4c = V_i
                    V3c = V4c/((1 / self.pressure_ratio)**(1 / self.k))
                else:
                    break

        valves_info = dict()
        open_suc = np.zeros(N, dtype=bool)
        open_disc = np.zeros(N, dtype=bool)

        # print(f"Capacity (head-end): {capacity}")
        stage_log = f"Capacity (head-end) = {capacity}\n\n"

        # Compression cycle (3) -> (4)
        start_index, end_index = angle_data["V3"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V3c,8) <= round(V_i,8) <= round(V3,8)):

                P_i = self.P_suction
                open_suc[i] = True
                stage_log += f"Compression (null): {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            elif (round(V3c,8) > round(V_i,8) >= round(V4c,8)) and (round(v_piston[i],8) > 0):  

                cap_param = round((V_i - V0)/(V4 - V0), 3)
                P_i = ((V3c/V_i)**(self.k))*self.P_suction
                stage_log += f"Compression: {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {cap_param}\n"
                
                if round(V_i,8) == round(V4c,8):
                    open_disc[i] = True

                # # the compressor mass flow capacity control is obtained by letting 
                # # the suction valve oppened at the begning of compression cycle
                # cap_param = round((theta_4i-theta[i])/(theta_4i-theta_3i), 3)
                # if (theta_4i-theta[i])/(theta_4i-theta_3i) > capacity:
                #     P_i = self.P_suction
                #     open_suc[i] = True
                #     V3c = (h0 - x_piston[i])*A
                #     V4c = V3c*(1/self.pressure_ratio)**(1/self.k)
                #     stage_log += f"Compression (null): {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {V3c} {V4c} {cap_param}\n"
                # else:
                #     P_i = ((V3c/V_i)**(self.k))*self.P_suction
                #     stage_log += f"Compression: {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {cap_param}\n"

                # if V_i == round(V4c,8):
                #     open_disc[i] = True

            pressures[i] = P_i

        # Discharge cycle (4) -> (1)
        start_index, end_index = angle_data["V4"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V3c,8) >= round(V_i,8) > round(V4c,8)) and (round(v_piston[i],8) >= 0):
                P_i = ((V3c/V_i)**(self.k))*self.P_suction
                stage_log += f"Discharge (remaining compression): {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            elif (round(V4c,8) >= round(V_i,8) >= round(V1,8)) and (round(v_piston[i],8) >= 0):
                P_i = self.P_discharge
                open_disc[i] = True
                stage_log += f"Discharge: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            pressures[i] = P_i

        # Expasion cycle (1) -> (2)
        start_index, end_index = angle_data["V1"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]
            if (V1 < round(V_i,8) <= round(V2,8)) and (round(v_piston[i],8) < 0):
                P_i = ((V1/V_i)**(self.k))*self.P_discharge
                if round(V_i,8) == round(V2,8):
                    open_suc[i] = True
                stage_log += f"Expansion: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"
            elif round(V_i,8) == round(V1, 8):
                P_i = self.P_discharge
                open_disc[i] = True

            pressures[i] = P_i

        # Suction cycle (2) -> (3)
        start_index, end_index = angle_data["V2"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]
            if (V2 < round(V_i,8) <= round(V3,8)) and (round(v_piston[i],8) <= 0):
                P_i = self.P_suction
                open_suc[i] = True                
                pressures[i] = P_i
                stage_log += f"Suction: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

        stage_log += "\n"
        valves_info["open suction"] = open_suc
        valves_info["open discharge"] = open_disc

        if export_data:

            folder_path = OPEN_PULSE_DIR.cwd() / "temporary_data"
            folder_path.mkdir(exist_ok=True)

            fname = folder_path / f"PV_diagram_head_end_crank_angle_{self.tdc_crank_angle_1}.dat"
            fname_log =folder_path / f"log_info_head_end_{self.tdc_crank_angle_1}_cap_{capacity}.txt"

            header = "Index, Time [s], Angle [deg], Velocity [m/s], Volumes [m³], Pressures [Pa], Suction valve open [bool], Discharge valve open [bool]\n\n"
            header += f"V1 = {V1}\n"
            header += f"V2 = {V2}\n"
            header += f"V3 = {V3}\n"
            header += f"V4 = {V4}\n"

            indexes = np.arange(N)
            data = np.array([
                indexes,
                time,
                angle,
                v_piston,
                volumes,
                pressures,
                open_suc,
                open_disc,
                ], dtype=float)

            np.savetxt(fname, data.T, delimiter=",", header=header, fmt="%i, %.14e, %.14e, %.14e, %.14e, %.14e, %i, %i")

            with open(fname_log, 'w+') as f:
                f.write(stage_log)

        return volumes, pressures, valves_info

    def process_crank_end_volumes_and_pressures(
        self, 
        tdc: float | None = None, 
        capacity: float | None = None, 
        export_data: bool = False,
        ):

        V0, A, h0 = self.get_clearance_data("CE")

        V1 = V0
        V2 = V1 * (self.pressure_ratio)**(1 / self.k)
        V3 = V3c = (2 * self.radius + h0) * A
        V4 = V4c= V3 * (1 / self.pressure_ratio)**(1 / self.k)
        
        angle_data = self.get_cycles_boundary_data(acting_label="CE", tdc=tdc)
        # [theta_3i, theta_3f] = angle_data["V3"]["angles"]
        # [theta_4i, theta_4f] = angle_data["V4"]["angles"]

        # if capacity is None:
        #     if self.cap is None:
        #         self.cap = self.process_capacity(capacity = self.capacity_fraction)
        #         if self.cap == -1:
        #             return None, None, None
        #     capacity = self.cap

        if tdc is None:
            tdc = self.tdc_1

        v_piston = -self.recip_v(tdc=tdc)
        theta, x_piston = self.recip_x(tdc=tdc)
        angle = theta*180/pi
        
        N = len(x_piston)
        time = np.linspace(0, 60 / self.rpm, N)

        volumes = (h0 + 2 * self.radius + x_piston) * A
        pressures = np.zeros(N, dtype=float)

        if capacity is None:
            capacity = self.capacity_fraction

        if capacity < 1:
            start_index, end_index = angle_data["V4"]["indexes"]
            indexes = self.get_cycle_indexes(start_index, end_index, N)
            V4_i = capacity*(V4-V0) + V0
            for i in indexes:
                V_i = volumes[i]
                if V_i >= V4_i:
                    V4c = V_i
                    V3c = V4c/((1/self.pressure_ratio)**(1/self.k))
                else:
                    # print(i, self.capacity_fraction, V_i, V4c, V3c)
                    break

        valves_info = dict()
        open_suc = np.zeros(N, dtype=bool)
        open_disc = np.zeros(N, dtype=bool)

        # print(f"Capacity (crank-end): {capacity}")
        stage_log = f"Capacity (crank-end) = {capacity}\n\n"
        
        # Compression cycle (3) -> (4)
        start_index, end_index = angle_data["V3"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V3c,8) <= round(V_i,8) <= round(V3,8)):

                P_i = self.P_suction
                open_suc[i] = True
                stage_log += f"Compression (null): {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            elif (round(V3c,8) > round(V_i,8) >= round(V4c,8)) and (round(v_piston[i],8) > 0):  

                cap_param = round((V_i - V0)/(V4 - V0), 3)
                P_i = ((V3c/V_i)**(self.k))*self.P_suction
                stage_log += f"Compression: {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {cap_param}\n"
                
                if round(V_i,8) == round(V4c,8):
                    open_disc[i] = True

                # # the compressor mass flow capacity control is obtained by letting 
                # # the suction valve oppened at the begning of compression cycle
                # cap_param = round((theta_4i-theta[i])/(theta_4i-theta_3i), 3)
                # if (theta_4i-theta[i])/(theta_4i-theta_3i) > capacity:
                #     P_i = self.P_suction
                #     open_suc[i] = True
                #     V3c = (h0 - x_piston[i])*A
                #     V4c = V3c*(1/self.pressure_ratio)**(1/self.k)
                #     stage_log += f"Compression (null): {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {V3c} {V4c} {cap_param}\n"
                # else:
                #     P_i = ((V3c/V_i)**(self.k))*self.P_suction
                #     stage_log += f"Compression: {i} {round(angle[i],1)} {V_i} {round(P_i,1)} {cap_param}\n"

                # if V_i == round(V4c,8):
                #     open_disc[i] = True

            pressures[i] = P_i

        # Discharge cycle (4) -> (1)
        start_index, end_index = angle_data["V4"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]

            if (round(V3c,8) >= round(V_i,8) > round(V4c,8)) and (round(v_piston[i],8) >= 0):
                P_i = ((V3c/V_i)**(self.k))*self.P_suction
                stage_log += f"Discharge (remaining compression): {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            elif (round(V4c,8) >= round(V_i,8) >= round(V1,8)) and (round(v_piston[i],8) >= 0):
                P_i = self.P_discharge
                open_disc[i] = True
                stage_log += f"Discharge: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            pressures[i] = P_i

        # Expasion cycle (1) -> (2)
        start_index, end_index = angle_data["V1"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]
            if (V1 < V_i <= round(V2,8)) and (round(v_piston[i],8) < 0):
                P_i = ((V1/V_i)**(self.k))*self.P_discharge
                if round(V_i,8) == round(V2,8):
                    open_suc[i] = True
                stage_log += f"Expansion: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"
            elif round(V_i,8) == round(V1, 8):
                P_i = self.P_discharge
                open_disc[i] = True
                stage_log += f"Discharge: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

            pressures[i] = P_i

        # Suction cycle (2) -> (3)
        start_index, end_index = angle_data["V2"]["indexes"]
        indexes = self.get_cycle_indexes(start_index, end_index, N)
        for i in indexes:
            V_i = volumes[i]
            if (V2 < round(V_i,8) <= round(V3,8)) and (round(v_piston[i],8) <= 0):
                P_i = self.P_suction
                open_suc[i] = True
                pressures[i] = P_i
                stage_log += f"Suction: {i} {round(angle[i],1)} {V_i} {round(P_i,1)}\n"

        stage_log += "\n"
        valves_info["open suction"] = open_suc
        valves_info["open discharge"] = open_disc

        if export_data:

            folder_path = OPEN_PULSE_DIR.cwd() / "temporary_data"
            folder_path.mkdir(exist_ok=True)

            fname = folder_path / f"PV_diagram_crank_end_crank_angle_{self.tdc_crank_angle_1}.dat"
            fname_log =folder_path / f"log_info_crank_end_{self.tdc_crank_angle_1}_cap_{capacity}.txt"

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
   
            # if capacity == 0.8:
            with open(fname_log, 'w+') as f:
                f.write(stage_log)

        return volumes, pressures, valves_info

    def get_cycle_indexes(self, start_index, end_index, N):

        if end_index > start_index:
            indexes = np.arange(start_index, end_index+1, 1)

        else:
            left_ind = np.arange(start_index, N, 1)
            right_ind = np.arange(0, end_index + 1, 1)
            indexes = np.append(left_ind, right_ind)

        return indexes

    def flow_head_end(self, tdc=None, capacity=1):

        _, _, valves_info = self.process_head_end_volumes_and_pressures(tdc=tdc, capacity=capacity)
        if valves_info is None:
            return None

        # the piston velocity
        v_piston = self.recip_v(tdc=tdc)

        # # volumetric flow rate for head-end cylinder (for loop)
        # N = len(v_piston)
        # flow_in = np.zeros(N, dtype=float)
        # flow_out = np.zeros(N, dtype=float)

        # for i, v in enumerate(v_piston):
        #     if valves_info["open suction"][i]:
        #         flow_in[i] = v * self.area_head_end
        #     if valves_info["open discharge"][i]:
        #         flow_out[i] = v * self.area_head_end

        # volumetric flow rate for head-end cylinder (direct)
        flow_in = v_piston * self.area_head_end * valves_info["open suction"].astype(int)
        flow_out = v_piston * self.area_head_end * valves_info["open discharge"].astype(int)

        output_data = {
            "in_flow" : flow_in,
            "out_flow" : flow_out,
        }

        return output_data

    def flow_crank_end(self, tdc=None, capacity=1):

        _, _, valves_info = self.process_crank_end_volumes_and_pressures(tdc=tdc, capacity=capacity)
        if valves_info is None:
            return None

        # the piston velocity on the crank-end side is opposite to the head-end ones
        v_piston = -self.recip_v(tdc=tdc)

        # # volumetric flow rate for crank-end cylinder (for loop)
        # N = len(v_piston)
        # flow_in = np.zeros(N, dtype=float)
        # flow_out = np.zeros(N, dtype=float)

        # for i, v in enumerate(v_piston):
        #     if valves_info["open suction"][i]:
        #         flow_in[i] = v * self.area_crank_end
        #     if valves_info["open discharge"][i]:
        #         flow_out[i] = v * self.area_crank_end

        # volumetric flow rate for crank-end cylinder (direct)
        flow_in = v_piston * self.area_crank_end * valves_info["open suction"].astype(int)
        flow_out = v_piston * self.area_crank_end * valves_info["open discharge"].astype(int)

        output_data = {
            "in_flow" : flow_in,
            "out_flow" : flow_out,
        }

        return output_data

    def mass_flow_crank_end(self, capacity=None):
        vf = self.flow_crank_end(capacity=capacity)
        mf = -vf['in_flow'] * self.rho_suc
        return mf

    def mass_flow_head_end(self, capacity=None):
        vf = self.flow_head_end(capacity=capacity)
        mf = -vf['in_flow'] * self.rho_suc
        return mf

    def total_mass_flow(self):
        N = self.number_points
        f_he = np.sum(self.mass_flow_head_end()) / N
        f_ce = np.sum(self.mass_flow_crank_end()) / N
        return f_he + f_ce

    def process_sum_of_volumetric_flow_rate(self, key: str, capacity=None, smooth_data=False):
        try:

            if self.acting_mode == CylindersActingMode.BOTH_ENDS:

                if self.number_of_cylinders == 1:
                    flow_rate = self.flow_crank_end(tdc=self.tdc_1, capacity=capacity)[key]
                    flow_rate += self.flow_head_end(tdc=self.tdc_1, capacity=capacity)[key]
                else:
                    flow_rate = self.flow_crank_end(tdc=self.tdc_1, capacity=capacity)[key]
                    flow_rate += self.flow_head_end(tdc=self.tdc_1, capacity=capacity)[key]
                    flow_rate += self.flow_crank_end(tdc=self.tdc_2, capacity=capacity)[key] 
                    flow_rate += self.flow_head_end(tdc=self.tdc_2, capacity=capacity)[key]

            elif self.acting_mode == CylindersActingMode.HEAD_END:

                if self.number_of_cylinders == 1:
                    flow_rate = self.flow_head_end(tdc=self.tdc_1, capacity=capacity)[key]
                else:
                    flow_rate = self.flow_head_end(tdc=self.tdc_1, capacity=capacity)[key]
                    flow_rate += self.flow_head_end(tdc=self.tdc_2, capacity=capacity)[key]

            elif self.acting_mode == CylindersActingMode.CRANK_END:

                if self.number_of_cylinders == 1:
                    flow_rate = self.flow_crank_end(tdc=self.tdc_1, capacity=capacity)[key]
                else:
                    flow_rate = self.flow_crank_end(tdc=self.tdc_1, capacity=capacity)[key]
                    flow_rate += self.flow_crank_end(tdc=self.tdc_2, capacity=capacity)[key]

        except Exception as error:
            logging.error(str(error))
            return None

        if smooth_data:
    
            N = len(flow_rate)
            fs = N * (self.rpm / 60)

            flow_rate_ext = np.append(flow_rate[:-1], flow_rate)
            flow_rate_ext = np.append(flow_rate_ext, flow_rate[1:])

            b, a = butter(1, fs/15, btype='low', fs=fs,  output='ba')
            flow_rate = filtfilt(b, a, flow_rate_ext)[N-1 : 2*N-1]

        return flow_rate

    def get_in_mass_flow(self, capacity=None):

        in_flow = self.process_sum_of_volumetric_flow_rate('in_flow', capacity=capacity)
        if in_flow is None:
            return None

        else:
            return -np.mean(in_flow) * self.rho_suc

    def get_out_mass_flow(self, capacity=None):

        out_flow = self.process_sum_of_volumetric_flow_rate('out_flow', capacity=capacity)
        if out_flow is None:
            return None

        else:
            return np.mean(out_flow) * self.rho_disc

    def get_nearest_capacity(self, list_caps, nearest_absolute=True):

        values = np.array([self.get_in_mass_flow(capacity=_cap) for _cap in list_caps])
        if nearest_absolute:
            indexes = np.argsort(np.abs(values - self.final_mass_flow))

        else:
            indexes = np.argsort(values - np.min(values))

        output = np.array(list_caps)[indexes]

        return output[0]

    def process_capacity(self, capacity=1):

        cap_aux = list()
        mass_flow_aux = list()
        ratio = list()
        iterations = list()

        if capacity == 1:
            return 1
        elif capacity < 0.005 or capacity > 1:
            return -1
        else:
            mass_flow_full_capacity = self.get_in_mass_flow(capacity=1)
            print(f"final mass flow: {capacity*mass_flow_full_capacity}")

            if mass_flow_full_capacity == -1:
                return -1
            self.final_mass_flow = capacity*mass_flow_full_capacity

            cap_aux.append(capacity)
            stable = False
            _interp = False
            self.flag_max_iter = True
            max_iter = 100
            i = 0

            while not stable and i != max_iter: 
                
                iter_flow = self.get_in_mass_flow(capacity=cap_aux[i])
                if iter_flow is None:
                    return -1

                # temporary structure due to a negative flow rate at small capacities
                while iter_flow < 0: 
                    if 2*cap_aux[i] < 1:
                        cap_aux[i] *= 2
                        iter_flow = self.get_in_mass_flow(capacity=cap_aux[i])
                    else:
                        return -1
                    if iter_flow > 0: # improve the convergence reducing the domain
                        temp_cap = cap_aux[i]*(3/2)
                        iter_flow_temp = self.get_in_mass_flow(capacity=temp_cap)
                        cap_aux[i] = self.linear_interpolation(cap_aux[i], temp_cap, iter_flow, iter_flow_temp, self.final_mass_flow)
                        iter_flow = self.get_in_mass_flow(capacity=cap_aux[i])

                mass_flow_aux.append(iter_flow)
                avg_mass_flow = (self.final_mass_flow + iter_flow)/2
                ratio.append(iter_flow/self.final_mass_flow)
              
                # print("Iter. flow: {} \nAvg. flow: {}".format(iter_flow, avg_mass_flow ))
                # print("Capacity: {} \nRatio: {}\n".format(cap_aux[i], (iter_flow/self.final_mass_flow)))

                if len(mass_flow_aux) >= 2:
                    cap = self.linear_interpolation(cap_aux[i-1], cap_aux[i], mass_flow_aux[i-1], mass_flow_aux[i], self.final_mass_flow)
                    cap_aux.append(cap) 
                else:
                    cap_aux.append(cap_aux[i]*(self.final_mass_flow/avg_mass_flow)) 
                        
                if i > 2:
                    # promote the linear average if ratio does not change in 3 iterations
                    if ratio[i-1]==ratio[i-2]: 
                        if ratio[i]==ratio[i-1]:
                            cap = np.mean(cap_aux[-2:])
                        else: # promote the linear interpolation if periodic
                            cap = self.linear_interpolation(cap_aux[i-1], cap_aux[i], mass_flow_aux[i-1], mass_flow_aux[i], self.final_mass_flow)
                        stable = True
                        list_caps = [cap, cap_aux[i-1], cap_aux[i]]
                        cap = self.get_nearest_capacity(list_caps, nearest_absolute=True)
                iterations.append(i)
                i += 1 
                
            if i == max_iter:
                self.flag_max_iter = True 
            # self.plot_convergence(iterations, ratio)
            return cap

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
            Xf[0] = Xf[0] / 2

        else: # Two-sided spectrum
            Xf = np.fft.fft(x_t)

        return Xf/N

    def extend_signals(self, data: np.ndarray, revolutions: int):

        Trev = 60 / self.rpm
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

    def process_FFT_of_volumetric_flow_rate(self, revolutions, key):

        flow_rate = self.process_sum_of_volumetric_flow_rate(key)

        if flow_rate is None:
            return None, None
        
        freq, flow_rate = self.process_FFT_of_(flow_rate, revolutions)
        freq = freq[freq <= self.max_frequency]
        flow_rate = flow_rate[:len(freq)]

        return freq, flow_rate
    
    def get_piston_position_and_velocity_data(self, tdc=None, domain="time") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        _, x = self.recip_x(tdc=tdc)
        v = self.recip_v(tdc=tdc)
        Trev = 60 / self.rpm
        N = len(x)

        if domain == "time":
            x_data = np.linspace(0, Trev, N)

        else:
            x_data = np.linspace(0, 360, N)

        return x_data, x, v

    def get_PV_diagram_head_end_data(self) -> tuple[np.ndarray, np.ndarray]:
        volume_HE, pressure_HE_Pa, _ = self.process_head_end_volumes_and_pressures()
        if volume_HE is None:
            return None, None

        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", self.pressure_unit)

        return volume_HE, pressure_HE

    def get_PV_diagram_crank_end_data(self) -> tuple[np.ndarray, np.ndarray]:
        volume_CE, pressure_CE_Pa, _ = self.process_crank_end_volumes_and_pressures()
        if volume_CE is None:
            return None, None

        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", self.pressure_unit)

        return volume_CE, pressure_CE

    def get_volumetric_flow_rate_at_suction_time_data(self) -> tuple[np.ndarray, np.ndarray]:
        flow_rate = self.process_sum_of_volumetric_flow_rate("in_flow")
        if flow_rate is None:
            return None, None

        Trev = 60 / self.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)

        return time, flow_rate

    def get_volumetric_flow_rate_at_discharge_time_data(self) -> tuple[np.ndarray, np.ndarray]:
        flow_rate = self.process_sum_of_volumetric_flow_rate("out_flow")
        if flow_rate is None:
            return None, None

        Trev = 60 / self.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)

        return time, flow_rate

    def get_rod_pressure_load_time_data(self) -> tuple[np.ndarray, np.ndarray]:
        _, pressure_HE_Pa, _ = self.process_head_end_volumes_and_pressures()
        _, pressure_CE_Pa, _ = self.process_crank_end_volumes_and_pressures()

        load_head = pressure_HE_Pa * self.area_head_end
        load_crank = -pressure_CE_Pa * self.area_crank_end

        # convert the calculated force in kN
        rod_pressure_load = (load_head + load_crank) / 1000

        Trev = 60 / self.rpm
        N = len(rod_pressure_load)
        time = np.linspace(0, Trev, N)

        return time, rod_pressure_load

    def get_rod_pressure_load_frequency_data(self, revolutions: int) -> tuple[np.ndarray, np.ndarray]:
        _, rod_pressure_load_time = self.get_rod_pressure_load_time_data()

        freq, rod_pressure_load = self.process_FFT_of_(rod_pressure_load_time, revolutions)
        mask = freq <= self.max_frequency

        return freq[mask], rod_pressure_load[mask]

    def get_volumetric_flow_rate_at_suction_frequency_data(self, revolutions: int) -> tuple[np.ndarray, np.ndarray]:
        return self.process_FFT_of_volumetric_flow_rate(revolutions, "in_flow")

    def get_volumetric_flow_rate_at_discharge_frequency_data(self, revolutions: int) -> tuple[np.ndarray, np.ndarray]:
        return self.process_FFT_of_volumetric_flow_rate(revolutions, "out_flow")

    def get_pressure_head_end_angle_data(self) -> tuple[np.ndarray, np.ndarray]:
        _, pressure_HE_Pa, _ = self.process_head_end_volumes_and_pressures()

        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", self.pressure_unit)

        N = len(pressure_HE)
        angle = np.linspace(0, 360, N)

        return angle, pressure_HE

    def get_volume_head_end_angle_data(self) -> tuple[np.ndarray, np.ndarray]:
        volume_HE, _, _ = self.process_head_end_volumes_and_pressures()

        N = len(volume_HE)
        angle = np.linspace(0, 360, N)

        return angle, volume_HE

    def get_pressure_crank_end_angle_data(self) -> tuple[np.ndarray, np.ndarray]:
        _, pressure_CE_Pa, _ = self.process_crank_end_volumes_and_pressures()

        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", self.pressure_unit)

        N = len(pressure_CE)
        angle = np.linspace(0, 360, N)

        return angle, pressure_CE

    def get_volume_crank_end_angle_data(self) -> tuple[np.ndarray, np.ndarray]:
        volume_CE, _, _ = self.process_crank_end_volumes_and_pressures()

        N = len(volume_CE)
        angle = np.linspace(0, 360, N)

        return angle, volume_CE

    def plot_PV_diagram_both_ends(self):

        volume_HE, pressure_HE = self.get_PV_diagram_head_end_data()
        volume_CE, pressure_CE = self.get_PV_diagram_crank_end_data()

        if volume_HE is None:
            return

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V RECIPROCATING COMPRESSOR DIAGRAM"

        volumes = [volume_HE, volume_CE]
        pressures = [pressure_HE, pressure_CE]
        labels = ["Head End", "Crank End"]
        colors = [(1,0,0), (0,0,1)]
        linestyles = ["-", "--"]

        plot2(volumes, pressures, x_label, y_label, title, labels, colors, linestyles)

    def plot_PV_diagram_head_end(self):

        volume_HE, pressure_HE = self.get_PV_diagram_head_end_data()
        if volume_HE is None:
            return

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V diagram (head-end)"

        plot(volume_HE, pressure_HE, x_label, y_label, title)

    def plot_PV_diagram_crank_end(self):

        volume_CE, pressure_CE = self.get_PV_diagram_crank_end_data()
        if volume_CE is None:
            return

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V diagram (crank-end)"

        plot(volume_CE, pressure_CE, x_label, y_label, title)

    def plot_pressure_vs_time(self):

        _, pressure_HE_Pa, _ = self.process_head_end_volumes_and_pressures()
        _, pressure_CE_Pa, _ = self.process_crank_end_volumes_and_pressures()
        
        if pressure_HE_Pa is None:
            return

        Trev = 60 / self.rpm
        N = len(pressure_HE_Pa)
        time = np.linspace(0, Trev, N)

        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", self.pressure_unit)
        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", self.pressure_unit)

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

        Trev = 60 / self.rpm
        N = len(volume_HE)

        time = np.linspace(0, Trev, N)

        x_label = "Time [s]"
        y_label = "Volume [m³]"
        x_data = [time, time]
        y_data = [volume_HE, volume_CE]
        labels = ["Head End", "Crank End"]
        title = "PRESSURES vs TIME PLOT"
        colors = [(1,0,0),(0,0,1)]
        linestyles = ["-","--"]

        plot2(x_data, y_data, x_label, y_label, title, labels, colors, linestyles)

    def plot_volumetric_flow_rate_at_suction_time(self):

        time, flow_rate = self.get_volumetric_flow_rate_at_suction_time_data()
        if flow_rate is None:
            return

        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at suction"

        plot(time, flow_rate, x_label, y_label, title)


    def plot_volumetric_flow_rate_at_discharge_time(self):

        time, flow_rate = self.get_volumetric_flow_rate_at_discharge_time_data()
        if flow_rate is None:
            return

        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at discharge"

        plot(time, flow_rate, x_label, y_label, title)

    def plot_rod_pressure_load_frequency(self, revolutions):

        freq, rod_pressure_load = self.get_rod_pressure_load_frequency_data(revolutions)

        x_label = "Frequency [Hz]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"

        plot(freq, rod_pressure_load, x_label, y_label, title, _absolute=True)

    def plot_rod_pressure_load_time(self):

        time, rod_pressure_load_time = self.get_rod_pressure_load_time_data()

        x_label = "Time [s]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"

        plot(time, rod_pressure_load_time, x_label, y_label, title, _absolute=True)


    def plot_piston_position_and_velocity(self, tdc=None, domain="time"):

        x_data, x, v = self.get_piston_position_and_velocity_data()

        if domain == "time":
            x_label = "Time [s]"

        else:
            x_label = "Angle [deg]"

        data = dict()
        data["Piston position"] = { 
            "axis" : "left",
            "x_data" : x_data,
            "y_data" : x,
            "x_label" : x_label,
            "y_label" : "Piston relative displacement [m]",
            "legend_label" : "Piston position",
            "color" : [0,0,0],
            "linestyle" : "-",
            "linewidth" : 2,
            "y_axis_absolute" : False,
            }

        data["Piston velocity"] = { 
            "axis" : "right",
            "x_data" : x_data,
            "y_data" : v,
            "x_label" : x_label,
            "y_label" : "Piston velocity [m/s]",
            "legend_label" : "Piston velocity",
            "color" : [0,0,1],
            "linestyle" : "-",
            "linewidth" : 2,
            "y_axis_absolute" : False,
            }

        title = "Piston displacement and velocity during a complete cycle"

        plot_2_yaxis(data, title)

    def plot_volumetric_flow_rate_at_suction_frequency(self, revolutions):

        freq, flow_rate = self.get_volumetric_flow_rate_at_suction_frequency_data(revolutions)
        if flow_rate is None:
            return

        x_label = "Frequency [Hz]"
        y_label = "Volumetric head flow rate [m³/s]"
        title = "Volumetric flow rate at suction"

        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)

    def plot_volumetric_flow_rate_at_discharge_frequency(self, revolutions):

        freq, flow_rate = self.get_volumetric_flow_rate_at_discharge_frequency_data(revolutions)
        if flow_rate is None:
            return

        x_label = "Frequency [Hz]"
        y_label = "Volumetric crank flow rate [m³/s]"
        title = "Volumetric flow rate at discharge"

        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)

    def plot_head_end_pressure_vs_angle(self):

        angle, pressure_HE = self.get_pressure_head_end_angle_data()

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Head end pressure vs Angle"

        plot(angle, pressure_HE, x_label, y_label, title)

    def plot_head_end_volume_vs_angle(self):

        angle, volume_HE = self.get_volume_head_end_angle_data()

        x_label = "Crank angle [degree]"
        y_label = "Volume [m³]"
        title = "Head end volume vs Angle"

        plot(angle, volume_HE, x_label, y_label, title)

    def plot_crank_end_pressure_vs_angle(self):

        angle, pressure_CE = self.get_pressure_crank_end_angle_data()

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Crank end pressure vs Angle"

        plot(angle, pressure_CE, x_label, y_label, title)

    def plot_crank_end_volume_vs_angle(self):

        angle, volume_CE = self.get_volume_crank_end_angle_data()

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


def plt():
    '''
    Matplotlib imports usually take a long time to run.
    This is a trick to only import plt when it actually
    need to be used.
    The only difference is that now you need to call plt like a function
    like `plt().plot([1,2,3])` instead of `plt.plot([1,2,3])`
    '''
    import matplotlib.pyplot
    return matplotlib.pyplot

def plot(x, y, x_label, y_label, title, label="", _absolute=False):

    plt().ion()

    fig = plt().figure(figsize=[10, 6])
    ax_ = fig.add_subplot(1,1,1)

    if _absolute:
        y = np.abs(y)

    ax_.plot(x, y, color=[0,0,1], linewidth = 1, label = label)

    ax_.set_xlabel(x_label, fontsize = 11)#, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11)#, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12)#, fontweight = 'bold')

    plt().grid()
    plt().show() 

def plot2(x, y, x_label, y_label, title, labels, colors, linestyles):

    plt().ion()

    fig = plt().figure(figsize=[10, 6])
    ax_ = fig.add_subplot(1,1,1)

    for i, label in enumerate(labels): 
        ax_.plot(x[i], y[i], color=colors[i], linewidth=1, linestyle=linestyles[i], label=label)

    ax_.set_xlabel(x_label, fontsize = 11)#, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11)#, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12)#, fontweight = 'bold')

    plt().legend()
    plt().grid()
    plt().show() 

def plot_2_yaxis(data_to_plot, title):

    plt().ion()

    fig = plt().figure(figsize=[10, 6])
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

            ax_1.set_xlabel(x_label, fontsize = 11)#, fontweight = 'bold')

            plots = list()
            legends = list()

            if axis_ == "left":
                plot_1, = ax_1.plot(x_data, y_data, color=color, linewidth=linewidth, linestyle=linestyle, label=legend_label)
                ax_1.set_ylabel(y_label, fontsize = 11)#, fontweight = 'bold')
                plots.append(plot_1)
                legends.append(legend_label)

            else:
                plot_2, = ax_2.plot(x_data, y_data, color=color, linewidth=linewidth, linestyle=linestyle, label=legend_label)
                ax_2.set_ylabel(y_label, fontsize = 11)#, fontweight = 'bold')
                plots.append(plot_2)
                legends.append(legend_label)

        ax_1.set_title(title, fontsize = 12, fontweight = 'bold')
        ax_1.grid()
        ax_2.grid()
        fig.legend(bbox_to_anchor=(1,1), bbox_transform=ax_1.transAxes)
        plt().show()


if __name__ == "__main__":

    parameters = {  
        'acting_label' : CylindersActingMode.BOTH_ENDS,
        'number_of_cylinders' : 1,
        'bore_diameter' : 0.780,
        'stroke' : 0.33,
        'connecting_rod_length' : 1.25,
        'rod_diameter' : 0.135,
        'pressure_ratio' : 1.90788804,
        'clearance_HE' : 15.8,
        'clearance_CE' : 18.39,
        'tdc_crank_angle_1' : 0,
        'rotational_speed' : 360,
        'capacity' : 100,
        'suction_pressure' : 19.65,
        'suction_temperature' : 45,
        'pressure_unit' : "bar (g)",
        'temperature_unit' : "°C",
        'isentropic_exponent' : 1.400,
        'molar_mass' : 2.01568,
        'number_points' : 1000,
        }

    compressor = ReciprocatingCompressorModel(**parameters)
    compressor.process_remaining_fluid_properties()

    rho_suc = compressor.rho_suc
    # compressor.plot_rod_pressure_load_frequency(6)
    # compressor.plot_PV_diagram_head_end()
    # compressor.plot_PV_diagram_crank_end()
    compressor.plot_PV_diagram_both_ends()

    compressor.plot_volumetric_flow_rate_at_suction_time()
    compressor.plot_volumetric_flow_rate_at_discharge_time()

    # mass_in = compressor.get_in_mass_flow()
    # mass_out = compressor.get_out_mass_flow()
    # total_mass = compressor.total_mass_flow()
    # print(mass_in, mass_out, 200*(mass_in-mass_out)/(mass_in+mass_out))
    # print(total_mass)

    # cap = 80
    # res_cap = compressor.process_capacity(capacity = cap/100)
    # print(res_cap)

    # mass_flow_full_capacity = -np.mean(compressor.process_sum_of_volumetric_flow_rate('in_flow', capacity=1))*rho_suc
    # partial_flow = -np.mean(compressor.process_sum_of_volumetric_flow_rate('in_flow', capacity=res_cap))*rho_suc
    # print((partial_flow/mass_flow_full_capacity) * 100)