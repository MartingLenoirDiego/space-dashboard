# 🚀 Space Dashboard

A real-time interactive space data dashboard built with Python and Streamlit, powered by NASA's public APIs.

## 🌐 Live Demo
[space-dashboard.streamlit.app]([https://your-app-url.streamlit.app](https://space-dashboard.streamlit.app/)) 

## 📸 Features

- 🌌 **APOD** — Astronomy Picture of the Day with date picker
- 🛰️ **ISS Tracker** — Real-time ISS position on an interactive globe, auto-refreshed every 5 seconds
- ☀️ **Space Weather** — Solar flares and coronal mass ejections monitor via NASA DONKI API
- ☄️ **NEO Tracker** — Near-Earth asteroids with size, speed, distance and hazard visualization

## 🛠️ Tech Stack

- **Python 3.12**
- **Streamlit** — UI framework
- **Plotly** — Interactive charts and maps
- **Pandas** — Data manipulation
- **NASA APIs** — APOD, ISS, DONKI, NeoWs

## 🚀 Run Locally
```bash
git clone https://github.com/MartingLenoirDiego/space-dashboard.git
cd space-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file at the root :
```
NASA_API_KEY=your_api_key_here
```

Get your free API key at [api.nasa.gov](https://api.nasa.gov)
```bash
streamlit run app.py
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `NASA_API_KEY` | NASA Open API key (free at api.nasa.gov) |

## 📁 Project Structure
```
space-dashboard/
├── app.py              # Main entry point
├── modules/
│   ├── apod.py         # Astronomy Picture of the Day
│   ├── iss.py          # ISS Tracker
│   ├── space_weather.py# Space Weather
│   └── neo.py          # Near-Earth Objects
├── utils/
│   └── nasa_api.py     # NASA API helpers
├── .env                # API keys (not committed)
└── requirements.txt
```

## 📄 License
MIT
