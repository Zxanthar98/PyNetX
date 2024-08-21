from ncclient import manager
# import logging
# logging.basicConfig(level=logging.DEBUG)

switch = {"host": "10.10.210.2", "port": "22",
          "username": "admin", "password": "cisco123"}

with manager.connect_ssh(host=switch["host"], port=switch["port"], username=switch["username"], password=switch["password"], hostkey_verify=False) as m:
    for capability in m.server_capabilities:
        print('*' * 50)
        print(capability)