import requests
from pprint import pprint
from requests import session
import getpass

#Admin prompt to input Meraki API Key
API_KEY = getpass.getpass("Please enter the Meraki Dashboard API key: ")

Prettylines = ("---------------------------------------")

org_id = 90527

url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"

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
    
    #Checks to see that the list of data isn't empty   
    if len(data) > 0:    
        print(f"Here is the different data you can query:\n{Prettylines}")
        #Pulls data from position zero in the dict
        first_network_keys = data[0].keys()
        for key in first_network_keys:
            print(f"{key.capitalize()}")
        
        while True:
            try:    
                admin_input = input (f"{Prettylines}\nWhat would you like to know?: ").lower()
                
                if admin_input == "exit":
                    print (admin_input.lower())
                    print("Exiting prompt now..")
                    break
                
                network_data = [network[admin_input] for network in data]
                for admin_input in network_data:
                    print(admin_input)
                    
                print ("\nType 'exit' if you'd like to leave this prompt..")
                
            except Exception as ValueError:
                print ("Please input a valid entry")
                
    #Print the http error code if other than response code 200                        
    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)