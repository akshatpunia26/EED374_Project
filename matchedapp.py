import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, rfft, irfft
from scipy.signal import hamming, hann

def main():
    st.title("Matched Filtering Explored")
     st.markdown("""
This Streamlit app demonstrates the use of a matched filter for detecting a signal in noise. A signal is generated with the specified frequency, decay rate, and duration. Gaussian noise is added to the signal with the specified signal-to-noise ratio (SNR). The matched filter output is then computed using a replica of the signal, and the result is displayed in a plot.

**Input Parameters**
- `f0`: The frequency of the generated signal in Hz. Example: 150.
- `tau`: The decay rate of the signal in seconds. Example: 0.005.
- `SNR`: The signal-to-noise ratio in dB. Example: 10.
- `n`: The number of samples in the signal. Example: 1000.
- `Window Type`: The type of window function to apply to the signal. Example: Hamming.

**Expected Results:**
The plot displays the matched filter output versus time. The peak of the matched filter output corresponds to the time delay between the original signal and its replica, which is equal to the decay rate of the signal. The higher the signal-to-noise ratio, the more distinct the peak will be. The window function affects the shape of the matched filter output but does not affect the location of the peak.
""")


    # Set the default values for the signal parameters
    fs = 1000
    f0 = 100
    tau = 0.005
    snr = 5
    n = 1000
    window_type = "Hamming"

    # Create a sidebar with sliders to adjust the signal parameters
    st.sidebar.title("Signal Parameters")
    f0 = st.sidebar.slider("f0 (Hz)", 1, 500, 100)
    tau = st.sidebar.slider("tau (s)", 0.001, 0.1, 0.005, step=0.001)
    snr = st.sidebar.slider("SNR (dB)", -20, 20, 5)
    n = st.sidebar.slider("n", 100, 2000, 1000, step=100)
    window_type = st.sidebar.selectbox("Window Type", ["Hamming", "Hann"])

    # Create the signal
    t = np.arange(n) / fs
    x = np.sin(2 * np.pi * f0 * t) * np.exp(-t / tau)

    # Add noise to the signal
    noise = np.random.randn(n)
    noise_power = np.var(x) / (10**(snr / 10))
    noise *= np.sqrt(noise_power)
    y = x + noise

    # Create the replica signal
    htau = np.arange(-n/2, n/2) / fs
    replica = np.sin(2 * np.pi * f0 * htau) * np.exp(-htau / tau)

    nfft = int(2 ** np.ceil(np.log2(n)))
    # Apply the window function
    if window_type == "Hamming":
        win = hamming(n)
    else:
        win = hann(n)
    win = np.pad(win, (0, len(y) - len(win)), 'constant')
    y *= win
    replica *= win

    # Compute the FFT of the signals
    
    nfft = int(2 ** np.ceil(np.log2(n)))
    yfft = fft(y, nfft)
    rfft = fft(replica, nfft)

    # Compute the matched filter output
    eps = 1e-10
    time = -htau[0] + np.arange(nfft) / fs
    out = abs(ifft((rfft * np.conj(yfft)))) / (nfft)

    # Create the figure
    fig = plt.figure(figsize=(8, 6))
    plt.plot(time, out)
    plt.xlabel("Time (s)")
    plt.ylabel("Matched Filter Output")
    plt.title("Matched Filter Example")
    st.pyplot(fig)

if __name__ == "__main__":
    main()