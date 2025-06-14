from pyats.topology import loader
from genie.libs.parser.iosxe.show_version import ShowVersion
from genie.testbed import load

testbed = load('/etc/PyNetX/Cisco IOS/pyats/testbed.yaml') 
device = testbed.devices['LABCAT-01'] 
device.connect() 
output = device.execute('show version') 
parsed_output = ShowVersion(output) 
print(parsed_output.get('version')) 
device.disconnect()