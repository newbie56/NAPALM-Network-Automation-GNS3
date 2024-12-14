from napalm import get_network_driver
import json

driver = get_network_driver('ios')
device = driver('192.168.10.6','admin','cisco')
device.open()
print(json.dumps(device.get_facts(), indent=2))
device.close()
