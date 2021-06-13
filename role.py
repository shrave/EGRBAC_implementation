from device import device
from devices import devices
#Class of a real user/person in the house. For EGBRAC, users have to be converted to roles.
class user(object):
	def __init__(self, Name):
		#List of user-groups.
		self.user_privilege_set = []
		self.username = ''
		self.password = ''
		self.Name = Name
		self.device_groups = []
	#All device group operated by a role.
	def assign_device_groups(self, device_groups):
		for group in device_groups:
			self.device_groups.append(group)

	def register(self, username, password):
		self.username = username
		self.password = password