from netmiko import ConnectHandler
import json

#Our list of IPs to connect to
ip_addresses = ['10.10.210.2', '10.10.210.3', '10.10.210.4']

mac_address = ['e438.8340.84db']

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
        #mac_table = c.send_command('show mac address-table', use_textfsm=True)
        
        #Pulls interface data from output for later use in command payload.
        data = json.loads(output)
        interface_name = data["interface"]
        
        payload = (f'interface {t}','description test')
        print(json.dumps(f"Interface Name: {interface_name}", indent=4))
          
        
        #Comment here
        for t in output:
            if t['mode'] == 'trunk' or  ['admin_mode'] == 'trunk':
                print(f"Interface {t['interface']} on {hostname} is a trunk.\n")
            if not ['mode'] == 'trunk' or  ['admin_mode'] == 'trunk':
                c.send_config_set(payload)
            
        #Saves the running-config to the startup
        #c.save_config()  
                
    except Exception as e:
        print(e)