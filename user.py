from role import role

class user(object):
	"""docstring for user"""
	def __init__(self, Name):
		super(user, self).__init__()
		self.name = Name
		self.roles = []
		
	def assign_roles(self, role):
		self.roles.append(role)



