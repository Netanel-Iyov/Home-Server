from cloudflare import Cloudflare
import requests
import argparse
import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api-key", required=True, help="The Cloudflare global API key to use. NOTE: Domain-specific API tokens will NOT work!")
    args = parser.parse_args()

    with open('conf.yaml', 'r') as file:
        config = yaml.safe_load(file)

    url = 'http://ipinfo.io'
    response = requests.get(url)
    current_ip = response.json()['ip']

    # Initialize Cloudflare API client
    cf = Cloudflare(
        api_email=config['email'],
        api_key=args.api_key
    )


    # Get zone ID (for the domain). This is why we need the API key and the domain API token won't be sufficient
    for dns_record in config['dns_records']:
        hostname, zone_name, record_type = dns_record['hostname'], dns_record['zone_name'], dns_record['record_type']

        zone = cf.zones.list(name=zone_name)
        if not zone.result:
            print(f"Could not find CloudFlare zone {zone_name}, please check domain: {hostname}, with zone {zone_name}")
            continue
        zone_id = zone.result[0].id

        try:
            # Fetch existing A record
            a_record = cf.dns.records.list(zone_id=zone_id, name=hostname, type=record_type).result[0]
        except IndexError:
            print(f"Could not record, please check domain: {hostname}, with zone {zone_name}")
            continue
        
        # Update record & save to cloudflare
        if current_ip != a_record.content:
            try: 
                a_record.content = current_ip
                cf.dns.records.update(dns_record_id=a_record.id, zone_id=zone_id, content=current_ip, name=a_record.name, type=a_record.type, proxied=a_record.proxied)
                print(f"Successfully updated DNS record for {hostname}.")         
            except Exception as e:
                print(f"An unknown exception occured: {e}.")
        else:
            print(f"No need to update DNS record for {hostname}.")
