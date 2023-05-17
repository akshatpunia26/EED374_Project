import streamlit as st
st.set_page_config(layout="wide")
import radarapp
import matchedapp


def main():
    st.title("EED374:Webapp for Radar Engineering Concepts")
    app = st.sidebar.selectbox("Select App", ["Radar Signal Processing", "Matched Filter App"])

    if app == "Radar Signal Processing":
        radarapp.main()
    else:
        matchedapp.main()

if __name__ == "__main__":
    main()