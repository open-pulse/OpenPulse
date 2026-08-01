import numpy as np
from scipy import signal


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
    xt_rms = np.sqrt(np.sum(x_t**2) / len(x_t))
    Xf_rms = np.sqrt(np.sum(np.abs(X_f * np.conjugate(X_f))))

    # print(xt_rms, Xf_rms)
    if round(xt_rms, 8) == round(Xf_rms, 8):
        return True

    message = "Both domains do not have the same rms/energy values.\n"
    message += f"x_t rms: {round(xt_rms, 8)} \nX_f rms: {round(Xf_rms, 8)}"
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
        output[1:N_in] = Xf[1:] / 2
        output[N_in:] = np.conjugate(np.flip(Xf[1:-1])) / 2

    else:
        N_out = 2 * (N_in - 1) + 1
        output = np.zeros(N_out, dtype=complex)
        output[1:N_in] = Xf[1:] / 2
        output[N_in:] = np.conjugate(np.flip(Xf[1:])) / 2

    output[0] = Xf[0]

    return output


def process_ifft_from_one_sided_spectrum_signal(frequencies: np.ndarray, Xf_data: np.ndarray):
    """
    If n is even, the length of the transformed axis is (n/2)+1. If n is odd, the length is (n+1)/2.
    """

    N_f = len(Xf_data)

    # reinsert the DC component
    if frequencies[0] != 0:
        N_f += 1

    # create the auxilar vector Xf
    Xf = np.zeros(N_f, dtype=complex)

    # adjust the one-sided spectrum scale
    Xf[1:] = Xf_data / 2

    # process the sampling frequency and time increment
    f_max = np.max(frequencies)
    f_s = 2 * f_max
    dt = 1 / f_s

    # process the ifft from signal Xf
    x_t = np.fft.irfft(Xf)  # * (2*(N-1))
    N_t = len(x_t)

    # corrects the signal amplitude
    x_t *= N_t

    # create the time vector
    time = np.arange(N_t, dtype=float) * dt

    return time, x_t


def extend_signal(x_data: np.ndarray, N_rep: int):
    return np.tile(x_data[:-1], N_rep)


def process_one_sided_spectrum(x_data: np.ndarray, dt: float):

    # create the frequencies vector
    freq_vector = np.fft.rfftfreq(len(x_data), dt)

    # process the one-sided spectrum
    Xf_data = np.fft.rfft(x_data) / len(x_data)

    # adjust the one-sided spectrum amplitude
    Xf_data[1:] *= 2

    return freq_vector, Xf_data


def process_two_sided_spectrum(x_data: np.ndarray, dt: float):

    # create the frequencies vector
    freq_vector = np.fft.fftfreq(len(x_data), dt)

    # process the one-sided spectrum
    Xf_data = np.fft.fft(x_data) / len(x_data)

    freq_vector = np.fft.fftshift(freq_vector)
    Xf_data = np.fft.fftshift(Xf_data)

    check_if_signal_energy_is_conserved(x_data, Xf_data)

    return freq_vector, Xf_data


def get_window_and_correction_factor(window_type: str, correction_type: str, N: int):

    if window_type == "rectangular":
        window_type = "boxcar"

    if window_type not in ["hann", "flattop", "boxcar", "hamming"]:
        return 1, 1

    # create the window
    window = signal.get_window(window_type, N)

    if correction_type == "amplitude":
        correction_factors = {"boxcar": 1, "hann": 2, "flattop": 4.18, "hamming": 1.85}

    else:
        correction_factors = {"boxcar": 1, "hann": np.sqrt(8 / 3), "flattop": 2.26, "hamming": 1.59}

    return window, correction_factors.get(window_type)


def check_if_signal_energy_is_conserved(x_data: np.ndarray, Xf_data: np.ndarray):
    x_rms = np.sqrt(np.sum(x_data**2) / len(x_data))
    Xf_rms = np.sqrt(np.sum(np.abs(Xf_data * np.conjugate(Xf_data))))

    if round(x_rms, 8) != round(Xf_rms, 8):
        message = "Both domains do not have the same rms/energy values.\n"
        message += f"RMS value (x_data): {round(x_rms, 8)} \n"
        message += f"RMS value (Xf_data): {round(Xf_rms, 8)}"
        print(message)


def plot(x, y, x_label, y_label, title, label="", absolute=False):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1, 1, 1)

    if absolute:
        y = np.abs(y)

    ax.plot(x, y, color=[0, 0, 1], linewidth=1, label=label)

    ax.set_xlabel(x_label, fontsize=11, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=12, fontweight="bold")

    plt.grid()
    plt.show()


def plot_original_and_windowed_spectrums(freq: np.ndarray, Xf: np.ndarray, Xf_w: np.ndarray):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1, 1, 1)

    ax.semilogy(freq, np.abs(Xf), color=[0, 0, 1], linewidth=1, label="non-windowed signal")
    ax.semilogy(freq, np.abs(Xf_w), color=[1, 0, 0], linewidth=1, label="windowed signal")

    ax.set_xlabel("Frequency [Hz]", fontsize=11, fontweight="bold")
    ax.set_ylabel("Amplitude [--]", fontsize=11, fontweight="bold")
    ax.set_title("", fontsize=12, fontweight="bold")

    plt.legend()
    plt.grid()
    plt.show()
