import streamlit as st
import requests
import pandas as pd
from utils.nasa_api import NASA_API_KEY
import datetime

BASE_URL = "https://api.nasa.gov/DONKI"

def get_solar_flares(start_date, end_date):
    params = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY
    }
    response = requests.get(f"{BASE_URL}/FLR", params=params)
    response.raise_for_status()
    return response.json()

def get_cme(start_date, end_date):
    params = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY
    }
    response = requests.get(f"{BASE_URL}/CME", params=params)
    response.raise_for_status()
    return response.json()

def get_activity_level(flares):
    if not flares:
        return "🟢 Calme", "green"
    
    classes = [f.get("classType", "A") for f in flares]
    if any(c.startswith("X") for c in classes):
        return "🔴 Extrême", "red"
    elif any(c.startswith("M") for c in classes):
        return "🟠 Modérée", "orange"
    elif any(c.startswith("C") for c in classes):
        return "🟡 Faible", "yellow"
    return "🟢 Calme", "green"

def show():
    st.header("☀️ Space Weather")

    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input(
            "Date de début",
            value=datetime.date.today() - datetime.timedelta(days=7),
            key="sw_start"
        )
    with col_end:
        end_date = st.date_input(
            "Date de fin",
            value=datetime.date.today(),
            key="sw_end"
        )

    with st.spinner("Chargement des données solaires..."):
        try:
            flares = get_solar_flares(start_date, end_date)
            cmes = get_cme(start_date, end_date)
        except Exception as e:
            st.error(f"Erreur : {e}")
            return

    # Niveau d'activité
    activity_label, _ = get_activity_level(flares)
    st.subheader(f"Niveau d'activité solaire : {activity_label}")

    # Métriques
    col1, col2 = st.columns(2)
    col1.metric("🔥 Éruptions solaires", len(flares))
    col2.metric("💨 Éjections de masse coronale", len(cmes))

    # Tableau éruptions
    st.subheader("🔥 Éruptions solaires")
    if flares:
        df_flares = pd.DataFrame([{
            "Date": f.get("beginTime", "N/A")[:10],
            "Heure début": f.get("beginTime", "N/A")[11:16],
            "Heure pic": f.get("peakTime", "N/A")[11:16] if f.get("peakTime") else "N/A",
            "Classe": f.get("classType", "N/A"),
            "Région active": f.get("activeRegionNum", "N/A"),
        } for f in flares])
        st.dataframe(df_flares, width='stretch')
    else:
        st.info("Aucune éruption solaire sur cette période.")

    # Tableau CME
    st.subheader("💨 Éjections de masse coronale (CME)")
    if cmes:
        df_cmes = pd.DataFrame([{
            "Date": c.get("startTime", "N/A")[:10],
            "Heure": c.get("startTime", "N/A")[11:16],
            "Note": c.get("note", "N/A")[:80] + "..." if c.get("note") and len(c.get("note", "")) > 80 else c.get("note", "N/A"),
        } for c in cmes])
        st.dataframe(df_cmes, width='stretch')
    else:
        st.info("Aucune CME sur cette période.")