import requests
from pprint import pprint
from requests import session

#Admin prompt to input Meraki API Key
API_KEY = input("Please enter the Meraki Dashboard API key: ")

url = "https://api.meraki.com/api/v1/organizations"

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
        
        #Iterates over the list "data" to access the keys stored in each mini dict
        print("Here is the different data you can query:")
        for keys in data:
            for key in keys.keys():
                print(f"{key.capitalize()}")
         
        #Allows the admin to input str to select which key to query
        while True:
            try:    
                admin_input = input ("What would you like to know?: ")
                org_name = [org[admin_input] for org in data]
                for admin_input in org_name:
                    print(f"{admin_input}")
                
            except Exception as ValueError:
                print ("Please input a valid entry")
            break        
            
    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)
