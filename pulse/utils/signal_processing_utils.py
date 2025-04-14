import numpy as np


def process_iFFT_of_onesided_spectrum(df: float, Xf: np.ndarray, remove_avg: bool = True):
    """
    This function processes the inverse Fourier Transform of one-sided signal spectrum.

    Parameters
    ----------
    df : float
        spectrum resolution

    Xf : ndarray (complex data type)
        Represents the terms of one-sided spectrum of input signal.

    remove_avg : bool (default True)
    
        If True remove the average from signal output and False otherwise.
    
    Returns
    -------

    time : ndarray (float data type)
        The time vector of output signal.

    x_t : ndarray (float data type)
        The output signal in time domain. 
    
    """

    N = len(Xf)
    x_t = np.fft.irfft(Xf) * (N - 1)
    if remove_avg:
        x_t -= np.average(x_t)

    N_t = len(x_t)
    time = np.arange(0, N_t) / (df * N_t)
    

    return time, x_t

def is_parseval_theorem_satisfied(x_t: np.ndarray, X_f: np.ndarray) -> bool:
    """
    This function checks if the signal energy in time and frequency
    domains are conserved (Parseval's Theorem).

    Parameters
    ----------

    x_t : ndarray (normally, float data type). 
        Represents the signal x(t) in time domain.

    X_f : ndarray (complex data type)
        Represents the signal X(f) in frequency domain.


    Returns
    -------

    True if the signal energy is conserved, and False otherwise.   

    """
    xt_rms = np.sqrt(np.sum(x_t**2)/len(x_t))
    Xf_rms = np.sqrt(np.sum(np.abs(X_f*np.conjugate(X_f))))

    # print(xt_rms, Xf_rms)
    if round(xt_rms,8) == round(Xf_rms,8):
        return True

    message = "Both domains do not have the same rms/energy values.\n"
    message += f"x_t rms: {round(xt_rms,8)} \nX_f rms: {round(Xf_rms,8)}"
    print(message)
    return False

def process_twosided_spectrum(Xf: np.ndarray) -> np.ndarray:
    """
    This function returns the two-sided spectrum from a one-sided spectrum.

    Parameters
    ----------

    Xf : ndarray of complex values
        One-sided spectrum of signal.

    Returns
    -------
    ouput : ndarray of complex values
        Two-sided spectrum of signal.
    """

    N_in = len(Xf)

    # check the robustness of this criterion
    if round(abs(np.imag(Xf[-1])), 15) == 0:
        N_out = 2 * (N_in - 1)
        output = np.zeros(N_out, dtype=complex)
        output[1 : N_in] = Xf[1:] / 2
        output[N_in : ] = np.conjugate(np.flip(Xf[1:-1])) / 2

    else:
        N_out = 2 * (N_in - 1) + 1
        output = np.zeros(N_out, dtype=complex)
        output[1 : N_in] = Xf[1:] / 2
        output[N_in : ] = np.conjugate(np.flip(Xf[1:])) / 2

    output[0] = Xf[0]

    return output 