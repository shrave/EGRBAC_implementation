from device_groups import device_groups
from user import user
from role import role

def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def get_role_object(name):
	for r in roles:
		if r.name == name:
			return r

def get_group_object(name):
	for d in device_groups:
		if d.name == name:
			return d

def get_env_object(name):
	for d in environments:
		if d.name == name:
			return d

#This code is to match the role(already with restrictions) and device groups.
with open('device_groups.pkl', 'rb') as file:
	device_groups = pickle.load(file)

with open('roles.pkl', 'rb') as file:
	roles = pickle.load(file)

with open('envs.pkl', 'rb') as file:
	environments = pickle.load(file)

#This is defined by the homeowner. Keep environment group and device group.
role_device_group_map = {('parents', , ),('kids', , ), ('neighbors', , ) ,('babySitters', , )}


#System code continues.
device_groups_copy = device_groups
#Set Permission/privilege-role constraint. Keep a list of device groups and eliminate them as role, env are assigned.
RPDRA_mapping = []
for mapping in role_device_group_map:
	role_name = mapping[0]
	role_object = get_role_object(role_name)

	env_name = mapping[1]
	env_object = get_env_object(env_name)

	device_group_name = mapping[2]
	device_group_object = get_group_object(device_group_name)
	if device_group_object in device_groups_copy:
		#Add time here as well.
		RPDRA_mapping.append(((role_object, env_object), device_group_object))
		device_groups_copy.remove(device_group_object)
	else:
		print('Role device group constraint. Cannot allot '+device_group_object.name+' to role '+role_object.name)

save_object(RPDRA_mapping, 'RPDRA_mapping.pkl')