# SET OF FUNCTIONS FOR SIGNAL PROCESSING

import numpy as np
import scipy as sp
from matplotlib import pyplot as plt

def FFT_periodic(t, x_t, one_sided = True, rms_scaling=False):
    dt = t[1]-t[0]
    T = t[-1] + dt
    fs = 1/dt
    N = x_t.shape[0]
    df = fs/N
    freq = np.arange(N)*df
    if one_sided: # One-sided spectrum
        Xf = 2*np.fft.fft(x_t)
        Xf[0] = Xf[0]/2
        if np.remainder(N,2)==0:
            Nsel = int(N/2)
        else:
            Nsel = int((N+1)/2)
        freq = freq[0:Nsel]
        Xf = Xf[0:Nsel]
    else: # Two-sided spectrum
        Xf = np.fft.fft(x_t)
    if rms_scaling:
        Xf[1:] = Xf[1:]/np.sqrt(2)
    return freq, Xf/(fs*T)

def FFT_transient(t, x_t, one_sided = True, rms_scaling=False):
    dt = t[1]-t[0]
    # T = t[-1] + dt
    fs = 1/dt
    N = x_t.shape[0]
    df = fs/N
    freq = np.arange(N)*df
    if one_sided: # One-sided spectrum
        Xf = 2*np.fft.fft(x_t)
        Xf[0] = Xf[0]/2
        if np.remainder(N,2)==0:
            Nsel = int(N/2)
        else:
            Nsel = int((N+1)/2)
        freq = freq[0:Nsel]
        Xf = Xf[0:Nsel]
    else: # Two-sided spectrum
        Xf = np.fft.fft(x_t)
    if rms_scaling:
        Xf[1:] = Xf[1:]/np.sqrt(2)
    return freq, Xf/fs

if __name__ == "__main__":
    
    # SIGNAL AQUISITION PARAMETERS
    Npoints = 2048
    fs = 2048
    df = fs/Npoints
    T = 1/df

    # BUILDING THE SIGNAL
    t = np.arange(0, T, T/Npoints)
    f1, f2, f3 = 10, 20, 40
    A1, A2, A3 = 1, 0.5, 0.25
    x_t = A1*np.sin(2*np.pi*t*f1) + A2*np.sin(2*np.pi*t*f2) + A3*np.sin(2*np.pi*t*f3)

    # PERFORM THE FAST FOURIER TRANSFORM OF SIGNAL
    one_sided = True
    freq, X_f = FFT_periodic(t, x_t, one_sided=one_sided)

    # CHECKING THE RMS OF SIGNAL IN BOTH DOMAINS - SEE THE PARSEVAL'S THEOREM
    x_t_RMS = np.sqrt(np.sum(x_t**2)/Npoints)
    if one_sided:
        _, Xf = FFT_periodic(t,x_t, one_sided=False)
    else:
        Xf = X_f.copy()
    Xf_RMS = np.sqrt(np.sum(np.abs(Xf)**2))
    print("The rms of signal in time domain is {}".format(x_t_RMS))
    print("The rms of signal in frequency domais is {}".format(Xf_RMS))

    # PLOT OF SIGNAL IN THE TIME DOMAIN
    fig = plt.figure(figsize=[12,7])
    ax = fig.add_subplot(1,1,1)
    first_plot = ax.plot(t, x_t, color=[1,0,0], linewidth=2, label="Flow out")
    ax.set_xlabel("Time [s]", fontsize = 14, fontweight = 'bold')
    ax.set_ylabel("Signal Amplitude [--]", fontsize = 14, fontweight = 'bold')
    plt.grid()
    plt.show()

    # PLOT OF SIGNAL IN THE FREQUENCY DOMAIN
    fig = plt.figure(figsize=[12,7])
    ax = fig.add_subplot(1,1,1)
    second_plot = ax.plot(freq, np.abs(X_f), color=[1,0,0], linewidth=2, label="Flow out")
    ax.set_xlabel("Frequency [Hz]", fontsize = 14, fontweight = 'bold')
    ax.set_ylabel("Signal Magnitude [--]", fontsize = 14, fontweight = 'bold')
    plt.grid()
    plt.show()