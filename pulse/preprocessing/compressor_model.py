import numpy as np
from matplotlib import pyplot as plt

kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5

def offset_to_tdc(input_array, tdc):

    while tdc < 0:
        tdc += 2*np.pi

    N = len(input_array)
    output_array = np.zeros(N)
    i_tdc = round(tdc/(2*np.pi/(N-1)))
    output_array[i_tdc:] = input_array[0:N-i_tdc]
    output_array[0:i_tdc] = input_array[N-i_tdc:]

    return output_array

def plot(x, y, x_label, y_label, title, label="", _absolute=False):

    plt.ion()

    fig = plt.figure(figsize=[8,6])
    ax_ = fig.add_subplot(1,1,1)

    if _absolute:
        y = np.abs(y)

    ax_.plot(x, y, color=[1,0,0], linewidth = 2, label = label)
    ax_.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12, fontweight = 'bold')
    plt.grid()
    plt.show() 

def plot_2_yaxis(data_to_plot, title):

    plt.ion()
    fig = plt.figure(figsize=[8,6])
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
        # ax_1.legend()
        # ax_2.legend()
        # plt.legend(plots, legends, labelcolor="linecolor")
        plt.show() 

class CompressorModel:

    '''
    COMPRESSOR MODEL                                     

    This class contains a simplified reciprocating compressor model for calculating
    the excitation to the acoustic FE model. The main output data is the volumetric 
    flow in m³/s units which is dealt as an equivalent acoustic volume velocity source.

    Assumptions:

    1) Stead flow;
    2) Ideal gas behaviour;
    3) Compression and expansion cycles are isentropic processes;
    4) The suction and discharge pressures remains constant during suction and discharge cycles, respectively;
    5) No heat exchange in suction and discharge cycles; 

    '''

    def __init__( self, parameters, **kwargs):

        self._load_compressor_parameters(parameters)
        self.number_points = kwargs.get('number_points', 1000)
        self.max_frequency = kwargs.get('max_frequency', 250)
        self.number_of_cylinders = kwargs.get('number_of_cylinders', 1)


    def _load_compressor_parameters(self, parameters):
        """
        """

        # self.D = bore_diameter
        # self.r = stroke/2
        # self.L = rod_length
        # self.rod_diam = rod_diameter
        # self.p_ratio = pressure_ratio
        # self.c = clearance/100
        # self.tdc1 = TDC_crank_angle_1*np.pi/180
        # self.rpm = rotational_speed
        # self.capacity = capacity/100     

        self.D = parameters['bore diameter']                    # Cylinder bore diameter [m]
        self.r = parameters['stroke']/2                         # Connecting rod length [m]
        self.L = parameters['connecting rod length']            # Length of compressor full stroke [m]
        self.rod_diam = parameters['rod diameter']              # Rod diameter [m]
        self.p_ratio = parameters['pressure ratio']             # Compressor pressure ratio Pd/Ps
        self.c_HE = parameters['clearance (HE)']/100            # Clearance volume as percentage of full volume (%)
        self.c_CE = parameters['clearance (CE)']/100            # Clearance volume as percentage of full volume (%)
        self.tdc1 = parameters['TDC crank angle 1']*np.pi/180   # Crank angle (degrees) at which piston is at top dead center
        self.rpm = parameters['rotational speed']               # Compressor rotation speed (rpm)
        self.capacity = parameters['capacity']/100              # Capacity of compression stage (%)
        self.acting_label = parameters['acting label']          # Active cylinder(s) key (int)

        if self.acting_label == 0:
            self.active_cylinder = 'both ends'
        elif self.acting_label == 1:
            self.active_cylinder = 'head end'
        elif self.acting_label == 2:
            self.active_cylinder = 'crank end'

        pressure_at_suction = parameters['pressure at suction']         # Pressure at suction
        temperature_at_suction = parameters['temperature at suction']   # Temperature at suction
        self.pressure_unit = parameters['pressure unit']                     # Pressure unit
        self.temperature_unit = parameters['temperature unit']               # Temperature unit

        if self.pressure_unit == "kgf/cm²":
            self.p_suc = pressure_at_suction*kgf_cm2_to_Pa
        else:
            self.p_suc = pressure_at_suction*bar_to_Pa
        
        if self.temperature_unit == "°C":
            self.T_suc = temperature_at_suction + 273.15
        else:
            self.T_suc = temperature_at_suction

        self.area_head_end = np.pi*(self.D**2)/4
        self.area_crank_end = np.pi*((self.D**2)-(self.rod_diam**2))/4
        self.tdc2 = np.pi/2
        self.cap = None

        self.set_fluid_properties_and_update_state(parameters['isentropic exponent'],
                                                   parameters['molar mass'])


    def set_fluid_properties_and_update_state(self, isentropic_exponent, molar_mass):
        """ 
            This method sets the process fluid properties and updates the thermodynamic 
            fluid properties for suction and discharge states.

        Parameters:
        -----------
        isentropic_exponent: float number
        molar_mass: a float number in kg/kmol units.
        
        """

        self.k = isentropic_exponent            # Compressed gas isentropic exponent
        self.molar_mass = molar_mass            # Molar mass [kg/kmol]

        self.vr = (self.p_suc)**(-1/self.k)     # Volume ratio considering isentropic compression
        self.Ru = 8314.4621                     # Universal ideal gas constant [J/kmol.K]
        self.R = self.Ru/self.molar_mass        # Gas constant [J/kg.K]
        self.rho_suc = self.p_suc/(self.R*self.T_suc)

        self.T_disc = (self.T_suc)*(self.p_ratio**((self.k-1)/self.k))
        self.rho_disc = (self.p_suc*self.p_ratio)/(self.R*self.T_disc)

        # print(self.k, self.molar_mass, self.R, self.rho_suc)
        # print(self.T_disc, self.rho_disc)

    def recip_v(self, tdc=None):
        N = self.number_points + 1
        if tdc == None:
            tdc = self.tdc1
        r = self.r
        l = self.L
        t = np.linspace(0, 2*np.pi, N)
        v = -(r * np.sin(t-tdc) + (r**2*np.sin(t-tdc)*np.cos(t-tdc))/np.sqrt(l**2 - r**2*np.sin(t-tdc)**2))
        v = v * self.rpm*(2*np.pi/60)
        return v

    def recip_x(self, tdc=None):
        N = self.number_points + 1
        if tdc == None:
            tdc = self.tdc1
        r = self.r
        l = self.L
        t = np.linspace(0, 2*np.pi, N)
        # self.theta = t
        # x_mean = np.sqrt(l**2 - r**2)
        x_max = l + r
        x = (r * np.cos(t-tdc) + np.sqrt(l**2 - r**2*np.sin(t-tdc)**2)) - x_max
        return x 

    def p_head_end( self,
                    label = "HE",
                    tdc=None, 
                    capacity=None, 
                    full_output=False, 
                    plot_pv=False, 
                    aux_process=False):

        N = self.number_points + 1
        ang = np.linspace(0, 2*np.pi, N)

        if tdc is None:
            tdc = self.tdc1
                
        if capacity is None:
            if self.cap is None:
                self.cap = self.process_capacity(capacity = self.capacity)
            capacity = self.cap

        open_suc = [False]*N
        open_disch = [False]*N

        if self.active_cylinder not in ['head end', 'both ends'] and not aux_process and not plot_pv:
            p = np.zeros(N) 
            print('Cylinder does not have head end pressure.')
        else:
            x = self.recip_x(tdc=0)
            p, vol = [], []
            p0 = self.p_ratio
            p_aux = p0

            if label == "HE":
                l0 = self.c_HE*(2*self.r) # clearance height head end
            elif label == "CE":
                l0 = self.c_CE*(2*self.r) # clearance height crank end
            else:
                l0 = ((self.c_HE+self.c_CE)/2)*(2*self.r) # average clearance height

            i = 0
            #EXPANSION CYCLE
            while p_aux > 1 and i < N:
                p_aux = p0*(l0 / (l0 + (x[0] - x[i])))**self.k
                if p_aux < 1:
                    p_aux = 1
                    open_suc[i] = True
                p.append(p_aux*self.p_suc)
                vol.append(self.area_head_end*(l0 + (x[0] - x[i])))
                i += 1

            if i < N:
                #SUCTION CYCLE
                while i <= (N-1)/2:
                    p.append(1*self.p_suc)
                    vol.append(self.area_head_end*(l0 + (x[0] - x[i])))
                    open_suc[i] = True
                    i += 1

                #COMPRESSION CYCLE
                p0 = 1
                i0 = i
                while p_aux < self.p_ratio and i < N:
                    vol.append(self.area_head_end*(l0 + (x[0] - x[i])))
                    if (2*np.pi-ang[i])/np.pi > capacity:
                        p_aux = 1
                        open_suc[i] = True
                        i0 = i
                    else:
                        p_aux = p0*((l0 + x[0] - x[i0])/(l0 + (x[0] - x[i])))**self.k
                    if p_aux > self.p_ratio:
                        p_aux = self.p_ratio
                        open_disch[i] = True
                    i += 1
                    p.append(p_aux*self.p_suc)

                #DISCHARGE CYCLE
                while i < N:
                    p.append(self.p_ratio*self.p_suc)
                    vol.append(self.area_head_end*(l0 + (x[0] - x[i])))
                    open_disch[i] = True
                    i += 1

        p = offset_to_tdc(p, tdc)
        vol = offset_to_tdc(vol, tdc)
        open_suc = offset_to_tdc(open_suc, tdc)
        open_disch = offset_to_tdc(open_disch, tdc)
     
        if plot_pv:
            return vol, p
        elif full_output:
            return p, open_suc, open_disch
        else:
            return p

    def p_crank_end(self, 
                    tdc=None, 
                    capacity=None, 
                    full_output=False, 
                    plot_pv=False):

        if tdc == None:
            tdc = self.tdc1

        if self.active_cylinder not in ['crank end', 'both ends']:
            print('Cylinder does not have crank end pressure.')

        if plot_pv:
            vol, pressure = self.p_head_end(label = "CE",
                                            tdc = tdc - np.pi, 
                                            capacity = capacity,
                                            full_output = full_output, 
                                            plot_pv = plot_pv)
            vol = list(np.array(vol)*(self.D**2 - self.rod_diam**2)/self.D**2)
            return vol, pressure
        else:
            pressure = self.p_head_end(tdc = tdc - np.pi, 
                                       capacity = capacity, 
                                       full_output = full_output, 
                                       plot_pv = plot_pv)
            return pressure

    def flow_head_end(self, tdc=None, capacity=None, aux_process=False):

        N = self.number_points

        if tdc == None:
            tdc = self.tdc1

        if self.active_cylinder not in ['head end', 'both ends'] and not aux_process:
            print('Cylinder does not have head end pressure.')
            return { 'in_flow': np.zeros(N+1),
                     'out_flow': np.zeros(N+1) }
        else:
            _, open_suc, open_disch = self.p_head_end(  tdc=0, 
                                                        capacity=capacity, 
                                                        full_output=True, 
                                                        aux_process=aux_process  )

            vel = self.recip_v(tdc=None)
            flow_in = np.zeros(N+1)
            flow_out = np.zeros(N+1)

            for i, v in enumerate(vel):
                if open_suc[i]:
                    flow_in[i] = v*(np.pi*self.D**2/4)
                if open_disch[i]:
                    flow_out[i] = v*(np.pi*self.D**2/4)

            flow_in = offset_to_tdc(flow_in, tdc)
            flow_out = offset_to_tdc(flow_out, tdc)
            
            return { 'in_flow': flow_in,
                     'out_flow': flow_out }

    def flow_crank_end(self, tdc=None, capacity=None):

        N = self.number_points

        if tdc is None:
            tdc = self.tdc1

        if self.active_cylinder not in ['crank end', 'both ends']:
            print('Cylinder does not have crank end pressure.')
            return { 'in_flow': np.zeros(N+1),
                     'out_flow': np.zeros(N+1) }
        else:
            aux_dict = self.flow_head_end(tdc=(tdc-np.pi), capacity=capacity, aux_process=True)
            flow_in = aux_dict['in_flow'] * (self.D**2 - self.rod_diam**2)/self.D**2
            flow_out = aux_dict['out_flow'] * (self.D**2 - self.rod_diam**2)/self.D**2
            return { 'in_flow': flow_in,
                     'out_flow': flow_out }

    def mass_flow_crank_end(self, tdc=None, capacity=None):
        vf = self.flow_crank_end(tdc=tdc, capacity=capacity)
        mf = -vf['in_flow']*self.rho_suc
        return mf

    def mass_flow_head_end(self, tdc=None, capacity=None):
        vf = self.flow_head_end(tdc=tdc, aux_process=True, capacity=capacity)
        mf = -vf['in_flow']*self.rho_suc
        return mf
    
    def total_mass_flow(self):
        N = self.number_points
        f_he = np.sum(self.mass_flow_head_end())/N
        f_ce = np.sum(self.mass_flow_crank_end())/N
        return f_he + f_ce

    def process_sum_of_volumetric_flow_rate(self, key, capacity=None):

        if self.active_cylinder == 'both ends':

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_crank_end(tdc=self.tdc1, capacity=capacity)[key]
                flow_rate += self.flow_head_end(tdc=self.tdc1, capacity=capacity)[key]
            else:
                flow_rate = self.flow_crank_end(tdc=self.tdc1, capacity=capacity)[key] 
                flow_rate += self.flow_head_end(tdc=self.tdc1, capacity=capacity)[key]
                flow_rate += self.flow_crank_end(tdc=self.tdc2, capacity=capacity)[key] 
                flow_rate += self.flow_head_end(tdc=self.tdc2, capacity=capacity)[key]

        elif self.active_cylinder == 'head end':

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_head_end(tdc=self.tdc1, capacity=capacity)[key]
            else:
                flow_rate = self.flow_head_end(tdc=self.tdc1, capacity=capacity)[key]
                flow_rate += self.flow_head_end(tdc=self.tdc2, capacity=capacity)[key]

        elif self.active_cylinder == 'crank end':

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_crank_end(tdc=self.tdc1, capacity=capacity)[key]
            else:
                flow_rate = self.flow_crank_end(tdc=self.tdc1, capacity=capacity)[key]
                flow_rate += self.flow_crank_end(tdc=self.tdc2, capacity=capacity)[key]

        return flow_rate

    def get_in_mass_flow(self, capacity=None):
        return -np.mean(self.process_sum_of_volumetric_flow_rate('in_flow', capacity=capacity))*self.rho_suc

    def get_out_mass_flow(self, capacity=None):
        return np.mean(self.process_sum_of_volumetric_flow_rate('out_flow', capacity=capacity))*self.rho_disc

    def get_nearest_capacity(self, list_caps, nearest_absolute=True):
        values = np.array([self.get_in_mass_flow(capacity=_cap) for _cap in list_caps])
        if nearest_absolute:
            indexes = np.argsort(np.abs(values - self.final_mass_flow))
        else:
            indexes = np.argsort(values - np.min(values))
        output = np.array(list_caps)[indexes]
        return output[0]

    def process_capacity(self, capacity=1):
        cap_aux, mass_flow_aux, ratio, iterations = [], [], [], []
        
        if capacity < 0.005 or capacity > 1: # capacity >= 0.5% and <=100%
            return -1

        mass_flow_full_capacity = self.get_in_mass_flow(capacity=1)

        if capacity == 1:
            return capacity
        else:
            self.final_mass_flow = capacity*mass_flow_full_capacity

            cap_aux.append(capacity)
            stable = False
            _interp = False
            self.flag_max_iter = True
            max_iter = 100
            i = 0

            while stable == False and i != max_iter: 
                
                iter_flow = self.get_in_mass_flow(capacity=cap_aux[i])

                while iter_flow < 0: # temporary structure due to a negative flow rate at small capacities
                    cap_aux[i] *= 2
                    iter_flow = self.get_in_mass_flow(capacity=cap_aux[i])
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
                    if ratio[i-1]==ratio[i-2]: # promote the linear average if ratio does not change in 3 iterations
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

    def process_FFT_of_volumetric_flow_rate(self, revolutions, key):
        flow_rate = self.process_sum_of_volumetric_flow_rate(key)
        freq, flow_rate = self.process_FFT_of_(flow_rate, revolutions)
        freq = freq[freq <= self.max_frequency]
        flow_rate = flow_rate[:len(freq)]
        return freq, flow_rate

    def plot_PV_diagram_head_end(self, plot_pv=True):
        vol, pressure = self.p_head_end(plot_pv=plot_pv)

        if self.pressure_unit == "kgf/cm²":
            pressure /= kgf_cm2_to_Pa
        else:
            pressure /= bar_to_Pa

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V RECIPROCATING COMPRESSOR DIAGRAM"
        plot(vol, pressure, x_label, y_label, title)

    def plot_PV_diagram_crank_end(self, plot_pv=True):
        vol, pressure = self.p_crank_end(plot_pv=plot_pv)

        if self.pressure_unit == "kgf/cm²":
            pressure /= kgf_cm2_to_Pa
        else:
            pressure /= bar_to_Pa

        x_label = "Volume [m³]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "P-V RECIPROCATING COMPRESSOR DIAGRAM"
        plot(vol, pressure, x_label, y_label, title)

    def plot_pressure_vs_time(self):
        _, pressure = self.p_head_end(plot_pv=True)
        Trev = 60/self.rpm
        N = len(pressure)
        time = np.linspace(0, Trev, N)
        x_label = "Time [s]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "PRESSURE vs TIME PLOT"
        plot(time, pressure, x_label, y_label, title)

    def plot_volume_vs_time(self):
        volume, _ = self.p_head_end(plot_pv=True)
        Trev = 60/self.rpm
        N = len(volume)
        time = np.linspace(0, Trev, N)
        x_label = "Time [s]"
        y_label = "Volume [m³]"
        title = "Volume vs Time"
        plot(time, volume, x_label, y_label, title)

    def plot_volumetric_flow_rate_at_suction_time(self):
        flow_rate = self.process_sum_of_volumetric_flow_rate('in_flow')
        Trev = 60/self.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)
        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at suction"
        plot(time, flow_rate, x_label, y_label, title)

    def plot_volumetric_flow_rate_at_discharge_time(self):
        flow_rate = self.process_sum_of_volumetric_flow_rate('out_flow')
        Trev = 60/self.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)
        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "Volumetric flow rate at discharge"
        plot(time, flow_rate, x_label, y_label, title)
    
    def plot_rod_pressure_load_frequency(self, revolutions):
        pressure_head = self.p_head_end()
        pressure_crank = self.p_crank_end()

        rod_pressure_load_time = (pressure_head*(self.D**2) - pressure_crank*((self.D**2) - (self.rod_diam**2)))*(np.pi/4)

        freq, rod_pressure_load = self.process_FFT_of_(rod_pressure_load_time, revolutions)
        freq = freq[freq <= self.max_frequency]
        rod_pressure_load = rod_pressure_load[:len(freq)]/1000

        x_label = "Frequency [Hz]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"
        plot(freq, rod_pressure_load, x_label, y_label, title, _absolute=True)  

    def plot_rod_pressure_load_time(self, revolutions):
        pressure_head = self.p_head_end()
        pressure_crank = self.p_crank_end()
        load_head = (pressure_head*(self.D**2))*(np.pi/4)
        load_crank = -(pressure_crank*((self.D**2) - (self.rod_diam**2)))*(np.pi/4)
        rod_pressure_load_time = (load_head + load_crank)/1000
        Trev = 60/self.rpm
        N = len(rod_pressure_load_time)
        time = np.linspace(0, Trev, N)
        x_label = "Time [s]"
        y_label = "Rod pressure load [kN]"
        title = "Rod pressure load"
        plot(time, rod_pressure_load_time, x_label, y_label, title, _absolute=True) 

    def plot_piston_position_and_velocity(self, domain="time"):
        x = self.recip_x(tdc=None)
        v = self.recip_v(tdc=None)
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
        x_label = "Frequency [Hz]"
        y_label = "Volumetric head flow rate [m³/s]"
        title = "Volumetric flow rate at suction"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)  

    def plot_volumetric_flow_rate_at_discharge_frequency(self, revolutions):
        freq, flow_rate = self.process_FFT_of_volumetric_flow_rate(revolutions, 'out_flow')
        x_label = "Frequency [Hz]"
        y_label = "Volumetric crank flow rate [m³/s]"
        title = "Volumetric flow rate at discharge"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)  

    def plot_head_end_pressure_vs_angle(self):
        N = self.number_points
        _, pressure = self.p_head_end(plot_pv=True)

        if self.pressure_unit == "kgf/cm²":
            pressure /= kgf_cm2_to_Pa
        else:
            pressure /= bar_to_Pa

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Head end pressure vs Angle"
        plot(angle, pressure, x_label, y_label, title)

    def plot_head_end_volume_vs_angle(self):
        N = self.number_points
        volume, _ = self.p_head_end(plot_pv=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Crank angle [degree]"
        y_label = "Volume [m³]"
        title = "Head end volume vs Angle"
        plot(angle, volume, x_label, y_label, title)

    def plot_crank_end_pressure_vs_angle(self):
        N = self.number_points
        _, pressure = self.p_crank_end(plot_pv=True)

        if self.pressure_unit == "kgf/cm²":
            pressure /= kgf_cm2_to_Pa
        else:
            pressure /= bar_to_Pa

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Crank angle [degree]"
        y_label = f"Pressure [{self.pressure_unit}]"
        title = "Crank end pressure vs Angle"
        plot(angle, pressure, x_label, y_label, title)

    def plot_crank_end_volume_vs_angle(self):
        N = self.number_points
        volume, _ = self.p_crank_end(plot_pv=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Crank angle [degree]"
        y_label = "Volume [m³]"
        title = "Crank end volume vs Angle"
        plot(angle, volume, x_label, y_label, title)

    def plot_convergence(self, x, y):
        x_label = "Iteration"
        y_label = "Ratio"
        title = "Convergence plot"
        plot(x, y, x_label, y_label, title)


if __name__ == "__main__":

    cap = 90

    parameters = [  1,              # Cylinder bore diameter [m]
                    0.3,            # Length of compressor full stroke [m]
                    0.8,            # Connecting rod length [m]
                    0.2,            # Rod diameter [m]
                    1.9,            # Compressor pressure ratio Pd/Ps
                    6,              # Clearance volume as percentage of full volume (%)
                    0,              # Crank angle (degrees) at which piston is at top dead center
                    360,            # Compressor rotation speed (rpm)
                    cap,             # Capacity of compression stage (%)
                    19,             # Pressure at suction [kgf/cm²]
                    45,             # Temperature at suction [°C]
                    True ]          # Compressor is double effect (bool)
    
    cylinder = CompressorModel(parameters)
    cylinder.number_of_cylinders = 1
    cylinder.number_points = 2000
    cylinder.set_fluid_properties_and_update_state(1.4, 2.01568)
    rho_suc = cylinder.rho_suc
    # cylinder.plot_rod_pressure_load_frequency(6)
    # cylinder.plot_PV_diagram_head_end()

    # mass_in = cylinder.get_in_mass_flow()
    # mass_out = cylinder.get_out_mass_flow()
    # total_mass = cylinder.total_mass_flow()
    # print(mass_in, mass_out, 200*(mass_in-mass_out)/(mass_in+mass_out))
    # print(total_mass)

    # cap = cap/100
    # res_cap = cylinder.process_capacity(capacity=cap)
    # print(res_cap)

    # mass_flow_full_capacity = -np.mean(cylinder.process_sum_of_volumetric_flow_rate('in_flow', capacity=1))*rho_suc
    # partial_flow = -np.mean(cylinder.process_sum_of_volumetric_flow_rate('in_flow', capacity=res_cap))*rho_suc
    # print((partial_flow/mass_flow_full_capacity)*100)