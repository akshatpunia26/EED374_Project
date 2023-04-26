import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title('Radar Signal Processing: Pulse Compression and Range Calculation')

    st.markdown("""
This Streamlit app demonstrates pulse compression and range calculation in radar signal processing. Users can adjust various parameters such as pulse width, bandwidth, number of scatterers, minimum range, receiver range, and carrier frequency to generate radar signals and visualize their compressed echo signals.

**Example input parameters:**
- Pulse width: 0.01 s
- Bandwidth: 1 GHz
- Number of scatterers: 3
- Minimum range: 150,000 m
- Receiver range: 30 m
- Carrier frequency: 5.6 GHz
- Window type: Hamming

**Expected results:**
- Uncompressed echo signal plot with zero delay coinciding with minimum range
- Compressed echo signal plot with zero delay coinciding with minimum range
""")


    # Define parameters
    taup = st.slider('Pulse Width (s)', 0.001, 0.1, 0.01, 0.001)
    b = st.slider('Bandwidth (Hz)', 1e6, 1e10, 1e9, 1e6)
    nscat = st.slider('Number of Scatterers', 1, 10, 3, 1)
    rmin = st.slider('Minimum Range (m)', 10000, 500000, 150000, 10000)
    rrec = st.slider('Receiver Range (m)', 10, 100, 30, 1)
    f0 = st.slider('Carrier Frequency (Hz)', 1e9, 10e9, 5.6e9, 1e9)
    scat_range = np.linspace(rmin, rmin + 1000, nscat)  # Linearly spaced scatterer ranges
    winid = st.selectbox('Window Type', ('Rectangular', 'Hamming', 'Kaiser'))
    scat_rcs = np.ones(nscat)  # Constant radar cross-section for all scatterers

    # Set constants and initialize variables
    eps = 1.0e-16  # Epsilon
    htau = taup / 2.  # Half pulse width
    c = 3e8  # Speed of light
    trec = 2. * rrec / c  # Time delay
    n = int(2. * trec * b)  # Number of samples
    m = int(np.ceil(np.log2(n)))  # Power of 2
    nfft = 2**m  # Number of FFT points
    x = np.zeros((nscat, nfft), dtype=np.complex_)  # Initialize signal
    y = np.zeros(nfft, dtype=np.complex128) # Initialize compressed echo signal

    # Generate window
    if winid == 'Rectangular':
        win = np.ones(nfft)
    elif winid == 'Hamming':
        win = np.hamming(nfft)
    elif winid == 'Kaiser':
        win = np.kaiser(nfft, np.pi)

    # Calculate maximum range
    deltar = c / 2. / b
    max_rrec = deltar * nfft / 2.
    maxr = np.max(scat_range) - rmin

    # Generate signal
    deltat = taup / nfft
    t = np.arange(0, taup - eps, deltat)
    uplimit = t.size
    for j in range(nscat):
        psi1 = 4. * np.pi * scat_range[j] * f0 / c - 4. * np.pi * b * scat_range[j] * scat_range[j] / c / c / taup
        psi2 = (4. * np.pi * b * scat_range[j] / c / taup) * t
        x[j, :uplimit] = scat_rcs[j] * np.exp(1j * psi1 + 1j * psi2)
        y += x[j, :]

    # Plot uncompressed signal
    fig1, ax1 = plt.subplots()
    ax1.plot(t, np.real(y), 'k')
    ax1.set_xlabel('Relative delay - seconds')
    ax1.set_ylabel('Uncompressed echo')
    ax1.set_title('Zero delay coincides with minimum range')

    # Apply window and perform FFT
    ywin = y * win
    yfft = np.fft.fft(ywin, nfft) / nfft
    out = np.fft.fftshift(np.abs(yfft))

    # Plot compressed echo signal
    fig2, ax2 = plt.subplots()
    time = np.linspace(-htau, htau-deltat, nfft)
    ax2.plot(time, out, 'k')
    ax2.set_xlabel('Relative delay - seconds')
    ax2.set_ylabel('Compressed echo')
    ax2.set_title('Zero delay coincides with minimum range')
    ax2.grid()

    # Display plots
    st.pyplot(fig1)
    st.pyplot(fig2)
if __name__ == "__main__":
    main()