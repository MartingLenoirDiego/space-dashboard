import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

def get_iss_position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    return {
        "lat": float(data["iss_position"]["latitude"]),
        "lon": float(data["iss_position"]["longitude"]),
        "timestamp": data["timestamp"]
    }

def get_astronauts():
    response = requests.get("http://api.open-notify.org/astros.json")
    response.raise_for_status()
    return response.json()["people"]

def show():
    st_autorefresh(interval=5000, key="iss_refresh")
    
    st.header("🛰️ ISS Tracker")

    position = get_iss_position()
    df = pd.DataFrame([{"lat": position["lat"], "lon": position["lon"], "name": "ISS"}])

    fig = px.scatter_geo(df, lat="lat", lon="lon", text="name", projection="natural earth")
    fig.update_traces(marker=dict(size=15, color="red", symbol="circle"))
    fig.update_layout(
        geo=dict(
            showland=True, landcolor="rgb(30, 30, 30)",
            showocean=True, oceancolor="rgb(10, 10, 50)",
            showlakes=True, lakecolor="rgb(10, 10, 50)",
            showcountries=True, countrycolor="rgb(80, 80, 80)",
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Position en temps réel")
        st.plotly_chart(fig, use_container_width=True)
        metrics = st.columns(2)
        metrics[0].metric("Latitude", f"{position['lat']:.4f}°")
        metrics[1].metric("Longitude", f"{position['lon']:.4f}°")

    with col2:
        st.subheader("👨‍🚀 Astronautes à bord")
        astronauts = get_astronauts()
        for person in astronauts:
            st.markdown(f"- **{person['name']}** ({person['craft']})")

    st.caption("🔄 Position mise à jour automatiquement toutes les 5 secondes")