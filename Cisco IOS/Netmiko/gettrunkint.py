'''
This script has a 20 min runtime for four switches.
'''

from netmiko import ConnectHandler
import getpass
import datetime

startime = datetime.datetime.now()
print(f'Script startime is {startime}.')

#Declaring a number of variables
ip_addresses = ['','']
mac_list = ['','']

u = input("Please enter your username: ")
p = getpass.getpass("Please enter your password: ")

#Creates 'ip' variable by iterating over list 'ip_addresses'. 
for ip in ip_addresses:
    switches = {
        'device_type': 'cisco_ios',
        'host': ip,
    }
    
    try:
        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands.
        c = ConnectHandler(**switches,username = u, password = p)
        c.enable()
        output = c.send_command('show interface switchport', use_textfsm=True)
        hostname = c.send_command('show run | sec hostname', use_textfsm=True)
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
                
    except Exception as e:
        print(e)
endtime = datetime.datetime.now()
print(f'Script endtime is {endtime}.')