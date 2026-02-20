import streamlit as st
from utils.nasa_api import get_apod
import datetime

def show():
    st.header("🌌 Astronomy Picture of the Day")

    date = st.date_input(
        "Choisir une date",
        value=datetime.date.today(),
        min_value=datetime.date(1995, 6, 16),  # première APOD
        max_value=datetime.date.today(),
        key="apod_date"
    )

    with st.spinner("Chargement..."):
        try:
            data = get_apod(date)
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")
            return

    st.subheader(data["title"])
    st.caption(f"📅 {data['date']}")

    if data["media_type"] == "image":
        st.image(data["url"], width="stretch")
    elif data["media_type"] == "video":
        st.video(data["url"])

    with st.expander("📖 Explication",expanded=False):
        st.write(data["explanation"])

    if "copyright" in data:
        st.caption(f"© {data['copyright']}")