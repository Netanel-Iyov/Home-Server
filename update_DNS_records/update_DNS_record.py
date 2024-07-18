from cloudflare import Cloudflare
import requests
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=True, help="The Cloudflare login email to use")
    parser.add_argument("-n", "--hostnames", required=True, nargs='+', help="The hostname to update, e.g. mydyndns.mydomain.com")
    parser.add_argument("-k", "--api-key", required=True, help="The Cloudflare global API key to use. NOTE: Domain-specific API tokens will NOT work!")
    args = parser.parse_args()

    url = 'http://ipinfo.io'
    response = requests.get(url)
    current_ip = response.json()['ip']

    # Initialize Cloudflare API client
    cf = Cloudflare(
        api_email=args.email,
        api_key=args.api_key
    )

    # Get zone ID (for the domain). This is why we need the API key and the domain API token won't be sufficient
    for hostname in args.hostnames:
        zone_name = '.'.join(hostname.split('.')[-2:])
        zone = cf.zones.list(name=zone_name)
        if not zone.result:
            print(f"Could not find CloudFlare zone {zone_name}, please check domain {args.hostnames}.")
            continue
        zone_id = zone.result[0].id

        # Fetch existing A record
        a_record = cf.dns.records.list(zone_id=zone_id, name=hostname, type="A").result[0]

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
