import pickle
from user import user

#Dividing list into chunks of size n.
def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


#Taking input of user details from an input file with .sce extension.

with open('example1.sce', 'r') as f:
	file_lines = f.readlines()

number_users = int(file_lines[1])
# Number of users in the input file.
file_lines = file_lines[2:]
user_list = [] #List of user instances.
user_names = file_lines[:number_users]
for name in user_names:
	user_list.append(user(name.strip('\n')))
# User names in the input file.
file_lines = file_lines[number_users:]
usermapping = {} # A dictionary of users as key and list of device instances as values.
device_groups = list(divide_chunks(file_lines, number_users+1))
# print(len(device_groups))
# Device groups are chunks of the device groups for each device.
user_group_dictionary = {}
for name in user_names:
	user_group_dictionary[name.strip('\n')] = []
devices = [] #Devices in the config.
for k in device_groups:
	#Mapping devices in the data file to device config in previous step.
	device_name = str(k[0][:-1])
	# print(device_name)
	devices.append(device_directory[device_name])
	i = 0
	for l,u in zip(k[1:], user_names):
		m = int(float(l))
		# print(m)
		user_group_dictionary[u.strip('\n')].append(m)