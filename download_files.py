import requests   
from dotenv import load_dotenv
import os

load_dotenv()

#Authentication

client_id = os.getenv('KEAP_CLIENT_ID')
client_secret = os.getenv('KEAP_CLIENT_SECRET')
scope = 'full'

# Redirect to Keap for Authentication 

ngrok_url = 'https://475f-69-146-65-82.ngrok-free.app'
redirect_uri = f'{ngrok_url}/callback'

authorization_url = 'https://accounts.infusionsoft.com/app/oauth/authorize'
authorization_params = {
    'client_id' : client_id,
    'redirect_uri' : redirect_uri,
    'response_type' : 'code', 
    'scope' : scope
}

authorization_response = requests.get(authorization_url, params=authorization_params)

# Assuming you have a web application, redirect the user to the authorization URL
# or print the URL and have the user manually visit it

# Example print statement for manual user visit
print("Visit the following URL to authorize your application:")
print(authorization_response.url)

# Capture the authorization code from the redirected URL or user input
authorization_code = input("Enter the authorization code: ")

# Step 2: Request an access token using the authorization code
token_url = 'https://api.infusionsoft.com/token'
token_payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri
}

token_response = requests.post(token_url, data=token_payload)

# Check if the response is successful
if token_response.status_code == 200:
    # Retrieve the access token from the response
    access_token = token_response.json().get('access_token')

    # Now you can use the obtained access token to make API requests
    api_url = 'https://api.infusionsoft.com/crm/rest/v1/files'  # Replace with your desired API endpoint
    api_headers = {
        'Authorization': f'Bearer {keap_access_token}'
    }

    # Example: Make an API request using the obtained access token
    api_response = requests.get(api_url, headers=api_headers)

    print(api_response.json())  # Print the API response
else:
    print(f"Error: {token_response.status_code} - {token_response.text}")


# #Get File Information 

# files_endpoint = 'https://api.infusionsoft.com/crm/rest/v1/files'
# download_base_url = 'https://api.infusionsoft.com/crm/rest/v1/files/{}/download'
# keap_access_token = os.getenv("ACCESS_TOKEN")
# local_directory = '/Users/zacmfp/keap_migration_files'


# # Step 1: Retrieve File Information
# headers = {
#     'Authorization': f'Bearer {keap_access_token}'
# }
# response = requests.get(files_endpoint, headers=headers)

# # Check if the response is successful
# if response.status_code == 200:
#     # Check if the 'files' key is present in the JSON response
#     if 'files' in response.json():
#         files_data = response.json()['files']

#         # Step 2: Download Files
#         for file_info in files_data:
#             file_id = file_info['id']
#             download_url = download_base_url.format(file_id)

#             download_response = requests.get(download_url, headers=headers)

#             # Extract filename from the Content-Disposition header
#             content_disposition = download_response.headers.get('Content-Disposition')
#             filename = content_disposition.split('=')[1] if content_disposition else f'file_{file_id}.pdf'

#             # Save the file to the specified local directory
#             with open(filename, 'wb') as file:
#                 file.write(download_response.content)

#             print(f"File {filename} downloaded successfully.")
#     else:
#         print("No 'files' key found in the JSON response.")
# else:
#     print(f"Error: {response.status_code} - {response.text}")