from netmiko import ConnectHandler
import getpass
import datetime
import yaml

starttime = datetime.datetime.now()

#Define custom functions to load YAML inventory file from local dir.  
def load_inventory_yaml(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)
    
def iterate_hosts_by_group(inventory, group_name):
    hosts = []
    for host, details in inventory['ALL_SWITCHES'][group_name].items():
        host_ip = details.get('HOST_IP')
        hosts.append(host_ip)
    return hosts

#Creating colors for terminal output using python lib colorama
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"  #Resets color to default

u = input("Please enter your username: ")
p = getpass.getpass("Please enter your password: ")

#Ask the user to input the group they want to run the script on
group_name = input("Please enter the group name (e.g., 'LAB', 'CORE, 'ACCESS'): ").upper()

#Load the inventory file hosts.yaml in the local dir. Str value in load_inventory_yaml is the filepath to the inv file.    
inventory = load_inventory_yaml('switch_hosts.yaml')
ip_list = iterate_hosts_by_group(inventory, group_name)



#Creates 'ip' variable by iterating over list 'ip_addresses'. 
for ip in ip_list:
    switches = {
        'device_type': 'cisco_ios',
        'host': ip,
    }
     
    try:
        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands.
        c = ConnectHandler(**switches,username = u, password = p)
        c.enable()
        gethostname = c.send_command('show run | sec hostname', use_textfsm=True)
        access_lists = c.send_command('show ip access-list', use_textfsm=True) 
        
        ###Debugging area start###
        #print (json.dumps(access_lists, indent=4))
        ###Debugging area end###
        
        #Strips the "hostname" out of the "show run | sec hostname" out put from gethostname
        hostname = gethostname.replace("hostname", "").strip()
        
        ACL_present = False
             
        for acl in access_lists:
            vty_acl = acl['acl_name'].upper()
            if vty_acl == ('VTY-ACCESS').upper():
                ACL_present = True
        
        if ACL_present == True:
            print("#"*30)
            print(f'{GREEN}Success! {hostname} ACL present in config.{RESET}')
            print("#"*30)

            
        elif ACL_present == False:
            print("!"*30)
            print(f'{RED}Failure! {hostname} missing ACL in config.{RESET}')
            print("!"*30)
        
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")   
#Grabs the time at the end of the script for record.
endtime = datetime.datetime.now()
duration = endtime - starttime
print(f'Total script runtime is {duration}.')