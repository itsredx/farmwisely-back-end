import requests
import json

# Replace with your ngrok URL or server address
BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/farms/"  # Replace with your ngrok url
PROFILE_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/"  # Replace with your ngrok url
ANALYTICS_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/analytics/"  # Replace with your ngrok url

# Global variable to store the authentication token
TOKEN = None
USER_ID = None


def register_and_login_user():
    """Registers a new user and logs it in getting the token"""
    global TOKEN
    global USER_ID
    url = f"{PROFILE_BASE_URL}auth/register/"
    register_payload = {
        "username": "testuser96",  # make sure that you are using the same user for all requests
        "password": "testpassword",
        "email": "test96@example.com"
    }
    try:
        response = requests.post(url, json=register_payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        TOKEN = data.get('token')
        USER_ID = data.get('user_id')
        print(f"User Registered Successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during register user: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding json")
        return False
    url = f"{PROFILE_BASE_URL}auth/login/"
    login_payload = {
        "username": "testuser96",  # make sure that you are using the same user for all requests
        "password": "testpassword"
    }
    try:
        response = requests.post(url, json=login_payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        TOKEN = data.get('token')
        USER_ID = data.get('user_id')
        print(f"User logged in Successfully: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error during login user: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding json")
        return False


def create_farm_profile():
    """Creates a new farm profile."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return

    url = BASE_URL
    headers = {"Authorization": f"Token {TOKEN}", 'Content-Type': 'application/json'}
    payload = {
        "farmName": "my farm",
        "farmLocation": "Kano Nigeria",
        "farmSize": "5 acres",
        "soilType": "Loamy",
        "pHValue": 6.5,
        "currentCrop": "Maize",
        "futureCrop": "Beans",
        "irrigationSystem": "Drip Irrigation",
        "latitude": 34.0522,  # Example latitude
        "longitude": -118.2437,  # Example longitude
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


def get_farm_analytics(farm_id, user_notes=None):
    """Fetches farm analytics from the API with optional user notes."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = f"{ANALYTICS_BASE_URL}{farm_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    params = {}
    if user_notes:
        params["notes"] = user_notes

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        analytics_data = response.json()
        print(f"Get Farm Analytics Success: {response.status_code}, data: {analytics_data}")
    except requests.exceptions.RequestException as e:
          print(f"Error getting farm analytics: {e}")
          try:
              print(f"Response body: {response.json()}")
          except:
             print(f"Response body: {response.content}")


if __name__ == "__main__":
    if register_and_login_user():
       # Create a farm profile
       created_farm = create_farm_profile()

       if created_farm:
          farm_id = created_farm['id']
          # Get analytics data without notes
          get_farm_analytics(farm_id)

          # Get analytics data with notes
          get_farm_analytics(farm_id, user_notes="Interested in data for maize")
       else:
          print("Could not create farm profile")
    else:
        print("Could not register and login user")