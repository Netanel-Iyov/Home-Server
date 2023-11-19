import requests
import sys
import os

# Get my Public IP address #
url = 'http://ipinfo.io'
response = requests.get(url)
new_ip = response.json()['ip']

# Replace with your GoDaddy API key and secret
api_key = os.environ['api_key']
api_secret = os.environ['api_secret']

# Replace with your GoDaddy domain and record details
domain = 'niyov.com'
record_name = '@'  # Replace with your record name
record_type = 'A'  # Replace with your record type (A, CNAME, etc.)

# Authenticate with GoDaddy API
url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}'
headers = {
    'Authorization': f'sso-key {api_key}:{api_secret}',
    'Content-Type': 'application/json'
}

# Get current DNS record details
response = requests.get(url, headers=headers)
data = response.json()[0]

# Update the IP address in the DNS record
current_ip = data.get('data', None)
if not current_ip:
    print(
        f'Failed to fetch current DNS record details. Status code: {response.status_code}, Response: {response.text}')
    sys.exit(1)

# Check if IP change is needed
if current_ip == new_ip:
    print('IP was not changed')
    sys.exit(0)

# Set new IP Address
data['data'] = new_ip
response = requests.put(url, json=[data], headers=headers)

# Check if the update was successful
if response.status_code == 200:
    print(f'DNS record updated successfully')
else:
    print(
        f'Failed to update DNS record. Status code: {response.status_code}, Response: {response.text}')
    sys.exit(1)
