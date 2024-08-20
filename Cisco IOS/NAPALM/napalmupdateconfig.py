#had to use pip install napalm --break-system-packages to install napalm
import napalm
from pprint import pprint

driver = napalm.get_network_driver('ios')

# Defines a dict of devices
devices = {
    "LABCAT01": {
        "hostname": "10.10.210.2",
        "username": "admin",
        "password": "cisco123"
    },
    "LABCAT02": {
        "hostname": "10.10.210.3",
        "username": "admin",
        "password": "cisco123"
    },
        "LABCAT03": {
        "hostname": "10.10.210.4",
        "username": "admin",
        "password": "cisco123"
    }, 
}

for device_name, device_info in devices.items():
    # Initialize the driver with device credentials
    device = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"]
    )

try: 
    device.open()
    
    #Load the config changes from a file
    with open('/home/jonathan/Documents/Net-Dev-Ops/Cisco IOS/NAPALM/napalmdemo.txt', 'r') as config_file:
        config = config_file.read()
        
        #Load the config file onto the devices
        device.load_template(source='string', config=config)
        
        #Commit the changes
        device.commit_config()

except Exception as e:
    print(f"An error occured: {e}")

finally:
    device.close()