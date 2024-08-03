import json
import requests
from pprint import pprint

#Admin prompt to input Meraki API Key
API_KEY = input("Please enter the Meraki Dashboard API key: ")


url = "https://api.meraki.com/api/v1/organizations/90527/networks"

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Accept': "application-json",
    'content-Type' : "application-json"    
}

try:
    #Send GET request
    response = requests.get (url, headers=headers)
    
    #Check if request was successful 
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        
        print("Here is the different data you can query:")
        for keys in data:
            for key in keys.keys():
                print(key.capitalize())
        
        while True:
            try:    
                admin_input = input ("What would you like to know?: ")
                org_name = [org[admin_input] for org in data]
                for admin_input in org_name:
                    print(admin_input)
                
            except Exception as ValueError:
                print ("Please input a valid entry")
            break   
        
    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)