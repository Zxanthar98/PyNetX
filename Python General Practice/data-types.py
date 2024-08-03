
##dictionary
router_info = {
    "hostname": "192.168.1.1", 
    "port": "22", 
    "username": "jon", 
    "password": "cisco123"
    }
#append dictionary
router_info ["platform"] = "cisco_IOS"

##list
routes = ['10.10.0.0/24', '10.10.1.0/24', '8.8.8.8/32']

##set
set_of_vlans = {"vlan 5", "vlan 10", "vlan 5"}
#append set
set_of_vlans.add("vlan 60")
set_of_vlans.remove("vlan 5")
