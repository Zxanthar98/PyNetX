import requests
import getpass
import json

#defining the function to get assets from Hudu
def get_hudu_assets(api_key, base_url, asset_layout_id):

    #Setting the headers for the API request
    headers = {
        'x-api-key': api_key,
        'Accept': "application/json",
        'Content-Type': "application/json"  
}
    #Setting the parameters for the API request
    params = {
        'page_size': 999,
        'archived': False,
        'asset_layout_id': asset_layout_id,
    }

    #Making the API request to get assets
    #Using try/except to handle any errors that may occur during the request
    try:
        url = f'{base_url}/api/v1/assets'
        response = requests.get(url, headers=headers, params=params)

        #Checking if the response status code is 200 (OK)
        #If the response is successful, parse the JSON data
        if response.status_code == 200:
            data = response.json()
            assets = data['assets']
            asset_data = []
            #print(json.dumps(assets, indent=4)) 
            #Iterate over the assets to find the IP address
            #If the asset type is 'firewalls', get the IP address
            for asset in assets:
                asset_type = asset['asset_type']
                fields = asset['fields']
                #Iterate over the fields to find the IP address
                #If the field label is 'IP Address', get the value
                for field in fields:
                    if field.get('label') == 'Device is Active':
                        is_active = field.get('value')
                    if field.get('label') == 'IP Address':
                        host_ip = field.get('value')
                        if is_active == False: 
                            print(f"Asset {asset['name']} is not active. Skipping...")
                            continue                         
                        asset_data.append({"asset_types": asset_type, "asset_name": asset['name'], "ip_address": host_ip})
            #Return the list of assets with their IP addresses
            return asset_data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Allows the above custom function to be run as a standalone program for debugging and testing.
if __name__ == '__main__':
    API_KEY = getpass.getpass("Please enter your API key: ")
    base_url = "https://lifeflight.huducloud.com"
    asset_layout_id = 29

    asset_data = get_hudu_assets(API_KEY, base_url, asset_layout_id)