from ncclient import manager

# Device credentials and connection parameters
device = {
    "host": "10.10.210.4",  
    "port": 22,             
    "username": "admin",     
    "password": "cisco123",  
    "hostkey_verify": False 
}

# Connect to the device
with manager.connect(**device) as m:
    # Send a simple get-config RPC request
    config = m.get_config(source="running")
    print(config)