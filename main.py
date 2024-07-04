from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import requests
import time
from functools import lru_cache

app = FastAPI()


API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "ee7036077ff115f4e0a8c12615218478"


class WeatherData(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature: float
    description: str
    weather_type: str


def get_weather_data(lat: float, lon: float) -> dict:
    response = requests.get(API_URL, params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ville non trouvée ou requête échouée")
    return response.json()


@lru_cache(maxsize=10)
def get_cached_weather_data(lat: float, lon: float) -> WeatherData:
    data = get_weather_data(lat, lon)
    return WeatherData(
        city=data["name"],
        latitude=lat,
        longitude=lon,
        temperature=data["main"]["temp"],
        description=data["weather"][0]["description"],
        weather_type=data["weather"][0]["main"]
    )

@app.get("/weather", response_model=WeatherData)
def get_weather(lat: float, lon: float):
    return get_cached_weather_data(lat, lon)

@app.get("/weather/type", response_model=WeatherData)
def get_weather_by_type(lat: float, lon: float, weather_type: str):
    data = get_cached_weather_data(lat, lon)
    if data.weather_type.lower() != weather_type.lower():
        raise HTTPException(status_code=404, detail="Type de météo non trouvé pour cette localisation")
    return data

def cache_cleanup():
    while True:
        time.sleep(3600)  
        get_cached_weather_data.cache_clear()

import threading
threading.Thread(target=cache_cleanup, daemon=True).start()

