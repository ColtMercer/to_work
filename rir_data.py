import requests
import pandas as pd

# Replace 'your_api_token' with your actual Nautobot API token
api_token = 'your_api_token'
api_base_url = 'https://nautobot.example.com/api/'

headers = {
    'Authorization': f'Token {api_token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def get_data(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_all_data(endpoint):
    results = []
    url = api_base_url + endpoint
    while url:
        data = get_data(url)
        results.extend(data['results'])
        url = data['next']
    return results

rir_data = get_all_data('ipam/rirs/')

public_rirs = [rir for rir in rir_data if rir['is_private'] == False]

data_rows = []

for rir in public_rirs:
    aggregate_data = get_all_data(f'ipam/aggregates/?rir_id={rir["id"]}')

    for aggregate in aggregate_data:
        prefix_data = get_all_data(f'ipam/prefixes/?within={aggregate["prefix"]}')

        for prefix in prefix_data:
            ip_data = get_all_data(f'ipam/ip-addresses/?within={prefix["prefix"]}')

            for ip in ip_data:
                device_name = ip['assigned_object']['device']['name'] if ip['assigned_object'] and ip['assigned_object']['device'] else None
                interface_name = ip['assigned_object']['name'] if ip['assigned_object'] else None

                data_rows.append({
                    'rir': rir['name'],
                    'aggregate': aggregate['prefix'],
                    'prefix': prefix['prefix'],
                    'ip_address': ip['address'],
                    'device': device_name,
                    'interface': interface_name,
                })

df = pd.DataFrame(data_rows)
print(df)
