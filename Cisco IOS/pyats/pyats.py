from pyats.topology import loader
from genie.libs.parser.iosxe.show_version import ShowVersion

testbed = loader.load('testbed.yaml') 
device = testbed.devices['LABCAT-01'] 
device.connect() 
output = device.execute('show version') 
parsed_output = ShowVersion(output) 
print(parsed_output.get('version')) 
device.disconnect()