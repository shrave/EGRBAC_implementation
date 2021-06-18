import pickle

#Function for pickling variables.
def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

#Load the privileges i.e device(acronyms) and functionality tuples.
privileges = []
#Import the already loaded device instances in the smart home.

#Retrieving previous device instances based on current floorplan.
with open('devices_floorplan.pkl', 'rb') as file:
	device_instances = pickle.load(file)

for device in device_instances:
	for privi in device.privileges:
		privileges.append((device.label, privi))
print(privileges)

#Group privileges in various device groups.

#Privilege sets different are present as dictionary and value in a list named device_privileges.
#This space is defined by the homeowner.
device_privileges = {}



#Make device group objects.
device_group_list = []
for name in device_privileges:
	k = device_groups(name)
	k.add_privileges(device_privileges[name])
	device_group_list.append(k)

save_object(device_group_list,'device_groups.pkl')
