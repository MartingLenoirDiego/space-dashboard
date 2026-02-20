import streamlit as st
from modules import apod, iss

st.set_page_config(
    page_title="Space Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 Space Dashboard")
page = st.sidebar.radio("Navigation", ["APOD", "ISS Tracker", "Space Weather"])

main = st.container()

with main:
    if page == "APOD":
        apod.show()
    elif page == "ISS Tracker":
        iss.show()
    elif page == "Space Weather":
        st.info("Coming soon ☀️")