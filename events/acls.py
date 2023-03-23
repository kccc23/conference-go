from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    params = {
        "per_page": 1,
        "query": city + " " + state,
    }
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture": None}


def get_weather_data(city, state):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city},{state},US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    response = requests.get(url, params=params)
    content = response.json()
    try:
        lat = content[0]["lat"]
        lon = content[0]["lon"]
    except (KeyError, IndexError):
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    response = requests.get(url, params=params)
    content = response.json()
    try:
        return {
            "description": content["weather"][0]["description"],
            "temp": content["main"]["temp"],
        }
    except (KeyError, IndexError):
        return None
