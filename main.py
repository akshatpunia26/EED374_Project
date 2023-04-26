import streamlit as st
import radarapp
import matchedapp

def main():
    st.title("EED374: Interactive Webapp for Matched Filtering and Radar Compression")
    app = st.sidebar.selectbox("Select App", ["Radar Signal Processing", "Matched Filter App"])

    if app == "Radar Signal Processing":
        radarapp.main()
    else:
        matchedapp.main()

if __name__ == "__main__":
    main()