import numpy as np

f_min = 0
f_max = 200
df = 2

frequencies = np.arange(f_min, f_max+df, df)
value = float(1e9)
real = value * np.ones(len(frequencies))
imag = np.zeros(len(frequencies))

filename = 'stifness_Kxyz.dat'
header = "Frequency [Hz], real, imaginary"
data = np.array([frequencies, real, imag], dtype=float).T 

np.savetxt(filename, data, delimiter=",", header=header)
teste = np.loadtxt(filename,delimiter=",")

f = open(filename)
header_r = f.readline()
# last_col_name = header.split(',')[-1]
# np.savetxt('load_Fx.dat', data, delimiter=",", header=header)
# np.savetxt('acoustic_pressure_table.dat', data, delimiter=",", header=header)
# np.savetxt('volume_velocity_table.dat', data, delimiter=",", header=header)
# np.savetxt('specific_impedance_table.dat', data, delimiter=",", header=header)