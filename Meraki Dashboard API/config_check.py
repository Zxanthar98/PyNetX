import requests
from requests import session
import getpass
import json
from Templates.LifeFlighteLock import eLock_ssid_config
from Templates.LifeFlightGuest import guest_ssid_config

#Admin prompt to input Meraki API Key
API_KEY = getpass.getpass("Please enter the Meraki Dashboard API key: ")

org_id_url = "https://api.meraki.com/api/v1/organizations"

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Accept': "application-json",
    'content-Type' : "application-json"    
}


ssid_config = {
    'enabled': True,
    'dot11r': {
        'enabled': False,
        'adaptive': False
    },
    'encryptionMode': 'wpa',
    'wpaEncryptionMode': 'WPA2 only'
}

try:
    #Send GET request to get the organization ID
    response = requests.get (org_id_url, headers=headers)
    
    #Check if request was successful
    if response.status_code == 200:
        #Parse JSON response
        data = response.json()
        #print(json.dumps(data, indent=4))  
        org_id = data[0]['id']
        #clear the response variable by reassigning it to an empty list
        response = []

        #get a list of networks in the organization
        response = requests.get (f"https://api.meraki.com/api/v1/organizations/{org_id}/networks", headers=headers)
        #parse JSON response
        networks = response.json()
        #print(json.dumps(networks, indent=4))
        response = []
        for network in networks:
            network_id = network['id']
            network_name = network['name']
            network_type = network['productTypes']
            #print(f"Network ID: {network_id} Network Name: {network_name} Network Type: {network_type}")
            if  'wireless' in network_type:
                response = requests.get (f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids", headers=headers)
                ssids =  response.json()  
                for ssid in ssids:
                    ssid_names = ssid['name']
                    if 'Unconfigured' in ssid['name']:
                        continue
                    #print (json.dumps(ssid_names, indent=2))
                    if 'eLock' in ssid['name'] and network_name == 'Spare008': 
                        #print (f"SSID Name: {ssid_names} Network Name: {network_name} Network ID: {network_id}")
                        put_url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids/"
                        put_response = requests.put(put_url, headers=headers, json=ssid_config)       


    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)