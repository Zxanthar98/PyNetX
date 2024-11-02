import getpass
import napalm

driver =  napalm.get_network_driver('fortios')

u = input("Please input your username: ")
p = getpass.getpass("Please input your password: ")

device = driver(hostname=' IP ADDRESS HERE ', username = u, password = p)
device.open()

print(device.get_config(retrieve='running', full=False))

print(device.get_environment())
device.close()