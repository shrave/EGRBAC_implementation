#This script is to make different groups.
from device import device
from devices import devices
import pickle

def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
#Device groups: Each user role has a device group.
#Security levels -> device groups have different security levels.
#Risk -> device groups have different risks.

#Retrieving previous device instances based on current floorplan.
with open('devices_floorplan.pkl', 'rb') as file:
	device_instances = pickle.load(file)

#Loading the safety dictionary
with open('safety.pkl', 'rb') as file:
	security_levels = pickle.load(file)

user_groups = {1:'Owner',2:'Normal',3:'Limited',4:'Child',5:'Guest',6:'Child Guest'}
device_groups = {}
for k in user_groups:
	device_groups[user_groups[k]] = []
for device in device_instances:
	for n in user_groups:
		for privi in device.get_privileges_by_user_group(n):
			# print(device.get_privileges_by_user_group(7))
			device_groups[user_groups[n]].append((device.label, privi))

save_object(device_groups,'normal_device_groups_config.pkl')

device_groups = {}
security_groups = ['1S', '2S', '3S', '4', '1P', '2P', '3P']
for k in security_groups:
	device_groups[k] = []
for device in device_instances:
	for privi in security_levels[device.name]:
		if len(str(security_levels[device.name][privi])) > 2:
			device_groups[security_levels[device.name][privi][0:2]].append((device.label, privi))
			device_groups[security_levels[device.name][privi][2:4]].append((device.label, privi))
		else:
			device_groups[str(security_levels[device.name][privi])].append((device.label, privi))

save_object(device_groups,'security_device_groups_config.pkl')

risks = ['Moderate risk','Low risk','High risk']
device_groups = {}
for k in risks:
	device_groups[k] = []
for device in device_instances:
	for privi in device.privileges:
		device_groups[device.risk].append((device.label, privi))

save_object(device_groups,'risk_device_groups_config.pkl')
