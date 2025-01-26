import requests
import json

# Replace with your ngrok URL or server address
BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/farms/"  # Replace with your ngrok url
PROFILE_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/"  # Replace with your ngrok url
WEATHER_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/weather/" # Replace with your ngrok url

# Global variable to store the authentication token
TOKEN = None
USER_ID = None


def register_user():
    """Registers a new user and gets the token"""
    global TOKEN
    global USER_ID
    url = f"{PROFILE_BASE_URL}auth/register/"
    payload = {
        "username": "testuser5",
        "password": "testpassword",
        "email": "test5@example.com"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        TOKEN = data.get('token')
        USER_ID = data.get('user_id')
        print(f"User Registered Successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during register user: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding json")

def login_user():
    """Logs in a user and gets the token"""
    global TOKEN
    global USER_ID
    url = f"{PROFILE_BASE_URL}auth/login/"
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        TOKEN = data.get('token')
        USER_ID = data.get('user_id')
        print(f"User logged in Successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during login user: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding json")


def create_farm_profile():
    """Creates a new farm profile."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return

    url = BASE_URL
    headers = {"Authorization": f"Token {TOKEN}", 'Content-Type': 'application/json'}
    payload = {
        "farmName": "Test Farm 1",
        "farmLocation": "Test Location 1",
        "farmSize": "5 acres",
        "soilType": "Loamy",
        "pHValue": 6.5,
        "currentCrop": "Maize",
        "futureCrop": "Beans",
        "irrigationSystem": "Drip Irrigation",
          "latitude": 34.0522,  # Example latitude
        "longitude": -118.2437, # Example longitude
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        farm_profile = response.json()
        print(f"Farm Profile Created Successfully: {response.status_code}, \n data:{farm_profile}")
        return farm_profile
    except requests.exceptions.RequestException as e:
        print(f"Error creating farm profile: {e}")
        return None


def get_weather_data(latitude, longitude):
    """Fetches weather data using the new weather API endpoint."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return

    url = f"{WEATHER_BASE_URL}{latitude}/{longitude}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        weather_data = response.json()
        print(f"Get Weather Data Success: {response.status_code} \n data: {weather_data}")
    except requests.exceptions.RequestException as e:
        print(f"Error getting weather data: {e}")


if __name__ == "__main__":
    register_user()
    login_user()
    # Create a farm profile
    created_farm = create_farm_profile()

    if created_farm:
        latitude = created_farm['latitude']
        longitude = created_farm['longitude']

        # Get Weather Data
        get_weather_data(latitude, longitude)
    else:
      print("Error creating a farm profile")