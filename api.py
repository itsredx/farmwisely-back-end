import requests
import json

# Replace with your ngrok URL or server address
BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/" #replace with the actual url

# Global variable to store the authentication token
TOKEN = None
USER_ID = None


def register_user():
    """Registers a new user and gets the token"""
    global TOKEN
    global USER_ID
    url = f"{BASE_URL}auth/register/"
    payload = {
        "username": "testuser22",
        "password": "testpassword",
        "email": "test2@example.com"
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
    url = f"{BASE_URL}auth/login/"
    payload = {
        "username": "testuser2",
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


def get_profile():
    """Retrieves the user profile."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = f"{BASE_URL}profile/"
    headers = {"Authorization": f"Token {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        profile_data = response.json()
        print(f"Get Profile Data Success: {response.status_code} \n profile data:{profile_data}")
    except requests.exceptions.RequestException as e:
        print(f"Error during get profile: {e}")

def update_profile():
    """Updates the user profile."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = f"{BASE_URL}profile/"
    headers = {"Authorization": f"Token {TOKEN}", 'Content-Type': 'application/json'}
    payload = {
        "name": "Musa Muhammad",
        "email": "musa@example.com",
        "phoneNumber": "505-123-4567",
        "measurementUnit": "imperial",
        "weatherAlerts": False,
        "cropGrowthUpdates": True,
        "farmTaskReminders": False,
    }
    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        updated_profile = response.json()
        print(f"Update Profile Data Success: {response.status_code} \n updated profile: {updated_profile}")
    except requests.exceptions.RequestException as e:
        print(f"Error during update profile: {e}")

if __name__ == "__main__":
    register_user()
    login_user()
    get_profile()
    update_profile()
    get_profile() #get updated profile to see changes