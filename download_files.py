import requests   
from dotenv import load_dotenv
import os

load_dotenv()

#Get File Information 

files_endpoint = 'https://api.infusionsoft.com/crm/rest/v1/files'
download_base_url = 'https://api.infusionsoft.com/crm/rest/v1/files/{}/download'
keap_access_token = os.getenv('ACCESS_TOKEN')
local_directory = '/Users/zacmfp/keap_migration_files'


# Step 1: Retrieve File Information
headers = {
    'Authorization': f'Bearer {keap_access_token}'
}
response = requests.get(files_endpoint, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Check if the 'files' key is present in the JSON response
    if 'files' in response.json():
        files_data = response.json()['files']

        # Step 2: Download Files
        for file_info in files_data:
            file_id = file_info['id']
            download_url = download_base_url.format(file_id)

            download_response = requests.get(download_url, headers=headers)

            # Extract filename from the Content-Disposition header
            content_disposition = download_response.headers.get('Content-Disposition')
            filename = content_disposition.split('=')[1] if content_disposition else f'file_{file_id}.pdf'

            # Save the file to the specified local directory
            with open(filename, 'wb') as file:
                file.write(download_response.content)

            print(f"File {filename} downloaded successfully.")
    else:
        print("No 'files' key found in the JSON response.")
else:
    print(f"Error: {response.status_code} - {response.text}")