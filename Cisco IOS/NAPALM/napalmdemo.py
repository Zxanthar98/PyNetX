#had to use pip install napalm --break-system-packages to install napalm
import napalm
from pprint import pprint

driver = napalm.get_network_driver('ios')

device = driver(hostname='10.10.210.2', username='admin', password='cisco123')
device.open()
pprint(device.get_config(retrieve='running', full=False))

pprint(device.get_environment())
device.close()

