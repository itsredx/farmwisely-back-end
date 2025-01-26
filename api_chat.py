import requests
import json

# Replace with your ngrok URL or server address
BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/farms/"  # Replace with your ngrok url
PROFILE_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/"  # Replace with your ngrok url
CHAT_BASE_URL = "https://59f3-35-236-193-48.ngrok-free.app/api/chat/"  # Replace with your ngrok url


# Global variable to store the authentication token
TOKEN = None
USER_ID = None


def register_user():
    """Registers a new user and gets the token"""
    global TOKEN
    global USER_ID
    url = f"{PROFILE_BASE_URL}auth/register/"
    payload = {
        "username": "testboy1",
        "password": "testpassword",
        "email": "testboy1@example.com"
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
        "username": "testboy1",
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

def create_chat_message(farm_id, message, chat_title = None):
    """Creates a new chat message."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return

    url = f"{CHAT_BASE_URL}{farm_id}/"
    headers = {"Authorization": f"Token {TOKEN}", 'Content-Type': 'application/json'}
    payload = {
        "message": message,
    }
    if chat_title:
        payload["chat_title"] = chat_title
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        chat_history = response.json()
        print(f"Chat Message Created Successfully: {response.status_code}, \n data: {chat_history}")
        return chat_history
    except requests.exceptions.RequestException as e:
        print(f"Error creating chat message: {e}")
        try:
            print(f"Response Body: {response.json()}")
        except:
            print(f"Response Body: {response.content}")
        return None


def get_all_chat_histories():
    """Retrieves all chat histories for the user."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return

    url = f"{CHAT_BASE_URL}"
    headers = {"Authorization": f"Token {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        chat_histories = response.json()
        print(f"Get All Chat Histories Success: {response.status_code}, data: {chat_histories}")
        return chat_histories
    except requests.exceptions.RequestException as e:
        print(f"Error getting all chat histories: {e}")
        return None

def get_chat_history(chat_history_id):
    """Retrieves a specific chat history by its ID."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return
    url = f"{CHAT_BASE_URL}{chat_history_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        chat_history = response.json()
        print(f"Get Chat History Success: {response.status_code}, data: {chat_history}")
        return chat_history
    except requests.exceptions.RequestException as e:
        print(f"Error getting a chat history: {e}")
        return None
def delete_chat_history(chat_history_id):
    """Deletes a chat history."""
    global TOKEN
    if TOKEN is None:
        print("Error: No token found, please register/login first")
        return
    url = f"{CHAT_BASE_URL}{chat_history_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    try:
         response = requests.delete(url, headers=headers)
         response.raise_for_status()
         print(f"Delete Chat History Success: {response.status_code}")
         return True
    except requests.exceptions.RequestException as e:
        print(f"Error deleting a chat history: {e}")
        return False

if __name__ == "__main__":
    register_user()
    login_user()
     # Create a farm profile
    created_farm = create_farm_profile()
    if created_farm:
        farm_id = created_farm['id']  # Get the id of the created farm profile.
        # Create a chat message
        chat_history_1 = create_chat_message(farm_id, "How to grow tomato?", "First Chat")
        chat_history_2 = create_chat_message(farm_id, "What about beans?", "First Chat")
        chat_history_3 = create_chat_message(farm_id, "What about maize?", "Second Chat")
        if chat_history_1 and chat_history_2 and chat_history_3:
              # Get all chat histories
            get_all_chat_histories()
            # Get a single chat history
            get_chat_history(chat_history_1['id'])
             # Delete a chat history
            delete_chat_history(chat_history_1['id'])
           # Get all chat histories again to see if its deleted
            get_all_chat_histories()
        else:
           print("Could not create chat messages")
    else:
       print("Could not create a farm profile")