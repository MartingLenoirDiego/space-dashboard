import requests
import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
BASE_URL = "https://api.nasa.gov"

def get_apod(date=None):
    params = {
        "api_key": NASA_API_KEY,
    }
    if date:
        params["date"] = date.strftime("%Y-%m-%d")
    
    response = requests.get(f"{BASE_URL}/planetary/apod", params=params)
    response.raise_for_status()
    return response.json()