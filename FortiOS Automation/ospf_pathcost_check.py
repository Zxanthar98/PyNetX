'''
The intention behind this script is to pull the configured cost from each router 
'''

import requests
from requests import session
import getpass
import yaml
import json

#Define custom functions to load YAML inventory file from local dir. 
def load_inventory_yaml(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)
    
def iterate_hosts_by_group(inventory, group_name):
    hosts = []
    for host, details in inventory['ALL_FIREWALLS'][group_name].items():
        host_ip = details.get('HOST_IP')
        hosts.append(host_ip)
    return hosts

#Creating colors for terminal output using python lib colorama
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"  #Resets color to default

#Use the above functions to load the group_name, inventory, and ip_list vars with data from the firewall_hosts.yaml inventory file
group_name = input("Please enter the group name (e.g., 'LAB', 'CORE, 'SPOKE'): ")
inventory = load_inventory_yaml('firewall_hosts.yaml')
ip_list = iterate_hosts_by_group(inventory, group_name)

#Populating username and password at runtime
username = input("Please enter your username> ")
password = getpass.getpass("Please enter your password> ")

target_route = " "

#Itereates over list of IP addresses and stores data in var firewall_ip to be used in future api calls
for ip in ip_list:
    firewall_ip = ip
    api_login_url = f"https://{firewall_ip}:442/logincheck"

    # Create a session to maintain the login state
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
            
            #Outputs entire system info dump into terminal, only useful for debuggin/ testing
            #print(json.dumps(status_data, indent=4))
            
            #Looks in the results root of the tree and searches for the key "hostname" to store in var "hostname"
            system_info = status_data.get('results', {})
            hostname = (system_info['hostname'])
            
            #Starts new get RESTful api call to gather routing information
            api_rib_url = f"https://{firewall_ip}:442/api/v2/monitor/router/ipv4"
            rib_response = session.get(api_rib_url, verify=False)
            
            #Formats the data in ospf_response into json and stores data in new var ospf_data
            rib_data = rib_response.json()
            routes = rib_data.get('results', [])

            
            #Pre-sets specific route to = None, making the logic for a route that doesn't exist work in the script by not finding any matching route and spitting out an error
            specific_route = None
            
            #Iterates over routes to get the keys from each dict in the list of "results"
            for route in routes:
                #Checks that the route queried for is actually in the RIB and breaks
                if route.get('ip_mask') == target_route:
                    specific_route = route
                    break 
            
            print (json.dumps(specific_route, indent=4))
            
            
    
    
        else:
            print("Login failed. Check your credentials or firewall settings.")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")   