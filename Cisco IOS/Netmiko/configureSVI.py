from netmiko import ConnectHandler
import json

#Our list of IPs to connect to
ip_addresses = ['10.10.210.2', '10.10.210.3', '10.10.210.4']

#Opens or creates new file called output.json and correlates output.json with the var 'file'.
with open('output.json', 'w') as file:
    
    #Creates 'ip' variable by iterating over list 'ip_addresses'. 
    for ip in ip_addresses:
        switches = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': 'admin',
            'password': 'cisco123',
        }

        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands. 
        try:
            c = ConnectHandler(**switches)
            c.enable()
            output = c.send_command('show interface vlan 1', use_textfsm=True)
            hostname = c.send_command('show run | sec hostname', use_textfsm=True)
            #print(json.dumps(output, indent=4))
            
            for SVI in output:
                #print(SVI['interface'])
                if SVI['link_status'] or ['protocol_status'] == 'administratively down' or 'down':
                    print(f"{SVI['interface']} is down on {hostname}")
                if not 'administratively down' or 'down' in SVI:
                    print(f"{SVI['interface']} is up on {hostname}")
            
            #Formats variable output and file in json format with an indentation of 4
            json.dump(output, file, indent=4)
            
            #Writes variable file into output.json
            file.write('\n\n')
        except Exception as e:
            print(e)