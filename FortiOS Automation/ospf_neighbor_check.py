import requests
from requests import session
import getpass
import yaml

'''

No known bugs at this time.

'''

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
group_name = input("Please enter the group name (e.g., 'LAB', 'PROD_SPOKE, 'PROD_CORE'): ")
inventory = load_inventory_yaml('firewall_hosts.yaml')
ip_list = iterate_hosts_by_group(inventory, group_name)

#List of router ID's that a router should be neighbors with
#expected_neighbors = ['10.10.150.1', '10.10.162.253', '10.10.165.253', '10.10.80.1', '10.10.1.1', '10.10.43.1']

#A dict of router IDs that we expect a spoke router to have
expected_neighbors = { 
                       "CORE1": "10.10.150.1",
                       "CORE2": "10.10.80.1",
                       "CORE3": "10.10.162.253"
}


#Populating username and password at runtime
username = input("Please enter your username> ")
password = getpass.getpass("Please enter your password> ")

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
            
            #Starts new get RESTful api call to gather OSPF neighbor information
            api_ospf_url = f"https://{firewall_ip}:442/api/v2/monitor/router/ospf/neighbors"
            ospf_response = session.get(api_ospf_url, verify=False,)      
            
            #Formats ospf_reponse into json format and then gets the data inside of the 'results' key  and stores data in 'neighbors' variable
            ospf_data = ospf_response.json()
            neighbors = ospf_data.get('results', [])

            #Initializes variable into an empty list
            router_IDs = []
            
            #iterates over output in neighbors and gets the value in key 'router_id' and appends empty list 'router_IDs' with output
            for neighbor in neighbors:
                router_IDs.append(neighbor['router_id'])
            
            #Populates variable 'missing_router_ids' with missing OSPF neighbors in 'router_IDs' that are checked against 'expected_neighbors' and iterated over with data stored in 'router_id'
            missing_router_ids = [name for name, router_id in expected_neighbors.items() if router_id not in router_IDs]
            
            #If 'missing_router_ids' is empty, hosts pass their neighbor check
            if not missing_router_ids:
                print("#"*75)
                print(f'{GREEN}{hostname} passed neighbor check.{RESET}')
                print("#"*75)
            
            #If 'missing_router_ids' is not empty (i.e router is missing neighbors) print which router is missing which neighbors    
            else:
                print("!"*75)
                print(f"{RED}{hostname} is missing the following neighbors: {missing_router_ids}{RESET}.")
                print("!"*75)
            
        else:
            print("Login failed. Check your credentials or firewall settings.")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")     