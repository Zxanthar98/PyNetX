'''
This script has a 9 min runtime for four switches
'''

'''
ToDo:

1. Match on more complex parameters such as the vlan configured on the interface for more precise script decision making.
2. Run script using actual 802.1x command payload to simulate real life use case.
3. Run against production to find all NXU devices to validate accuracy. 

'''

from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler
import getpass
import datetime
import yaml

#Grabs the start time of the script to be subtracted from the endtime variable at the end of the script.
starttime = datetime.datetime.now()

#Load YAML inventory file from local dir. 
def load_inventory_yaml(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)
    
def iterate_hosts_by_group(inventory, group_name):
    hosts = []
    for host, details in inventory['ALL_SWITCHES'][group_name].items():
        host_ip = details.get('HOST_IP')
        hosts.append(host_ip)
    return hosts

#Defines a custom function to be called upon later. 
def process_switch(switch_ip, username, password, mac_list):
    try:
        # Define switch parameters
        switch_params = {
            'device_type': 'cisco_ios', 
            'ip': switch_ip,
            'username': username,
            'password': password
        }
        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands.
        c = ConnectHandler(**switch_params)
        c.enable()
        output = c.send_command('show interface switchport', use_textfsm=True)
        mac_table = c.send_command('show mac address-table', use_textfsm=True) 
        
        #Debugging area
        #print (json.dumps(mac_table, indent=4))
        #print(f"Test {mac_list[0]}")
        
        #Iterates over the list of dictionaries in 'output' and gets the 'interface' name out of each dict in the list.     
        for t in output:     
            interface_name = t['interface']
        
            #Defining payloads to send in the send_config_set command
            trunkport_payload = (f'interface {interface_name}', 'description DONT TOUCH ME!')
            accessport_payload = (f'interface {interface_name}', 'description Standard')
            
            #If the admin status is a trunk or the mode is trunk send trunk_payload, else continue on in the script.
            if t['mode'] == 'trunk' or t['admin_mode'] == 'trunk':
                c.send_config_set(trunkport_payload)
            
            else:
                for m in mac_table:
                    dest_port = m['destination_port'][0]
                    specialport_payload = (f'interface {dest_port}', 'description SPECIAL')
                #If the mac address found on the port in the show mac address table command matches the mac_list take 'x' action.
                    if m['destination_address'] in mac_list:
                        c.send_config_set(specialport_payload)
                        break
                    
                    else:
                        c.send_config_set(accessport_payload)
            
        #Saves the running-config to the startup
        c.save_config()  

        print(f"Completed processing for switch {switch_ip}")

    except Exception as e:
        print(f"Error processing switch {switch_ip}: {e}")

#Load the inventory file hosts.yaml in the local dir. Str value in load_inventory_yaml is the filepath to the inv file.    
inventory = load_inventory_yaml('switch_hosts.yaml')

#Ask the user to input the group they want to run the script on
group_name = input("Please enter the group name (e.g., 'LAB', 'CORE, 'ACCESS'): ")

#Declaring our vars for the script
ip_addresses = iterate_hosts_by_group(inventory, group_name)
username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")
mac_list = ['','']

# Run the script concurrently for each switch IP
with ThreadPoolExecutor(max_workers=len(ip_addresses)) as executor:
    #Runs process switch and stores result in var futures to be iterated over later.  
    futures = {executor.submit(process_switch, ip, username, password, mac_list): ip for ip in ip_addresses}

    #Processes the variable future as they are completed.
    for future in as_completed(futures):
        ip = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"Exception for switch {ip}: {e}")
            
#Grabs the time at the end of the script for record.
endtime = datetime.datetime.now()
duration = endtime - starttime
print(f'Total script runtime is {duration}.')