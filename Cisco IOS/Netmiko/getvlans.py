from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler
import getpass
import datetime
import yaml
import json

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
    
#Defining the main function of the script to connect to our switches and check their vlan integrity.  
def process_switch(switch_ip, username, password, vlanid_DB):
    
    try:
        # Define switch parameters
        switch_params = {
            'device_type': 'cisco_ios', 
            'ip': switch_ip,
            'username': username,
            'password': password
        }
        
        #Connect to switches, execute 'show vlan' on each and store data in 'output' var. 
        c = ConnectHandler(**switch_params)
        c.enable()
        output = c.send_command('show vlan', use_textfsm=True)
        hostname = c.send_command('show run | sec hostname', use_textfsm=True)
        
        #Debugging area!!
        #print (f'Vlans configured on {switch_ip}\n {json.dumps(output, indent=4)}\n')

        #Presetting the var 'Pass' to True before the script continues.
        Pass = True
                
        #Creates a list of vlan id's from the data in 'output'
        configured_vlans_id = {v['vlan_id'] for v in output}
        '''
        Example data:
                    {'40', '999', '15', '1', '27', '1004', '43', '12', '1005', '65', '1002', '1003', '41', '42'}
                    This is a list of all the vlan id's on one of  our switches in the lab. 
        '''
        
        #Creates a list of vlan names from the data in 'output'
        configure_vlans_name = {v['vlan_name'] for v in output}
        '''
        Example data:
                    {'default', 'fddi-default', 'LAB', 'fddinet-default', 'trnet-default', 'eLock-VLAN-27', 'WiFi', 'token-ring-default'}
                    This is a list of all the vlan names on one of  our switches in the lab.        
        '''

        #Iterates over our list of vlan id's and checks that list against the configured vlans on each switch in the above data. 
        for vlan_id in vlanid_DB:
            config_vlan_id = (f'vlan {vlan_id}')
            if vlan_id not in configured_vlans_id:
                Pass = False
                #c.send_config_set(config_vlan_id)
                #print(f'{hostname} is missing vlan {vlan_id} from its vlan DB!!\n')
        
        for vlan_name in output:
            print (f'{vlan_name['vlan_name']}\n')
                
        #If the variable 'Pass' hasn't been overwritten to False, this means that the switch has all of the vlans in our static DB configured locally.         
        if Pass:
            print(f'{hostname} passed the vlan DB check.')

    except Exception as e:
        print(f"Error processing switch {switch_ip}: {e}")
        
        '''
        Boilerplate code below this point. This code generalizable and the ip_addresses data is populated by loading a 'hosts.yaml' file. 
        '''
    
#Load the inventory file hosts.yaml in the local dir. Str value in load_inventory_yaml is the filepath to the inv file.    
inventory = load_inventory_yaml('hosts.yaml')

#Ask the user to input the group they want to run the script on
group_name = input("Please enter the group name (e.g., 'LAB', 'PROD'): ")

#Declaring our vars for the script
ip_addresses = iterate_hosts_by_group(inventory, group_name)
username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")
vlanid_DB = ['2','99']
vlanname_DB = ['DMZ', 'Servers']

vlanDB = {
    'vlanid'
    
    
    
}

#Run the script concurrently for each IP address in our inventory file. 
with ThreadPoolExecutor(max_workers=len(ip_addresses)) as executor:
    
    #Runs process switch and stores result in var futures to be iterated over later.  
    futures = {executor.submit(process_switch, ip, username, password, vlanid_DB): ip for ip in ip_addresses}

    #Processes the variable future as they are completed.
    for future in as_completed(futures):
        ip = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"Exception for switch {ip}: {e}")
            
#Prints the total script runtime in the terminal for record. 
endtime = datetime.datetime.now()
duration = endtime - starttime
print(f'Total script runtime was {duration}.')