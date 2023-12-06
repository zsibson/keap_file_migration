import requests   
from dotenv import load_dotenv
load_dotenv() 

#Get File Information 

files_endpoint = 'https://api.infusionsoft.com/crm/rest/v1/files'
download_base_url = 'https://api.infusionsoft.com/crm/rest/v1/files/{}/download'
keap_access_token = 'ACCESS_TOKEN'
local_directory = '/Users/zacmfp/keap_migration_files'


headers = {
    'Authorization': f'Bearer {keap_access_token}'
}
response = requests.get(files_endpoint, headers=headers)
files_data = response.json()['files'] 

#Download Files 

for file_info in files_data:
    file_id = file_info['id']
    download_url = download_base_url.format(file_id)

    download_response = requests.get(download_url, headers=headers)

    # Extract filename from the Content-Disposition header
    content_disposition = download_response.headers.get('Content-Disposition')
    filename = content_disposition.split('=')[1] if content_disposition else f'file_{file_id}.pdf'

    # Save the file to the specified local directory
    local_path = local_directory + filename
    with open(local_path, 'wb') as file:
        file.write(download_response.content)

print(f"File {filename} downloaded successfully to {local_path}.")