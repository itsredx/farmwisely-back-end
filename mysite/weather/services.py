import requests
import json
from django.conf import settings

def fetch_weather_data(latitude, longitude):
    """Fetches weather data from the Visual Crossing API."""
    api_key = settings.VISUAL_CROSSING_API_KEY
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    url = f"{base_url}{latitude},{longitude}?unitGroup=metric&include=days,hours,alerts,current&key={api_key}&contentType=json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None