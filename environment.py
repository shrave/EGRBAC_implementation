class environment(object):
	"""docstring for environment"""
	def __init__(self, name):
		super(environment, self).__init__()
		self.name = name
		self.restricted_envs = []

	def set_restrictions(self, list_of_environments =[], *args):
		self.restricted_envs.extend(list_of_environments)
		