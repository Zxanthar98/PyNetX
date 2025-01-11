from genie.testbed import load
testbed = load('/etc/PyNetX/Cisco IOS/pyats/testbed.yaml')


device = testbed.devices['LABCAT02']
device.connect()