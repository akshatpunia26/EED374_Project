import streamlit as st
import radarapp
import matchedapp
st.set_page_config(layout="wide")

def main():
    st.title("EED374:Webapp for Radar Engineering Concepts")
    app = st.sidebar.selectbox("Select App", ["Radar Signal Processing", "Matched Filter App"])

    if app == "Radar Signal Processing":
        radarapp.main()
    else:
        matchedapp.main()

if __name__ == "__main__":
    main()