#In this file, we define roles, users, allot roles to user, add restrictions to the roles.
import pickle
from user import user
from role import role

def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
		
def get_name_object(name):
	for u in user_objects_list:
		if u.name == name:
			return u

def get_role_object(name):
	for r in role_objects_list:
		if r.name == name:
			return r
#Role and user names are given here by the homeowner.
user_roles = ['kids', 'parents', 'babySitters', 'guests', 'neighbors']
user_names = ['User 1','User 2','User 3','User 4']
restrictions_by_roles = {'User 1':['summer', 'morning'],'User 4':['summer', 'evening']}
user_role_map = [('User 1', 'kids'), ('User 2', 'parents'), ('User 3', 'babySitters'), ('User 4', 'guests'), ('User 2', 'neighbors')]

#Loading these players in the space.
role_objects_list = []
for name in user_roles:
	role_objects_list.append(role(name))

user_objects_list = []
for name in user_names:
	user_objects_list.append(user(name))


#Apply restrictions on roles.
new_roles = []

for u in role_objects_list:
	if u.name in restrictions_by_roles.keys():
		u.apply_restrictions(restrictions_by_roles[u.name])
		new_roles.append(u)
	else:
		temp_list = []
		u.apply_restrictions(temp_list)
		new_roles.append(u)

#Alloting roles to users.
for tup in user_role_map:
	user_name = tup[0]
	name_object = get_name_object(user_name)
	user_role = tup[1]
	role_object = get_role_object(user_role)
	name_object.assign_roles(role_object)
	# print(name_object.name)
	# print(name_object.roles)
save_object(role_objects_list, 'roles.pkl')
save_object(user_objects_list, 'users.pkl')
