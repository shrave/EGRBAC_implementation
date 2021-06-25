#In this file, we define roles, users, allot roles to user, add restrictions to the roles.
import pickle
from user import user
from role import role
from environment import environment

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
#For now, we are making sure that the roles are mutually exclusive and they are not being assigned to same user.
user_roles = ['Owner', 'Normal', 'Relative', 'Child', 'Guest', 'Guest Child']
user_names = ['User 1','User 2','User 3','User 4', 'User 5', 'User 6']
environments_restriction_defs = {'Env1':['summer', 'morning'],'Env2':['summer', 'evening'], 'Any Time':[]}
user_role_map = [('User 1', 'Owner'), ('User 2', 'Normal'), ('User 3', 'Relative') ,('User 4', 'Child'), ('User 5', 'Guest'), ('User 6', 'Guest Child') ]


#Write to policy config:
f = open('policy.config', 'a')
f.write('User Roles:\n')
for k in user_roles:
	f.write(k+'\n')
f.write('--------------------------\n')
f.write('User Names:\n')
for k in user_names:
	f.write(k+'\n')
f.write('--------------------------\n')
f.write('Environment Roles:\n')
for k in environments_restriction_defs:
	f.write(k+'\n')
	for j in environments_restriction_defs[k]:
		f.write(j+'\n')
f.write('--------------------------\n')
f.write('User Role Map:\n')
for k in user_role_map:
	f.write('('+k[0]+','+k[1]+')'+'\n')
f.write('--------------------------\n')

#Loading these players in the space.
role_objects_list = []
for name in user_roles:
	role_objects_list.append(role(name))

user_objects_list = []
for name in user_names:
	user_objects_list.append(user(name))


#Creating environment objects.
environment_objects_list = []
for name in environments_restriction_defs:
	env = environment(name)
	# print(environments_restriction_defs[name])
	env.set_restrictions(environments_restriction_defs[name])
	environment_objects_list.append(env)

save_object(environment_objects_list, 'envs.pkl')

new_roles = role_objects_list

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
