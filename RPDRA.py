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

#This code is to match the role(already with restrictions) and device groups.
with open('device_groups.pkl', 'rb') as file:
	device_groups = pickle.load(file)

with open('roles.pkl', 'rb') as file:
	roles = pickle.load(file)

#This is defined by the homeowner.
role_device_group_map = {('parents', ),('kids', ), ('neighbors', ) ,('babySitters', )}


#System code continues.
RPDRA_mapping = []
for mapping in role_device_group_map:
	role_name = mapping[0]
	role_object = get_role_object(role_name)
	device_group_name = mapping[1]
	device_group_object = get_group_object(device_group_name)
	RPDRA_mapping.append((role_object, device_group_object))

save_object(RPDRA_mapping, 'RPDRA_mapping.pkl')