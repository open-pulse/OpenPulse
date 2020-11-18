# -*- coding: utf-8 -*-


import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import ccp
from ccp import Q_
from scipy.optimize import root_scalar, newton, toms748, ridder, bisect
import plotly.express as px
import pandas as pd

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
                 Ps,            # Suction pressure (bar a)
                 Ts,            # Suction temperature (degC)
                 p_ratio,       # Compressor pressure ratio Pd/Ps
                 rpm,           # Compressor rotation speed (rpm)
                 double_effect, # Compressor is double effect (bool)
                 stroke,        # Length of compressor full stroke (m)
                 L,             # Connecting rod length
                 clearance,     # Clearance volume as percentage of full volume (%)
                 k_gas=None,    # Compressed gas isentropic exponent
                 MW=None,       # Gas molecular weight
                 gas=None,      # Gas name (not necessary if MX and k_gas informed)
                 rod_diam=0,    # Rod diameter (m)
                 active_cyl='HE',# Active cylinder (only if double effect = False): 'HE' or 'CE'
                 tdc_angle=0,   # Crank angle (degrees) at which piston is at top dead center
                 cap=100,
                 ): 
        self.poly_sig = np.poly1d(np.array([ 4.07662578e-12, -1.76845633e-09,  3.22571698e-07, -3.21443114e-05,
                                       1.90316519e-03, -6.81078403e-02,  1.42782751e+00, -1.53184727e+01,
                                       9.36732673e+01]))
        
        self.D = d_cylinder
        self.Ps = Ps
        self.Ts = Ts
        self.pr = p_ratio
        self.rpm = rpm
        self.de = double_effect
        self.r = stroke/2
        self.L = L
        self.c = clearance/100
        self.rod = rod_diam

        if cap == 100:
            self.cap = 1
        elif cap == 0:
            self.cap = 0
        elif cap > 0 and cap < 100:
            self.cap = self.poly_sig(cap)/100
        else:
            self.cap = 1
        # self.cap=(19+0.62*cap)/100 # Sigmoidal

        if double_effect:
            self.active_cyl = None
        else:
            self.active_cyl = active_cyl
        self.tdc = tdc_angle*np.pi/180
                
        if gas == None:
            self.k = k_gas
            self.mw = MW
            self.vr = (self.pr)**(-1/self.k) # Volume ratio considering isentropic compression
        else:
            self.suc = ccp.State.define(fluid=gas,T=Q_(Ts,'degC'),p=Q_(Ps,'bar'))
            self.k = self.suc.kv().m
            self.mw = self.suc.molar_mass().m
            self.disch = ccp.State.define(fluid=gas,s=self.suc.s(),p=self.suc.p()*p_ratio)
            self.vr = (self.disch.v() / self.suc.v()).m
     
    def cap_real(self):
        
        r = (float(self.cap)*100 - self.poly_sig).roots
        cap_real = np.real(r)[np.argmin([np.abs(np.imag(a)) for a in r])]
        if cap_real > 100:
            cap_real = 100
        elif cap_real < 0:
            cap_real = 0
            
        return cap_real #self.cap*100
    
    def recip_a(self,N,tdc=None):
        
        if tdc == None:
            tdc = self.tdc
        r = self.r
        l = self.L
        t = np.linspace(0,2*np.pi,N)
        a = -r * np.cos(t-tdc) 
        a = a - (r**2*(np.cos(t-tdc)**2 - np.sin(t-tdc)**2))/np.sqrt(l**2 - r**2*np.sin(t-tdc)**2)
        a = a - (r**4*(np.cos(t-tdc)**2 * np.sin(t-tdc)**2))/np.sqrt(l**2 - r**2*np.sin(t-tdc)**2)**3
        a = a * (self.rpm/60*2*np.pi)**2
        
        return a    
    
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
        
        ang = np.linspace(0,2*np.pi,N)
        
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
                i0 = i
                while p_aux < self.pr and i < N:
                    if (2*np.pi-ang[i])/np.pi > self.cap:
                        p_aux = 1
                        open_suc[i] = True
                        i0 = i
                    else:
                        p_aux = p0*(l0 + x[0]-x[i0])**self.k / (l0 + x[0]-x[i])**self.k
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
            return np.zeros(N)
        else:
            aux, open_suc, open_disch = self.p_head_end(N,tdc=0,full_output=True)
            
            vel = self.recip_v(N,tdc=0)
            flow_in = np.zeros(N)
            flow_out = np.zeros(N)
            
            for i, v in enumerate(vel):
                if open_suc[i]:
                    flow_in[i] = v * np.pi*self.D**2/4
                if open_disch[i]:
                    flow_out[i] = v * np.pi*self.D**2/4
            
            flow_in = offset_to_tdc(flow_in,tdc)
            flow_out = offset_to_tdc(flow_out,tdc)
                    
            return {'in_flow': flow_in,
                    'out_flow': flow_out}
            
    def flow_crank_end(self,N,tdc=None):
        
        if tdc == None:
            tdc = self.tdc
            
        if not self.de and self.active_cyl != 'CE':
            print('Cylinder does not have Crank End Pressure.')
            return np.zeros(N)
        else:
            aux_dict = self.flow_head_end(N,tdc-np.pi)
            flow_in = aux_dict['in_flow'] * (self.D**2 - self.rod**2)/self.D**2
            flow_out = aux_dict['out_flow'] * (self.D**2 - self.rod**2)/self.D**2
            
            return {'in_flow': flow_in,
                    'out_flow': flow_out}
    
    def mass_flow_crank_end(self,N,tdc=None):
        
        if tdc == None:
            tdc = self.tdc
            
        vf = self.flow_crank_end(N,tdc)
        mf = -vf['in_flow']*self.suc.rho().m
        
        return mf

    def mass_flow_head_end(self,N,tdc=None):
    
        if tdc == None:
            tdc = self.tdc
            
        vf = self.flow_head_end(N,tdc)
        mf = -vf['in_flow']*self.suc.rho().m
        
        return mf
    
    def total_mass_flow(self):
        
        N = 1000
        T = 60 / self.rpm
        dt = np.linspace(0,T,N)[1]
        
        f_he = np.sum(self.mass_flow_head_end(N)*dt)*self.rpm/60
        f_ce = np.sum(self.mass_flow_crank_end(N)*dt)*self.rpm/60
        
        return f_he+f_ce

      
def create_compressor(cap1,ks1,ks2,Pd,tol=0.005,
                      cap2=None,cap3=None,
                      output_cap=False):
    global cil2, cil3, cil4
    Ts = 45
    Ps = 20
    # Pd = 142
    # ks1 = 1
    # ks2 = 0.97
    # if cap2 == None:
    cap2_0 = cap1
    # if cap3 == None:
    cap3_0 = cap1
    
    pr = Pd/Ps
    
    Pi1 = Ps * ks1 * pr**(1/3)
    Pi2 = Ps * ks2 * pr**(2/3)
        
    
    L = 1.3
       
    
    cil1 = Cylinder(d_cylinder=0.78,    # Cylinder bore diameter (m)
                     Ps=Ps,            # Suction pressure (bar a)
                     Ts=Ts,            # Suction temperature (degC)
                     p_ratio=Pi1/Ps,       # Compressor pressure ratio Pd/Ps
                     rpm=360,           # Compressor rotation speed (rpm)
                     double_effect=True, # Compressor is double effect (bool)
                     k_gas=None,    # Compressed gas isentropic exponent
                     MW=None,       # Gas molecular weight
                     gas='H2',      # Gas name (not necessary if MX and k_gas informed)
                     stroke=0.33,        # Length of compressor full stroke (m)
                     L=L,             # Connecting rod length
                     clearance=17,     # Clearance volume as percentage of full volume (%)
                     rod_diam=0.135,
                     tdc_angle=0,   # Crank angle (degrees) at which piston is at top dead center
                     cap=cap1,
                     )
    
    cil2 = Cylinder(d_cylinder=0.315,    # Cylinder bore diameter (m)
                     Ps=Pi2,            # Suction pressure (bar a)
                     Ts=Ts,            # Suction temperature (degC)
                     p_ratio=Pd/Pi2,       # Compressor pressure ratio Pd/Ps
                     rpm=360,           # Compressor rotation speed (rpm)
                     double_effect=True, # Compressor is double effect (bool)
                     k_gas=None,    # Compressed gas isentropic exponent
                     MW=None,       # Gas molecular weight
                     gas='H2',      # Gas name (not necessary if MX and k_gas informed)
                     stroke=0.33,        # Length of compressor full stroke (m)
                     L=L,             # Connecting rod length
                     clearance=18.4,     # Clearance volume as percentage of full volume (%)
                     rod_diam=0.135,
                     tdc_angle=0,   # Crank angle (degrees) at which piston is at top dead center
                     cap=cap3_0
                     )
    
    cil3 = Cylinder(d_cylinder=0.575,    # Cylinder bore diameter (m)
                     Ps=Pi1,            # Suction pressure (bar a)
                     Ts=Ts,            # Suction temperature (degC)
                     p_ratio=Pi2/Pi1,       # Compressor pressure ratio Pd/Ps
                     rpm=360,           # Compressor rotation speed (rpm)
                     double_effect=True, # Compressor is double effect (bool)
                     k_gas=None,    # Compressed gas isentropic exponent
                     MW=None,       # Gas molecular weight
                     gas='H2',      # Gas name (not necessary if MX and k_gas informed)
                     stroke=0.33,        # Length of compressor full stroke (m)
                     L=L,             # Connecting rod length
                     clearance=16.4,     # Clearance volume as percentage of full volume (%)
                     rod_diam=0.135,
                     tdc_angle=90,   # Crank angle (degrees) at which piston is at top dead center
                     cap=cap2_0
                     )
    
    cil4 = Cylinder(d_cylinder=0.315,    # Cylinder bore diameter (m)
                     Ps=Pi2,            # Suction pressure (bar a)
                     Ts=Ts,            # Suction temperature (degC)
                     p_ratio=Pd/Pi2,       # Compressor pressure ratio Pd/Ps
                     rpm=360,           # Compressor rotation speed (rpm)
                     double_effect=True, # Compressor is double effect (bool)
                     k_gas=None,    # Compressed gas isentropic exponent
                     MW=None,       # Gas molecular weight
                     gas='H2',      # Gas name (not necessary if MX and k_gas informed)
                     stroke=0.33,        # Length of compressor full stroke (m)
                     L=L,             # Connecting rod length
                     clearance=18.4,     # Clearance volume as percentage of full volume (%)
                     rod_diam=0.135,
                     tdc_angle=90,   # Crank angle (degrees) at which piston is at top dead center
                     cap=cap3_0
                     )
    
    if cap2 != None:
        cil3.cap = cap2
    
    
    c = 0
    c_max = 30
    while np.abs(cil3.total_mass_flow() / cil1.total_mass_flow() - 1) > tol and cil3.cap<1 and c<c_max:
        c += 1
        dev = cil3.total_mass_flow() / cil1.total_mass_flow()
        cil3.cap = cil3.cap / np.sqrt(dev)
        if cil3.cap > 1:
            cil3.cap = 1
        if cil3.cap < 0.3:
            cil3.cap = 0.3
            break
        
    if cap3 != None:
        cil2.cap = cap3
        cil4.cap = cap3
    c = 0
    while np.abs((cil2.total_mass_flow()+cil4.total_mass_flow()) / cil1.total_mass_flow() - 1) > tol and cil2.cap < 1 and c<c_max:
        c += 1
        dev = (cil2.total_mass_flow()+cil4.total_mass_flow()) / cil1.total_mass_flow()
        cil2.cap = cil2.cap / np.sqrt(dev)
        cil4.cap = cil4.cap / np.sqrt(dev)
        if cil2.cap > 1 or cil4.cap > 1:
            cil2.cap = 1
            cil4.cap = 1
            
        if cil2.cap < 0.3 or cil4.cap < 0.3:
            cil2.cap = 0.3
            cil4.cap = 0.3
            break
        
    if output_cap:
        return cil1, cil2, cil3, cil4, cil3.cap, cil2.cap
    else:
        return cil1, cil2, cil3, cil4


    
cil1, cil2, cil3, cil4 = create_compressor(75,1,0.97,
                                                140,tol=0.01)

