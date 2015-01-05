class Robot(object):
	"""Holding all of the variables"""
	def __init__(self, actions):
		super(ClassName, self).__init__()
		self.index = 1
		self.actions = actions
		self.time = [0]
		self.points = [0]
		sef.owned = 1

r1 = Robot(['UpTote','UpTote','Uptote','LazyStack'])
r2 = Robot(['UpTote','Uptote','GreedyStack'])
r3 = Robot(['UpTote','UpTote','Uptote','SelfishStack'])
