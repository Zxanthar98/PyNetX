import requests
from pprint import pprint
from requests import session
import getpass

#Admin prompt to input Meraki API Key
API_KEY = getpass.getpass("Please enter the Meraki Dashboard API key: ")

networkID = "N_616430198996351386"

url = f"https://api.meraki.com/api/v1/networks/{networkID}/wireless/ssids"

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Accept': "application-json",
    'content-Type' : "application-json"    
}

try:
    #Send GET request
    response = requests.get (url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        for keys in data:
            name = data
            print(f"SSID: {name}")
                
                
    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)        