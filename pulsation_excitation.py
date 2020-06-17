import numpy as np
import matplotlib.pyplot as plt


def FFT_periodic(x_, one_sided = True):
    
    N = x_.shape[0]-1
    if one_sided: # One-sided spectrum
        Xf = 2*np.fft.fft(x_[:-1])/N
        Xf[0] = Xf[0]/2
    else: # Two-sided spectrum
        Xf = np.fft.fft(x_[:-1])/N
    return Xf

f_mech = 10 # mechanical frequency [Hz]
N_pistons = 3 # number of pistons
dt_rev = 1/f_mech
dt_each_piston = dt_rev/N_pistons
dt_pulsation = 6/1000 # pulse width time
A = 40e5

fs = 60000
dt = 1/fs
N = round(dt_each_piston/dt)

t = np.arange(0,dt_each_piston+dt,dt)
x = np.zeros_like(t)

t_pulse = np.arange(0,dt_pulsation+dt,dt)

signal_type = 2
if signal_type == 1:
    x_pulse = A*((np.sin(2*np.pi*t_pulse/dt_pulsation))**1)*np.exp(-8*t_pulse/dt_pulsation)
    x_pulse = x_pulse*((np.sin(np.pi*t_pulse/dt_pulsation))**2)
    filename = "compressor_signal_1.dat"
elif signal_type == 2:
    x_pulse = A*((np.sin(np.pi*t_pulse/dt_pulsation))**4)
    filename = "compressor_signal_2.dat"
else:
    print("Invalid signal type input!")
x[0:t_pulse.shape[0]] = x_pulse

N_rev = 5
df = 1/(N_rev*dt_rev) # Hz

aux = np.arange(1, N_rev*N_pistons, 1)
ind = np.ones(N_rev*N_pistons-1)*t.shape[0]*aux + 1

x_rev = np.tile(x, N_rev*N_pistons)
x_rev = np.delete(x_rev, ind.astype(int))
t_rev = np.arange(0, x_rev.shape[0], 1 )*dt

N_points = x_rev.shape[0]-1 


freq = np.arange(0, fs, df)
Xf = FFT_periodic(x_rev)
f_max = 200
spectral_lines_to_save = np.arange(0,f_max+df,df) 
N_spectral_lines = len(spectral_lines_to_save)

Xf = Xf[0:N_spectral_lines]
freq = freq[0:N_spectral_lines]

header = "Frequency [Hz], Real(acoustic pressure), Imaginary(acoustic pressure)"
output = np.array([freq, np.real(Xf), np.imag(Xf)]).T

np.savetxt(filename, output, delimiter=",", header=header)
load_file = np.loadtxt(filename, delimiter=",")

fig1 = plt.figure(figsize=[10,6])
ax1 = fig1.add_subplot(1,1,1)

# plt.plot(t_rev, x_rev, linewidth=1.5, color=[0,0,1])
plt.plot(t, x, linewidth=1.0, color=[1,0,0])
plt.plot(t_pulse, x_pulse, linewidth=2.0, color=[0,0,0])
ax1.set_title('Virtual Pressure pulsation of the Compressor', fontsize = 18, fontweight = 'bold')
ax1.set_xlabel('Time [s]', fontsize = 16, fontweight = 'bold')
ax1.set_ylabel("Amplitude of pressure [Pa]", fontsize = 16, fontweight = 'bold')
        
plt.grid()
plt.show()

fig2 = plt.figure(figsize=[10,6])
ax2 = fig2.add_subplot(1,1,1)

plt.plot(freq, np.abs(Xf), linewidth=2.0, color=[0,0,0])
ax2.set_title('Virtual Spectrum of Pressure pulsation of the Compressor', fontsize = 18, fontweight = 'bold')
ax2.set_xlabel('Frequency [Hz]', fontsize = 14, fontweight = 'bold')
ax2.set_ylabel("Pressure spectrum magnitude [Pa]", fontsize = 14, fontweight = 'bold')
        
plt.grid()
plt.show()

## Amplitude correction checks for sine functions

# T = 1
# fs = 1000
# dt = 1/fs

# t_sine = np.arange(0, T+dt, dt)
# x_sine = np.sin(2*np.pi*50*t_sine)

# Xf_sine = FFT_periodic(x_sine)
# N_spectral_lines = Xf_sine.shape[0]
# freq_sine = np.arange(0, N_spectral_lines, 1)*(1/T)

# fig3 = plt.figure(figsize=[10,6])
# ax3 = fig3.add_subplot(1,1,1)

# plt.plot(freq_sine, np.abs(Xf_sine), linewidth=2.0, color=[0,0,0])
# ax3.set_title('Virtual Spectrum of Pressure pulsation of the Compressor', fontsize = 18, fontweight = 'bold')
# ax3.set_xlabel('Frequency [Hz]', fontsize = 14, fontweight = 'bold')
# ax3.set_ylabel("Pressure spectrum magnitude [Pa]", fontsize = 14, fontweight = 'bold')
# plt.xlim([0, 100])
        
# plt.grid()
# plt.show()
