from netmiko import ConnectHandler
import json

#Our list of IPs to connect to
ip_addresses = ['10.10.210.2', '10.10.210.3', '10.10.210.4']

mac_list = ('00e0.4c69.1015')

#Creates 'ip' variable by iterating over list 'ip_addresses'. 
for ip in ip_addresses:
    switches = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'admin',
        'password': 'cisco123'
    }
    
    try:
        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands.
        c = ConnectHandler(**switches)
        c.enable()
        output = c.send_command('show interface switchport', use_textfsm=True)
        hostname = c.send_command('show run | sec hostname', use_textfsm=True)
        mac_table = c.send_command('show mac address-table', use_textfsm=True) 
        
        for m in mac_table:
            #mac_address = m['destination_address']
            if m['destination_address'] == mac_list:
                print(f"Steamdeck found on {hostname} on {m['destination_port']}\n")
        
        for t in output:     
            interface_name = t['interface'] #gets the 'interface' name out of output by iterating over each dictionary
            payload = [f'interface {interface_name}', 'description Standard'] 
            if t['mode'] == 'trunk' or  ['admin_mode'] == 'trunk':
                print(f"Interface {t['interface']} on {hostname} is a trunk.\n") 
            else:
                c.send_config_set(payload)
            
        #Saves the running-config to the startup
        #c.save_config()  
                
    except Exception as e:
        print(e)