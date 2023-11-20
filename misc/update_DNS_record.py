import requests
import sys
import os

# Get my Public IP address #
url = 'http://ipinfo.io'
response = requests.get(url)
new_ip = response.json()['ip']

# GoDaddy API key and secret
api_key = os.environ['api_key']
api_secret = os.environ['api_secret']

# GoDaddy details
domain = 'niyov.com'
record_name = 'jenkins'  # record name
record_type = 'A'  # record type

# Authenticate with GoDaddy API
url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}'
headers = {
    'Authorization': f'sso-key {api_key}:{api_secret}',
    'Content-Type': 'application/json'
}

# Get current DNS record details
response = requests.get(url, headers=headers)
if not response.status_code in range(200, 400):
    raise Exception(
        f"Error: GoDaddy API GET request at {url} returned status code {response.status_code}")

response_json = response.json()
if not response_json:
    raise Exception(f"response.hson returned {response_json}")

data = response.json()[0]

# Update the IP address in the DNS record
current_ip = data.get('data', None)
if not current_ip:
    raise Exception(
        f"Failed to fetch current DNS record details. Status code: {response.status_code}, Response: {response.text}")

# Check if IP change is needed
if current_ip == new_ip:
    print('IP was not changed')
    sys.exit(0)

# Set new IP Address
data['data'] = new_ip
response = requests.put(url, json=[data], headers=headers)

# Check if the update was successful
if response.status_code in range(200, 400):
    print(f'DNS record updated successfully')
else:
    raise Exception(
        f"Error: GoDaddy API PUT request at {url} returned status code {response.status_code}")
