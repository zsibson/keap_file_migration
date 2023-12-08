import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your Keap API credentials
client_id = os.getenv('KEAP_CLIENT_ID')
client_secret = os.getenv('KEAP_CLIENT_SECRET')
redirect_uri = os.getenv('KEAP_REDIRECT_URI')
access_token = os.getenv('KEAP_ACCESS_TOKEN')
refresh_token = os.getenv('KEAP_REFRESH_TOKEN')

# Base URL for Keap API
api_base_url = "https://api.infusionsoft.com/crm/rest/v1"

# Function to refresh access token using the refresh token
def refresh_access_token():
    refresh_url = "https://api.infusionsoft.com/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_encode(client_id + ':' + client_secret)}"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(refresh_url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get("access_token")

# Function to get all file IDs
def get_all_file_ids(access_token):
    files_url = f"{api_base_url}/files"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(files_url, headers=headers)
    return response.json()

# Function to download files to a local directory
def download_files(file_ids, directory_path):
    for file_id in file_ids:
        file_url = f"https://api.infusionsoft.com/crm/rest/v1/files/{file_id}/download"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(file_url, headers=headers)
        
        # Use a meaningful file name (you may extract it from the response headers)
        file_name = f"file_{file_id}.txt"
        
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)

# Helper function to encode client_id and client_secret for authorization header
def base64_encode(s):
    import base64
    return base64.b64encode(s.encode()).decode()

# Check if the access token is still valid, refresh if necessary
if not access_token:
    access_token = refresh_access_token()

# Get all file IDs from the Keap API
all_file_ids = get_all_file_ids(access_token)

# Specify the directory path for downloading files
directory_path = "downloaded_files"

# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

# Download files to the local directory
download_files(all_file_ids, directory_path)

print(f"All files downloaded successfully to {directory_path}")