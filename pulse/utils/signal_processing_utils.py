import numpy as np


def process_iFFT_of_onesided_signal(df: float, Xf: np.ndarray, remove_avg: bool = True):

    N = len(Xf)
    x_t = np.fft.irfft(Xf) * (N - 1)
    if remove_avg:
        x_t -= np.average(x_t)

    N_t = len(x_t)
    time = np.arange(0, N_t) / (df * N_t)

    return time, x_t