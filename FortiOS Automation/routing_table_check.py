'''
This script imports a python dict file named "core_routes.py" which is used to validate the reachability of core subnets from spoke routers perspectives.
The script also checks the interface the traffic is taking to reach a destination subnet, against data in the dictionary to validate if routing is behaving optimally.

'''
from Boilerplate import getassets
import requests
from requests import session
import getpass
from Boilerplate.core_routes import c_routes

'''

There is no error handling for routes not found in the RIBs of our firewalls at this time. This could be implemented for further error handling capabilities, but it isn't urgent.

'''

#Creating colors for terminal output using python lib colorama
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"  #Resets color to default

#Prompting user for Hudu API key and base URL
API_KEY = getpass.getpass("Please enter your Hudu API key: ")
base_url = "https://lifeflight.huducloud.com"
#Mapping the asset type to the asset layout ID as defined in Hudu
asset_type_mapping = {
    'firewalls': 29,
    'switches': 30,

}

#Prompting user for asset type (firewalls or switches) and converting to lowercase
asset_type = input("Are we running this script against firewalls or switches?: ").lower()
asset_layout_id = asset_type_mapping.get(asset_type)
#Checking if the asset type is valid
if asset_layout_id is None:
    print("Invalid input. Please enter 'firewalls' or 'switches'.")
    exit(1)

#Calling the get_hudu_assets function to retrieve assets from Hudu
inventory = getassets.get_hudu_assets(API_KEY, base_url, asset_layout_id)

#Populating username and password at runtime
username = input("Please enter your username> ")
password = getpass.getpass("Please enter your password> ")

#Itereates over list of IP addresses and stores data in var firewall_ip to be used in future api calls
for asset in inventory:
    firewall_ip = asset['ip_address']
    api_login_url = f"https://{firewall_ip}:442/logincheck"

    #Create a session to maintain the login state
    session = requests.Session()
    headers = {
        'Accept': "application-json",
        'content-Type': "application-json"
    }

    #Payload for login
    payload = {
        "username": username,
        "secretkey": password
    }
    
    #Disable warnings over self signed certificates
    requests.packages.urllib3.disable_warnings()
    
    #Authenticate using local creds
    try:
        login_response = session.post(api_login_url, data=payload, headers=headers, verify=False)
        
        #If the returned status code is 200, then continue, if not then the script won't continue to run
        if login_response.status_code == 200:
        
            #Get firewall system status
            api_status_url = f"https://{firewall_ip}:442/api/v2/monitor/system/status"
            status_response = session.get(api_status_url, verify=False)
    
        #If return status code is 200 then continue running the script
        if status_response.status_code == 200:
            status_data = status_response.json()
            
            #Looks in the results root of the tree and searches for the key "hostname" to store in var "hostname"
            system_info = status_data.get('results', {})
            hostname = (system_info['hostname'])
            
            #Starts new get RESTful api call to gather routing information
            api_rib_url = f"https://{firewall_ip}:442/api/v2/monitor/router/ipv4"
            rib_response = session.get(api_rib_url, verify=False)
            
            #Formats the data in ospf_response into json and stores data in new var ospf_data
            rib_data = rib_response.json()
            routes = rib_data.get('results', [])
            
            #Iterates over the expected routes in the c_routes module imported | "core_route" is the value part of the dict whereas "route_name" is the value part of the dict.
            for route_name, core_route in c_routes.items():
                specific_route = None
                #Iterates over RIB searching in the value portion of the key "ip_mask" for matches on "core_route" and once a match is found break and continue to print statements.
                for route in routes:
                    if route.get('ip_mask') == core_route:
                        specific_route = route
                        break
                    
                if specific_route.get('interface') == route_name:
                    print(f'{GREEN}{hostname} route to', f'{specific_route.get('ip_mask')}', f'takes {specific_route.get('interface')} with a metric of {specific_route.get('metric')}{RESET}')    
                       
                
                elif not specific_route.get('interface') == route_name:
                    print (f'{RED}{hostname} is taking suboptimal path via {specific_route.get('interface')} to get to {specific_route.get('ip_mask')}{RESET}')
  
        else:
            print("Login failed. Check your credentials or firewall settings.")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")   