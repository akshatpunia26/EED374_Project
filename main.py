import streamlit as st
import radarapp
import matchedapp

def main():
    st.title("Radar Apps")

    app = st.sidebar.selectbox("Select App", ["Radar App", "Matched Filter App"])

    if app == "Radar App":
        radarapp.main()
    else:
        matchedapp.main()

if __name__ == "__main__":
    main()