#Class of a real user/person in the house. For EGBRAC, users have to be converted to roles.
class role(object):
	def __init__(self, Name):
		#List of user-groups.
		self.user_privilege_set = []
		self.username = ''
		self.password = ''
		self.name = Name

	def register(self, username, password):
		self.username = username
		self.password = password

