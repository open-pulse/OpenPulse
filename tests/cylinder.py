# -*- coding: utf-8 -*-


import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot

def offset_to_tdc(array,tdc):
    
    while tdc < 0:
        tdc += 2*np.pi
        
    
    N = len(array)
    array2 = np.zeros(N)
    
    i_tdc = round(tdc/(2*np.pi/(N-1)))
    
    array2[i_tdc:] = array[0:N-i_tdc]
    array2[0:i_tdc] = array[N-i_tdc:]
    
    return array2


class Cylinder:
    
    def __init__(self,
                 d_cylinder,    # Cylinder bore diameter (m)
                 p_ratio,       # Compressor pressure ratio Pd/Ps
                 rpm,           # Compressor rotation speed (rpm)
                 double_effect, # Compressor is double effect (bool)
                 k_gas,         # Compressed gas isentropic exponent
                 stroke,        # Length of compressor full stroke (m)
                 L,             # Connecting rod length
                 clearance,     # Clearance volume as percentage of full volume (%)
                 rod_diam=0,    # Rod diameter (m)
                 active_cyl='HE',# Active cylinder (only if double effect = False): 'HE' or 'CE'
                 tdc_angle=0,   # Crank angle (degrees) at which piston is at top dead center
                 ): 
        
        self.D = d_cylinder
        self.pr = p_ratio
        self.rpm = rpm
        self.de = double_effect
        self.k = k_gas
        self.r = stroke/2
        self.L = L
        self.c = clearance/100
        self.rod = rod_diam
        if double_effect:
            self.active_cyl = None
        else:
            self.active_cyl = active_cyl
        self.tdc = tdc_angle*np.pi/180
        
        self.vr = (self.pr)**(-1/self.k) # Volume ratio considering isentropic compression
        
        
        
    def recip_v(self,N,tdc=None):
        if tdc == None:
            tdc = self.tdc
        r = self.r
        l = self.L
        t = np.linspace(0,2*np.pi,N)
        v = -r * np.sin(t-tdc) - (r**2*np.sin(t-tdc)*np.cos(t-tdc))/np.sqrt(l**2 - r**2*np.sin(t-tdc)**2)
        v = v * self.rpm/60*2*np.pi
        
        return v
    
    def recip_x(self,N,tdc=None):
        if tdc == None:
            tdc = self.tdc
        r = self.r
        l = self.L
        t = np.linspace(0,2*np.pi,N)
        x_mean = np.sqrt(l**2 - r**2)
        x = r * np.cos(t-tdc) + np.sqrt(l**2 - r**2*np.sin(t-tdc)**2) - x_mean
    
        return x 
        
    def p_head_end(self,N,tdc=None,full_output=False):
        
        if tdc == None:
            tdc = self.tdc
            
        if not self.de and self.active_cyl != 'HE':
            print('Cylinder does not have Head End Pressure.')
        else:
            x = self.recip_x(N,tdc=0)
            open_suc = [False]*N
            open_disch = [False]*N
            p = []
            p0 = self.pr
            p_aux = p0
            l0 = self.c * self.r*2
            i = 0
            #Ciclo de expansão
            while p_aux > 1 and i < N:
                p_aux = p0*l0**self.k / (l0 + x[0]-x[i])**self.k
                if p_aux < 1:
                    p_aux = 1
                    open_suc[i] = True
                i += 1
                p.append(p_aux)
                
            if i < N:
                #Ciclo de sucção
                while i <= (N-1)/2:
                    p.append(1)
                    open_suc[i] = True
                    i += 1
                
                #Ciclo de compressão 
                p0 = 1
                while p_aux < self.pr and i < N:
                    p_aux = p0*(l0 + 2*self.r)**self.k / (l0 + x[0]-x[i])**self.k
                    if p_aux > self.pr:
                        p_aux = self.pr
                        open_disch[i] = True
                    i += 1
                    p.append(p_aux)
                
                #Ciclo de descarga
                while i < N:
                    p.append(self.pr)
                    open_disch[i] = True
                    i += 1
            
            p = offset_to_tdc(p,tdc)
            open_suc = offset_to_tdc(open_suc,tdc)
            open_disch = offset_to_tdc(open_disch,tdc)
            
            if full_output:
                return p, open_suc, open_disch
            else:
                return p
    
    def p_crank_end(self,N,tdc=None,full_output=False):
        
        if tdc == None:
            tdc = self.tdc
            
        if not self.de and self.active_cyl != 'CE':
            print('Cylinder does not have Crank End Pressure.')
        else:
            return self.p_head_end(N,tdc-np.pi,full_output=full_output)
    
    
    def flow_head_end(self,N,tdc=None):
        
        if tdc == None:
            tdc = self.tdc
        
        if not self.de and self.active_cyl != 'HE':
            print('Cylinder does not have Head End Pressure.')
        else:
            aux, open_suc, open_disch = self.p_head_end(N,tdc=0,full_output=True)
            
            vel = self.recip_v(N,tdc=0)
            flow_in = np.zeros(N)
            flow_out = np.zeros(N)
            
            for i, v in enumerate(vel):
                if open_suc[i]:
                    flow_in[i] = v * 2*np.pi*self.D**2/4
                if open_disch[i]:
                    flow_out[i] = v * 2*np.pi*self.D**2/4
            
            flow_in = offset_to_tdc(flow_in,tdc)
            flow_out = offset_to_tdc(flow_out,tdc)
                    
            return {'in_flow': flow_in,
                    'out_flow': flow_out}
            
    def flow_crank_end(self,N,tdc=None):
        
        if tdc == None:
            tdc = self.tdc
            
        if not self.de and self.active_cyl != 'CE':
            print('Cylinder does not have Crank End Pressure.')
        else:
            aux_dict = self.flow_head_end(N,tdc-np.pi)
            flow_in = aux_dict['in_flow'] * (self.D**2 - self.rod**2)/self.D**2
            flow_out = aux_dict['out_flow'] * (self.D**2 - self.rod**2)/self.D**2
            
            return {'in_flow': flow_in,
                    'out_flow': flow_out}
    
    
            
    
cil = Cylinder(d_cylinder=1,    # Cylinder bore diameter (m)
                 p_ratio=1.9,       # Compressor pressure ratio Pd/Ps
                 rpm=360,           # Compressor rotation speed (rpm)
                 double_effect=True, # Compressor is double effect (bool)
                 k_gas=1.4,         # Compressed gas isentropic exponent
                 stroke=0.3,        # Length of compressor full stroke (m)
                 L=0.8,             # Connecting rod length
                 clearance=5,     # Clearance volume as percentage of full volume (%)
                 rod_diam=0.2,    # Rod diameter (m)
                 tdc_angle=0)

cil2 = Cylinder(d_cylinder=1,    # Cylinder bore diameter (m)
                 p_ratio=1.9,       # Compressor pressure ratio Pd/Ps
                 rpm=360,           # Compressor rotation speed (rpm)
                 double_effect=True, # Compressor is double effect (bool)
                 k_gas=1.4,         # Compressed gas isentropic exponent
                 stroke=0.3,        # Length of compressor full stroke (m)
                 L=0.8,             # Connecting rod length
                 clearance=5,     # Clearance volume as percentage of full volume (%)
                 rod_diam=0.2,    # Rod diameter (m)
                 tdc_angle=90)
    

N = 1001
t = np.linspace(0,1/6,N)
x = cil.recip_x(N)
v = cil.recip_v(N)
p_he = cil.p_head_end(N)
p_ce = cil.p_crank_end(N)
f_in = cil.flow_head_end(N)['in_flow'] + cil.flow_crank_end(N)['in_flow']
f_out = cil.flow_head_end(N)['out_flow'] + cil.flow_crank_end(N)['out_flow']
f_in += cil2.flow_head_end(N)['in_flow'] + cil2.flow_crank_end(N)['in_flow']
f_out += cil2.flow_head_end(N)['out_flow'] + cil2.flow_crank_end(N)['out_flow']

fig = go.Figure(data=[go.Scatter(x=t,y=f_in),go.Scatter(x=t,y=f_out)])
plot(fig, auto_open=True)
