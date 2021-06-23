from device import device
from devices import devices

class device_group(object):
	"""docstring for device_group"""
	def __init__(self, Name):
		super(device_group, self).__init__()
		self.group_name = Name
		self.device_privilege_list = []
	#Privileges are device, privilege tuples.
	def add_privileges(self, privileges):
		self.device_privilege_list.extend(privileges)
