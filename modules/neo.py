import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils.nasa_api import NASA_API_KEY
import datetime

BASE_URL = "https://api.nasa.gov/neo/rest/v1"

def get_neo(start_date, end_date):
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY
    }
    response = requests.get(f"{BASE_URL}/feed", params=params)
    response.raise_for_status()
    return response.json()

def parse_neo(data):
    asteroids = []
    for date, neos in data["near_earth_objects"].items():
        for neo in neos:
            close_approach = neo["close_approach_data"][0]
            asteroids.append({
                "Nom": neo["name"],
                "Date": date,
                "Diamètre min (m)": round(neo["estimated_diameter"]["meters"]["estimated_diameter_min"]),
                "Diamètre max (m)": round(neo["estimated_diameter"]["meters"]["estimated_diameter_max"]),
                "Vitesse (km/h)": round(float(close_approach["relative_velocity"]["kilometers_per_hour"])),
                "Distance (km)": round(float(close_approach["miss_distance"]["kilometers"])),
                "Dangereux": "⚠️ Oui" if neo["is_potentially_hazardous_asteroid"] else "✅ Non",
                "Lien NASA": neo["nasa_jpl_url"]
            })
    return pd.DataFrame(asteroids).sort_values("Date")

def show():
    st.header("☄️ Astéroïdes proches de la Terre (NEO)")

    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input(
            "Date de début",
            value=datetime.date.today(),
            key="neo_start"
        )
    with col_end:
        end_date = st.date_input(
            "Date de fin",
            value=start_date + datetime.timedelta(days=7),
            min_value=start_date,
            max_value=start_date + datetime.timedelta(days=7),
            key="neo_end"
        )

    with st.spinner("Chargement des données..."):
        try:
            data = get_neo(start_date, end_date)
            df = parse_neo(data)
        except Exception as e:
            st.error(f"Erreur : {e}")
            return

    col1, col2, col3 = st.columns(3)
    col1.metric("☄️ Total astéroïdes", len(df))
    col2.metric("⚠️ Potentiellement dangereux", len(df[df["Dangereux"] == "⚠️ Oui"]))
    col3.metric("📅 Période", f"{start_date} → {end_date}")

    st.subheader("📊 Distance vs Taille")
    fig = px.scatter(
        df,
        x="Distance (km)",
        y="Diamètre max (m)",
        color="Dangereux",
        hover_name="Nom",
        size="Diamètre max (m)",
        color_discrete_map={"⚠️ Oui": "red", "✅ Non": "green"},
        labels={"Distance (km)": "Distance de passage (km)", "Diamètre max (m)": "Diamètre max (m)"}
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width='stretch')

    st.subheader("📋 Liste complète")
    st.dataframe(
        df.drop(columns=["Lien NASA"]),
        width='stretch'
    )