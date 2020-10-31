
import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt

def offset_to_tdc(array, tdc):

    while tdc < 0:
        tdc += 2*np.pi

    N = len(array)
    array2 = np.zeros(N)
    i_tdc = round(tdc/(2*np.pi/(N-1)))
    array2[i_tdc:] = array[0:N-i_tdc]
    array2[0:i_tdc] = array[N-i_tdc:]

    return array2

def plot(x, y, x_label, y_label, title, label="", _absolute=False):

    fig = plt.figure(figsize=[12,7])
    ax_ = fig.add_subplot(1,1,1)
    if _absolute:
        y = np.abs(y)
    ax_.plot(x, y, color=[1,0,0], linewidth=2, label=label)
    ax_.set_xlabel(x_label, fontsize = 14, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 14, fontweight = 'bold')
    ax_.set_title(title, fontsize=16, fontweight = 'bold')
    plt.grid()
    plt.show() 

class CompressorModel:

    def __init__( self, parameters, **kwargs):

        [  bore_diameter,                      # Cylinder bore diameter [m]
           stroke,                             # Length of compressor full stroke [m]
           rod_lenght,                         # Connecting rod length [m]
           rod_diameter,                       # Rod diameter [m]
           pressure_ratio,                     # Compressor pressure ratio Pd/Ps
           clearance,                          # Clearance volume as percentage of full volume (%)
           TDC_crank_angle_1,                  # Crank angle (degrees) at which piston is at top dead center
           rotational_speed,                   # Compressor rotation speed (rpm)
           capactity,                          # Capacity of compression stage (%)
           isentropic_coefficient,             # Compressed gas isentropic exponent
           molar_mass,                         # Molar mass [kg/kmol]
           pressure_at_suction,                # Pressure at suction
           temperature_at_suction,             # Temperature at suction
           double_effect  ] = parameters       # Compressor is double effect (bool)

        if double_effect:
            self.active_cylinder = None
        else:                                  # Active cylinder (only if double effect = False): 'HEAD END' or 'CRANK END'
            self.active_cylinder = kwargs.get('acitve_cylinder', 'HEAD END')     

        self.D = bore_diameter
        self.r = stroke/2
        self.L = rod_lenght
        self.rod = rod_diameter
        self.pressure_ratio = pressure_ratio
        self.c = clearance/100
        self.tdc1 = TDC_crank_angle_1*np.pi/180
        self.rpm = rotational_speed
        self.k = isentropic_coefficient
        self.molar_mass = molar_mass
        self.pressure_at_suction = pressure_at_suction
        self.Ts = temperature_at_suction
        self.double_effect = double_effect
        
        self.area_head_end = np.pi*(bore_diameter**2)/4
        self.area_crank_end = np.pi*((bore_diameter**2)-(rod_diameter**2))/4
        self.vr = (self.pressure_at_suction)**(-1/self.k)       # Volume ratio considering isentropic compression

        self.Ru = 8314.4621                     # Universal ideal gas constant [J/kmol.K]
        self.R = self.Ru/self.molar_mass       # Gas constant [J/kg.K]

        self.number_points = kwargs.get('number_points', 0)
        self.max_frequency = kwargs.get('max_frequency', 250)
        self.compression_stage = kwargs.get('compression_stage', 1)
        self.number_of_cylinders = kwargs.get('number_of_cylinders', 1)
        self.tdc2 = kwargs.get('TDC_crank_angle_2', 90)*np.pi/180 

        self.poly_sig = np.poly1d(np.array([ 4.07662578e-12, -1.76845633e-09,  3.22571698e-07, -3.21443114e-05,
                                            1.90316519e-03, -6.81078403e-02,  1.42782751e+00, -1.53184727e+01,
                                            9.36732673e+01]))

        if capactity == 100:
            self.cap = 1
        elif capactity == 0:
            self.cap = 0
        elif capactity > 0 and capactity < 100:
            self.cap = self.poly_sig(capactity)/100
        else:
            self.cap = 1

    def cap_real(self):
        
        r = (float(self.cap)*100 - self.poly_sig).roots
        cap_real = np.real(r)[np.argmin([np.abs(np.imag(a)) for a in r])]
        if cap_real > 100:
            cap_real = 100
        elif cap_real < 0:
            cap_real = 0
    
        return cap_real #self.cap*100

    def update_interstages_parameters(self):
        self.pr = self.pressure_ratio**(1/3)
        if self.compression_stage == 1:
            self.ps = self.pressure_at_suction
        elif self.compression_stage == 2:
            self.ps = self.pressure_at_suction*self.pr
        elif self.compression_stage == 3:
            self.ps = self.pressure_at_suction*(self.pr**2)

    def recip_v(self, tdc=None):
        N = self.number_points + 1
        if tdc == None:
            tdc = self.tdc1
        r = self.r
        l = self.L
        t = np.linspace(0, 2*np.pi, N)
        v = -r * np.sin(t-tdc) - (r**2*np.sin(t-tdc)*np.cos(t-tdc))/np.sqrt(l**2 - r**2*np.sin(t-tdc)**2)
        v = v * self.rpm*(2*np.pi/60)
        return v

    def recip_x(self, tdc=None):
        N = self.number_points + 1
        if tdc == None:
            tdc = self.tdc1
        r = self.r
        l = self.L
        t = np.linspace(0, 2*np.pi, N)
        self.theta = t
        x_mean = np.sqrt(l**2 - r**2)
        x = r * np.cos(t-tdc) + np.sqrt(l**2 - r**2*np.sin(t-tdc)**2) - x_mean
        return x 

    def p_head_end(self, tdc=None, full_output=False, plot_process=False, aux_process=False):

        N = self.number_points + 1
        self.update_interstages_parameters()
        ang = np.linspace(0, 2*np.pi, N)

        if tdc == None:
            tdc = self.tdc1

        open_suc = [False]*N
        open_disch = [False]*N

        if not self.double_effect and self.active_cylinder != 'HEAD END' and not aux_process:
            p = np.zeros(N) 
            print('Cylinder does not have Head End Pressure.')
        else:
            x = self.recip_x(tdc=0)
            # open_suc = [False]*N
            # open_disch = [False]*N
            p, vol = [], []
            p0 = self.pr
            p_aux = p0
            l0 = self.c*(2*self.r)
            i = 0
            #EXPANSION CYCLE
            while p_aux > 1 and i < N:
                p_aux = p0*(l0 / (l0 + x[0]-x[i]))**self.k
                if p_aux < 1:
                    p_aux = 1
                    open_suc[i] = True
                p.append(p_aux*self.ps)
                # rho.append(p_aux*self.ps/(self.R*self.T))
                vol.append(self.area_head_end*(l0 + x[0]-x[i]))
                i += 1

            if i < N:
                #SUCTION CYCLE
                while i <= (N-1)/2:
                    p.append(1*self.ps)
                    vol.append(self.area_head_end*(l0 + x[0]-x[i]))
                    open_suc[i] = True
                    i += 1

                #COMPRESSION CYCLE
                p0 = 1
                i0 = i
                # while p_aux < self.pr and i < N:
                #     p_aux = p0*(l0 + 2*self.r)**self.k / (l0 + x[0]-x[i])**self.k
                #     vol.append(self.area_head_end*(l0 + x[0]-x[i]))
                #     if p_aux > self.pr:
                #         p_aux = self.pr
                #         open_disch[i] = True
                #     p.append(p_aux*self.ps)
                #     i += 1
                while p_aux < self.pr and i < N:
                    vol.append(self.area_head_end*(l0 + x[0] - x[i]))
                    if (2*np.pi-ang[i])/np.pi > self.cap:
                        p_aux = 1
                        open_suc[i] = True
                        i0 = i
                    else:
                        p_aux = p0*((l0 + x[0] - x[i0])/(l0 + x[0] - x[i]))**self.k
                    if p_aux > self.pr:
                        p_aux = self.pr
                        open_disch[i] = True
                    i += 1
                    p.append(p_aux*self.ps)

                #DISCHARGE CYCLE
                while i < N:
                    p.append(self.pr*self.ps)
                    vol.append(self.area_head_end*(l0 + x[0]-x[i]))
                    open_disch[i] = True
                    i += 1

        p = offset_to_tdc(p, tdc)
        vol = offset_to_tdc(vol, tdc)
        open_suc = offset_to_tdc(open_suc, tdc)
        open_disch = offset_to_tdc(open_disch, tdc)
     
        if plot_process:
            return vol, p

        if full_output:
            return p, open_suc, open_disch
        else:
            return p

    def p_crank_end(self, tdc=None, full_output=False, plot_process=False):

        if tdc == None:
            tdc = self.tdc1

        if not self.double_effect and self.active_cylinder != 'CRANK END':
            print('Cylinder does not have Crank End Pressure.')

        vol, pressure = self.p_head_end(tdc-np.pi, full_output=full_output, plot_process=plot_process)
        vol = list(np.array(vol)*(self.D**2 - self.rod**2)/self.D**2)
        return vol, pressure

    def flow_head_end(self, tdc=None, aux_process=False):

        N = self.number_points

        if tdc == None:
            tdc = self.tdc1

        if not self.double_effect and self.active_cylinder != 'HEAD END' and not aux_process:
            print('Cylinder does not have Head End Pressure.')
            return { 'in_flow': np.zeros(N+1),
                     'out_flow': np.zeros(N+1) }
        else:
            _, open_suc, open_disch = self.p_head_end(tdc=0, full_output=True, aux_process=aux_process)

            vel = self.recip_v(tdc=0)
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

    def flow_crank_end(self, tdc=None):

        N = self.number_points

        if tdc == None:
            tdc = self.tdc1

        if not self.double_effect and self.active_cylinder != 'CRANK END':
            print('Cylinder does not have Crank End Pressure.')
            return { 'in_flow': np.zeros(N+1),
                     'out_flow': np.zeros(N+1) }
        else:
            aux_dict = self.flow_head_end(tdc-np.pi, aux_process=True)
            flow_in = aux_dict['in_flow'] * (self.D**2 - self.rod**2)/self.D**2
            flow_out = aux_dict['out_flow'] * (self.D**2 - self.rod**2)/self.D**2
            return { 'in_flow': flow_in,
                     'out_flow': flow_out }

    def process_sum_of_volumetric_flow_rate(self, key):

        if self.double_effect:

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_crank_end(tdc=self.tdc1)[key] + self.flow_head_end(tdc=self.tdc1)[key]
                # print('double_effect', 1)
            else:
                flow_rate = self.flow_crank_end(tdc=self.tdc1)[key] + self.flow_head_end(tdc=self.tdc1)[key]
                flow_rate += self.flow_crank_end(tdc=self.tdc2)[key] + self.flow_head_end(tdc=self.tdc2)[key]
                # print('double_effect', 2)

        elif self.active_cylinder == 'HEAD END':

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_head_end(tdc=self.tdc1)[key]
                # print('head end', 1)
            else:
                flow_rate = self.flow_head_end(tdc=self.tdc1)[key]
                flow_rate += self.flow_head_end(tdc=self.tdc2)[key]
                # print('head end', 2)

        elif self.active_cylinder == 'CRANK END':

            if self.number_of_cylinders == 1:
                flow_rate = self.flow_crank_end(tdc=self.tdc1)[key]
                # print('crank end', 1)
            else:
                flow_rate = self.flow_crank_end(tdc=self.tdc1)[key]
                flow_rate += self.flow_crank_end(tdc=self.tdc2)[key]
                # print('crank end', 2)

        return flow_rate

    def FFT_periodic(self, x_t, one_sided = True):
        N = x_t.shape[0]
        if one_sided: # One-sided spectrum
            Xf = 2*np.fft.fft(x_t)
            Xf[0] = Xf[0]/2
        else: # Two-sided spectrum
            Xf = np.fft.fft(x_t)
        return Xf/N

    def process_FFT_of_(self, values, revolutions):
        Trev = 60/self.rpm
        T = revolutions*Trev
        df = 1/T
        values_time = np.tile(values[:-1], revolutions) # extending signals
        values_freq = self.FFT_periodic(values_time)
        
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

    def plot_PV_diagram_head_end(self, plot_process=True):
        vol, pressure = self.p_head_end(plot_process=plot_process)

        x_label = "Volume [m³]"
        y_label = "Pressure [kgf/cm²]"
        title = "P-V RECIPROCATING COMPRESSOR DIAGRAM"
        plot(vol, pressure, x_label, y_label, title)

    def plot_PV_diagram_crank_end(self, plot_process=True):
        vol, pressure = self.p_crank_end(plot_process=plot_process)

        x_label = "Volume [m³]"
        y_label = "Pressure [kgf/cm²]"
        title = "P-V RECIPROCATING COMPRESSOR DIAGRAM"
        plot(vol, pressure, x_label, y_label, title)

    def plot_pressure_vs_time(self):
        N = self.number_points
        _, pressure = self.p_head_end(plot_process=True)
        T = 60/self.rpm
        dt = T/N
        time = np.arange(0, T+dt, dt)

        x_label = "Time [s]"
        y_label = "Pressure [kgf/cm²]"
        title = "PRESSURE vs TIME PLOT"
        plot(time, pressure, x_label, y_label, title)

    def plot_volume_vs_time(self):
        N = self.number_points
        volume, _ = self.p_head_end(plot_process=True)
        T = 60/self.rpm
        dt = T/N
        time = np.arange(0, T+dt, dt)

        x_label = "Time [s]"
        y_label = "Volume [m³]"
        title = "VOLUME vs TIME PLOT"
        plot(time, volume, x_label, y_label, title)

    def plot_volumetric_flow_rate_at_suction_time(self):
        flow_rate = self.process_sum_of_volumetric_flow_rate('in_flow')
        N = self.number_points
        T = 60/self.rpm
        dt = T/N
        time = np.arange(0, T+dt, dt)
        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "TIME PLOT OF VOLUMETRIC FLOW RATE AT SUCTION"
        plot(time, flow_rate, x_label, y_label, title)

    def plot_volumetric_flow_rate_at_discharge_time(self):
        flow_rate = self.process_sum_of_volumetric_flow_rate('out_flow')
        N = self.number_points
        T = 60/self.rpm
        dt = T/N
        time = np.arange(0, T+dt, dt)
        x_label = "Time [s]"
        y_label = "Volume [m³/s]"
        title = "TIME PLOT OF VOLUMETRIC FLOW RATE AT DISCHARGE"
        plot(time, flow_rate, x_label, y_label, title)
    
    def plot_volumetric_flow_rate_at_suction_frequency(self, revolutions):
        freq, flow_rate = self.process_FFT_of_volumetric_flow_rate(revolutions, 'in_flow')
        x_label = "Frequency [Hz]"
        y_label = "Volumetric head flow rate [m³/s]"
        title = "FREQUENCY PLOT OF VOLUMETRIC FLOW RATE AT SUCTION"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)  

    def plot_volumetric_flow_rate_at_discharge_frequency(self, revolutions):
        freq, flow_rate = self.process_FFT_of_volumetric_flow_rate(revolutions, 'out_flow')
        x_label = "Frequency [Hz]"
        y_label = "Volumetric crank flow rate [m³/s]"
        title = "FREQUENCY PLOT OF VOLUMETRIC FLOW RATE AT DISCHARGE"
        plot(freq, flow_rate, x_label, y_label, title, _absolute=True)  

    def plot_head_end_pressure_vs_angle(self):
        N = self.number_points
        _, pressure = self.p_head_end(plot_process=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Angle [degree]"
        y_label = "Pressure [kgf/cm²]"
        title = "HEAD END PRESSURE vs ANGLE"
        plot(angle, pressure, x_label, y_label, title)

    def plot_head_end_volume_vs_angle(self):
        N = self.number_points
        volume, _ = self.p_head_end(plot_process=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Angle [degree]"
        y_label = "Volume [m³]"
        title = "HEAD END VOLUME vs ANGLE"
        plot(angle, volume, x_label, y_label, title)

    def plot_crank_end_pressure_vs_angle(self):
        N = self.number_points
        _, pressure = self.p_crank_end(plot_process=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Angle [degree]"
        y_label = "Pressure [kgf/cm²]"
        title = "CRANK END PRESSURE vs ANGLE"
        plot(angle, pressure, x_label, y_label, title)

    def plot_crank_end_volume_vs_angle(self):
        N = self.number_points
        volume, _ = self.p_crank_end(plot_process=True)

        d_theta = 360/N
        angle = np.arange(0, N+1, 1)*d_theta

        x_label = "Angle [degree]"
        y_label = "Volume [m³]"
        title = "CRANK END VOLUME vs ANGLE"
        plot(angle, volume, x_label, y_label, title)