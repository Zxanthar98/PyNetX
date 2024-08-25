from netmiko import ConnectHandler
import json

#Our list of IPs to connect to
ip_addresses = ['10.10.210.2', '10.10.210.3', '10.10.210.4']

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
        output = c.send_command('show spanning-tree vlan 1', use_textfsm=True)
        hostname = c.send_command('show run | sec hostname', use_textfsm=True)
        #print(json.dumps(output, indent=4))
        
        #Saves the running-config to the startup
        c.save_config()  
        
        #Custom list of commands to complete in the for loop to properly configure STP on switches
        payload_1 = ('spanning-tree vlan 1 priority 0', 'spanning-tree pathcost method long')
        payload_2 = ('spanning-tree vlan 1 priority 4096', 'spanning-tree pathcost method long')
        
        #Iterates over output and checks the STP port role (desg, root, blk) and sends config payload
        for bridge in output:
            print(f"{hostname}'s STP status is \n{json.dumps(bridge, indent=4)}")
            #print (f"{bridge['role']}")
            if bridge['role'] == ['Desg']:
                c.send_config_set(payload_1)  
                
    except Exception as e:
        print(e)