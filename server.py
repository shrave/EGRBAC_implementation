#!/user/bin/env python

from app import create_app
from tests import test_app
from flask import jsonify
from flask import request
import json
import pickle
import threading
from threading import Timer

from flask import Flask
from flaskext.mysql import MySQL
from datetime import date, datetime
import calendar

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Krsna_12'
app.config['MYSQL_DATABASE_DB'] = 'EGBRAC'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

app = create_app()

################################################################
# File Imports

with open('roles.pkl', 'rb') as input:
	roles_list = pickle.load(input)

with open('users.pkl', 'rb') as file:
	user_list = pickle.load(file)

with open('device_groups.pkl', 'rb') as file:
	device_groups = pickle.load(file)

with open('envs.pkl', 'rb') as file:
	environments = pickle.load(file)

with open('RPDRA_mapping.pkl', 'rb') as file:
	RPDRA_mapping = pickle.load(file)
################################################################
# Functions other than mysql

Y = date.today().year # Current year.
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
		   ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
		   ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
		   ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
		   ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now):
	if isinstance(now, datetime):
		now = now.date()
	now = now.replace(year=Y)
	return next(season for season, (start, end) in seasons
				if start <= now <= end)

def weekend_check(now):
	weekno = now.weekday()
	if weekno < 5:
		return "Weekday"
	else:  # 5 Sat, 6 Sun
		return "Weekend"

def get_part_of_day(hour):
	return (
		"morning" if 5 <= hour <= 11
		else
		"afternoon" if 12 <= hour <= 17
		else
		"evening" if 18 <= hour <= 22
		else
		"night"
	)

#Get current environment variables.
def current_time_variables():
	environment = {}
	now = date.today()
	# print(get_season(date.today()))
	environment['season'] = get_season(now)
	environment['Weekend'] = weekend_check(now)
	environment['period'] = get_part_of_day(datetime.now().hour)
	environment['year'] = now.year
	environment['month'] = now.month
	environment['date'] = now.day
	environment['day'] = calendar.day_name[now.weekday()]
	environment['month_name'] = calendar.month_name[now.month]
	return list(environment.values())




################################################################
#Mysql-resource based functions.
def begin_job_commit(user_privileges, user_object):
	#Loop through all resources in each device and commit them.
	user_name = user_object.name
	for device_label in user_privileges:
		for privilege in user_privileges[device_label]:
			cursor.execute("INSERT INTO Resource_ownership (Owner, Device, Privilege, Timestamp,  Status) VALUES (%s, %s, %s, CURRENT_TIME() , 'Start');",(user_name, device_label,privilege))
			conn.commit()


def commit_job_ends(user_privileges):
	for device_label in user_privileges:
		for privilege in user_privileges[device_label]:
			print(privilege, device_label)
			cursor.execute("INSERT INTO Resource_ownership (Owner, Device, Privilege, Timestamp,  Status) VALUES ('System', %s, %s, CURRENT_TIME() , 'End');",(device_label,privilege))
			conn.commit()
			# resource_master_list[(device_label, privilege)] = 'available'
			# resource_master_list[(device_label, privilege)] += 1

			#commit privilege, device mysql unoccupied command.
def get_current_user_privileges(user_object):
	#Get current environment conditions.
	current_environments = current_time_variables()
	a = [str(x).lower() for x in current_environments]

	#Get all roles of a user.
	user_roles = user_object.roles
	# print(user_roles)
	no_role_flag = True
	all_privileges = {}
	for tup in RPDRA_mapping:
		current_role_object = tup[0][0]
		current_environment_object = tup[0][1]
		current_device_group = tup[1]
		for role in user_roles:
			# print(role.name)
			# print('--------')
			# print(current_role_object.name)
			if role.name == current_role_object.name:
				#Check for environment compatability.
				b = [str(x).lower() for x in current_environment_object.restricted_envs]
				# print(a)
				# print('8888888')
				# print(b)
				if set(a).isdisjoint(b):
					no_role_flag = True
					all_privileges[current_role_object.name] = current_device_group.device_privilege_list
					#The above code collects all privileges of a role in RDPRA mapping.
	# print(all_privileges)
	#Converting formats to out Task based system.
	user_privileges = {}
	for tup in all_privileges:
		# print(tup)
		# print(all_privileges[tup])
		for j in all_privileges[tup]:
			# print(j)
			if j[0] not in user_privileges.keys():
				user_privileges[j[0]] = [j[1]]
			else:
				user_privileges[j[0]].append(j[1])
	# print(user_privileges)
	return user_privileges

def update_user_every_hour(user_object):
	user_privileges = get_current_user_privileges(user_object)
	commit_job_ends(user_privileges)
	threading.Timer(60*60, update_user_every_hour,[user_object]).start()
	begin_job_commit(user_privileges, user_object)


def initialize_resource_status():
	#Clear all tables.
	cursor.execute('Truncate Resource_ownership;')
	cursor.execute('Truncate API_Request;')
	conn.commit()
	#make all resources to availble and commit.
	# resource_master_list = {}
	for group in device_groups:
		for privilege in group.device_privilege_list:
			# resource_master_list[(device.label, privilege)] = 'available'
			# resource_master_list[privilege] = 1
			#Since in EGRAC only one user can control the session.
			# print('yesssssss')
			cursor.execute("INSERT INTO Resource_ownership (Owner, Device, Privilege, Timestamp,  Status) VALUES ('System', %s, %s, CURRENT_TIME() , 'Available');",privilege)
			conn.commit()
	# return resource_master_list
################################################################
#Server initialization and endpoint code.
def get_user_object(name):
	for r in user_list:
		# print(r.name)
		if r.name == name:
			return r
def get_role_object(name):
	for r in roles_list:
		if r.name == name:
			return r

def get_group_object(name):
	for d in device_groups:
		if d.group_name == name:
			return d

def get_env_object(name):
	for d in environments:
		if d.name == name:
			return d
################################################################
initialize_resource_status()
# print(resource_master_list)

@app.route("/test", methods=["POST"])
def test():
	user_privileges = {}
	print(request.get_json(force = True))
	d = request.get_json(force = True)
	ip_addr = request.remote_addr

	user_request_dict = json.loads(d)
	user_name = user_request_dict['User']
	#Sessions not needed to be named.
	# task_name = user_request_dict['Session']
	#Record the request and its response in the table.
	#Get user object.
	user_object = []
	for user in user_list:
		if user.name == user_name:
			user_object = user
	if not user_object:
		print("User not registered in the house.")
		# INSERT INTO API_Request(User, Task, Timestamp, Validity, Status, ip_address, Message, Resources_allowed) VALUES('krsna', 'Cook Food', CURRENT_TIME() ,
		#0, 'Failed',  INET_ATON('127.0.0.1'),'User not registered in the house.','None');
		cursor.execute("INSERT INTO API_Request (User, Timestamp, Status, ip_address, Message, Resources_allowed) VALUES (%s, CURRENT_TIME(), 'Failed',  INET_ATON(%s),'User not registered in the house.','None');",(user_name, ip_addr))
		conn.commit()
		return {"System response":"User not registered in the house."}

	#Getting current user privilges.
	user_privileges = get_current_user_privileges(user_object)
	# print(user_privileges)
	if not user_privileges:
		cursor.execute("INSERT INTO API_Request (User, Timestamp, Status, ip_address, Message, Resources_allowed) VALUES (%s, CURRENT_TIME(), 'Failed',  INET_ATON(%s),'User is has no privileges in the current environment.','None');",(user_name, ip_addr))
		conn.commit()
		# print('abcd')
		return {"System response":"User has no privileges in the current environment."}
	else:
		cursor.execute("INSERT INTO API_Request (User, Timestamp, Status, ip_address, Message, Resources_allowed) VALUES (%s, CURRENT_TIME(), 'Success',  INET_ATON(%s),'User has these privileges in the current environment.',%s);",(user_name,ip_addr, json.dumps(user_privileges)))
		conn.commit()
	#Get roles, select thatrole for the session(those which are active in this env) and
	#get groups active for the session.
	

	#TO DO:Write code to commit into db perpetually, returning current privileges.
	#Every few hours, calculate the difference in privileges and commit them end. do A-B make them start,
	#Do B-A, make them free.
	#Make a global function to get all privileges at a point.
	#Make a timed function that calls this function, puts them in a db and end commits the prev privileges.

	# #Loop through all resources in each device and commit them.
	# for device_label in user_privileges:
	# 	for privilege in user_privileges[device_label]:
	# 		cursor.execute("INSERT INTO Resource_ownership (Owner, Device, Privilege, Timestamp,  Status) VALUES (%s, %s, %s, CURRENT_TIME() , 'Start');",(user_name, device_label,privilege))
	# 		conn.commit()

	return {"System response":("User has the following privileges currently."), "privileges":user_privileges}

if __name__ == '__main__':
	for user in user_list:
		# user_object = get_user_object(user.name)
		# print(user_object)
		update_user_every_hour(user)
	app.run()