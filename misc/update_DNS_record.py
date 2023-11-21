import requests
import sys
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Update DNS records in GoDaddy.')
    parser.add_argument('--domain', required=True, help='Domain name')
    parser.add_argument('--record-names', nargs='+',
                        required=True, help='List of record names')
    args = parser.parse_args()

    return args


def update_dns_record(domain, record_names):
    # Get my Public IP address #
    url = 'http://ipinfo.io'
    response = requests.get(url)
    new_ip = response.json()['ip']

    # GoDaddy API key and secret
    api_key = os.environ['api_key']
    api_secret = os.environ['api_secret']

    record_type = 'A'
    # Authenticate with GoDaddy API
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/@'
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
        raise Exception(f"response.json returned {response_json}")

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
    for record_name in record_names:
        url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}'
        response = requests.put(url, json=[data], headers=headers)

        # Check if the update was successful
        if response.status_code in range(200, 400):
            print(f'DNS record for {record_name} updated successfully')
        else:
            raise Exception(
                f"Error: GoDaddy API PUT request at {url} returned status code {response.status_code}")


if __name__ == "__main__":
    args = parse_args()
    update_dns_record(args.domain, args.record_names)
