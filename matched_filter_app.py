import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def matched_filter(signal, template):
    # Compute the matched filter response
    corr = np.correlate(signal, template, mode='same')
    return corr

st.title('Matched Filter Demo')

# Upload the CSV file
st.header('Upload CSV file')
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    signal = data['signal'].values
    template = data['template'].values

    # Apply the matched filter
    mf_response = matched_filter(signal, template)

    # Visualize the results
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    ax[0].plot(signal)
    ax[0].set_title('Original signal')
    ax[1].plot(mf_response)
    ax[1].set_title('Matched filter response')
    st.pyplot(fig)