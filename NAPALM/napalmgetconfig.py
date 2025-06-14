#had to use pip install napalm --break-system-packages to install napalm
import napalm
from pprint import pprint
import xmltodict

driver = napalm.get_network_driver('ios')

#Defines a dict of devices
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

#Iterates over each devices in the above devices dict
for device_name, device_info in devices.items():
    # Initialize the driver with device credentials
    device = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"]
    )
    
    try:
        #Open the connection to the device
        device.open()
        
        #Retrieve the running configuration and print output to terminal
        (device.get_config(retrieve ='running', full=False))
    
    except Exception as e:
        print(f"An error occurred with device {device_name}: {e}")
    
    finally:
        #Always close the connection to the device
        device.close()