import requests
import json

# Replace with your ngrok URL or server address
BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/farms/" # Replace with your ngrok url
PROFILE_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/" # Replace with your ngrok url

# Global variable to store the authentication token
TOKEN = None
USER_ID = None


def register_user():
    """Registers a new user and gets the token"""
    global TOKEN
    global USER_ID
    url = f"{PROFILE_BASE_URL}auth/register/"
    payload = {
        "username": "testuser3",
        "password": "testpassword",
        "email": "test3@example.com"
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

def get_all_farm_profiles():
    """Retrieves all farm profiles for the user."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = BASE_URL
    headers = {"Authorization": f"Token {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        farm_profiles = response.json()
        print(f"Get All Farm Profiles Success: {response.status_code} \n data: {farm_profiles}")
        return farm_profiles
    except requests.exceptions.RequestException as e:
        print(f"Error getting all farm profiles: {e}")
        return None

def get_farm_profile(farm_id):
    """Retrieves a specific farm profile by its ID."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return

    url = f"{BASE_URL}{farm_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        farm_profile = response.json()
        print(f"Get Farm Profile Success: {response.status_code} \n data: {farm_profile}")
        return farm_profile
    except requests.exceptions.RequestException as e:
        print(f"Error getting farm profile: {e}")
        return None

def update_farm_profile(farm_id):
    """Updates an existing farm profile."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = f"{BASE_URL}{farm_id}/"
    headers = {"Authorization": f"Token {TOKEN}", 'Content-Type': 'application/json'}
    payload = {
         "farmName": "Updated Farm Name",
        "farmLocation": "Updated Location",
        "farmSize": "10 acres",
        "soilType": "Sandy",
        "pHValue": 7.2,
        "currentCrop": "Rice",
        "futureCrop": "Maize",
        "irrigationSystem": "Rain-fed",
    }
    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        updated_farm_profile = response.json()
        print(f"Update Farm Profile Success: {response.status_code} \n data: {updated_farm_profile}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating farm profile: {e}")

def delete_farm_profile(farm_id):
    """Deletes a farm profile."""
    global TOKEN
    if TOKEN is None:
         print("Error: No token found, please register/login first")
         return
    url = f"{BASE_URL}{farm_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}

    try:
         response = requests.delete(url, headers=headers)
         response.raise_for_status()
         print(f"Delete Farm Profile Success: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting farm profile: {e}")


if __name__ == "__main__":
    register_user()
    login_user()
    # Create a farm profile
    created_farm = create_farm_profile()

    if created_farm:
        farm_id = created_farm['id'] #get the id of the created farm profile.

        # Get all farm profiles
        get_all_farm_profiles()

       #Get a single farm profile
        get_farm_profile(farm_id)

        # Update the farm profile
        update_farm_profile(farm_id)

        # Get all farm profiles
        get_all_farm_profiles()

        # Get the updated farm profile
        get_farm_profile(farm_id)

        # Delete the farm profile
        delete_farm_profile(farm_id)

        # Get all farm profiles again to confirm it is deleted
        get_all_farm_profiles()
    else:
        print("Error: could not create a farm profile")