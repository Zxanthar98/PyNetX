import requests
from pprint import pprint
from requests import session
import getpass

#Admin prompt to input Meraki API Key
API_KEY = getpass.getpass("Please enter the Meraki Dashboard API key: ")

Prettylines = ("---------------------------------------")

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
        print(f"Here is the different data you can query:\n{Prettylines}")
        for keys in data:
            for key in keys.keys():
                print(f"{key.capitalize()}")
         
        #Allows the admin to input string to select which key to query
        while True:
            try:    
                admin_input = input (f"{Prettylines}\nWhat would you like to know?: ").lower()
                
                #Allows the admin to break the loop by typing exit    
                if admin_input.lower() == "exit":
                    print (admin_input.lower())
                    print("Exiting prompt now..")
                    break
                
                org_data = [org[admin_input] for org in data]
                for admin_input in org_data:
                    print(f"{admin_input}")
                    
                print ("\nType 'exit' if you'd like to leave this prompt..")
                    
            except Exception as ValueError:
                print ("Please input a valid entry")
                
    #Print the http error code if other than response code 200                        
    else:
        print ("Error:", response.status_code)
except Exception as e:
    print ("An error occurred:", e)