from netmiko import ConnectHandler
import json

#Our list of IPs to connect to
ip_addresses = [' ', ' ', ' ']

file_path = '/your/file/path'

#Opens or creates new file called output.json and correlates output.json with the var 'file'.
with open(file_path, 'w') as file:
    
    #Creates 'ip' variable by iterating over list 'ip_addresses'. 
    for ip in ip_addresses:
        switches = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': ' ',
            'password': ' '
        }

        #Iterates over switches and uses Netmiko connecthandler to connect over ssh and send commands. 
        try:
            c = ConnectHandler(**switches)
            c.enable()
            output = c.send_command('show interface vlan 1', use_textfsm=True)
            hostname = c.send_command('show run | sec hostname', use_textfsm=True)
            
            #Optional print statement to display output to the terminal for debugging
            #print(json.dumps(output, indent=4))
            
            #Custom list of commands to complete in order from position 0 to position 1.
            command_set = ('interface vlan 1', 'no shutdown')
            
            #Iterates over 'output and checks the value of link status and protocol status on each vlan1 interface
            for SVI in output:
                if SVI['link_status'] == 'administratively down' or ['protocol_status']  == 'down':
                    print(f"{SVI['interface']} is down on {hostname}")
                    c.send_config_set(command_set)
                else: 
                    print(f"{SVI['interface']} is up on {hostname}")
            
            #Formats variable output and file in json format with an indentation of 4
            json.dump(output, file, indent=4)
            
            #Writes variable file into output.json
            file.write('\n\n')
            
        except Exception as e:
            print(e)