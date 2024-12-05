# Cloudflare DNS Updater

This script automatically updates DNS records in Cloudflare with the current public IP address. It is designed for dynamic IP scenarios, ensuring that DNS records remain up-to-date.

---

## Features
- Fetches the current public IP address.
- Updates Cloudflare DNS records if the IP has changed.
- Supports multiple DNS records and zones via a configuration file (`conf.yaml`).

---

## Prerequisites
1. **Python 3.7 or higher** is required due to library dependencies.
2. A Cloudflare Global API Key (domain-specific API tokens **will not work**).
3. A configuration file (`conf.yaml`) containing the necessary DNS record details.

---

## Installation
1. Clone the repository or download the script:
    ```bash
    git clone https://github.com/Netanel-Iyov/Home-Server
    cd Home-Server/update_DNS_record
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Usage
Run the script with your Cloudflare Global API Key:
```bash
python update_DNS_record.py -k <your-cloudflare-global-api-key>
```