from role import role

class user(object):
	"""docstring for user"""
	self.roles = []
	def __init__(self, Name):
		super(user, self).__init__()
		self.name = Name

	def assign_roles(self, roles):
		if type(roles) == list:
			self.roles = roles

	def apply_restrictions(self, restrictions):
		#restrictions = {'locations':[], 'environments':[], 'devices':[]}
		#Here, restrictions have no relationship with privilege tuples.
		#Only environment needs to be checked with user at runtime.
		self.restricted_environment = restrictions['environments']
		self.updated_privileges = restricted_privileges
		return restricted_privileges
