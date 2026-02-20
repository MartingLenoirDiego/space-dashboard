import streamlit as st
from modules import apod

st.set_page_config(
    page_title="Space Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 Space Dashboard")
page = st.sidebar.radio("Navigation", ["APOD", "ISS Tracker", "Space Weather"])

if page == "APOD":
    apod.show()
elif page == "ISS Tracker":
    st.info("Coming soon 🛰️")
elif page == "Space Weather":
    st.info("Coming soon ☀️")