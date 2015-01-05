class Robot(object):
	"""Holding all of the variables"""
	def __init__(self, actions):
		super(ClassName, self).__init__()
		self.ind = 1
		self.actions = actions
		self.time = [0]
		self.points = [0]
		sef.owned = 1
		self.load = 0

def cumsum(lis):
    total = 0
    for x in lis:
        total += x
        yield total

def ValidStacks(bot,stacks,maxstack):
	for i in stacks:
		if maxstack-(i+bot.load)>0:
			yield i.index

def firstMin(lis):
	ind = []
	for i in lis:
		if i == min(lis):
			ind.append(i.index)
	return ind[0]


def GreedyStack(bot, stacks, maxstack):
	openstacks = ValidStacks(bot, stacks, maxstack)
	owned = openstacks[0]
	return owned

def LazyStack(stacks):
	return firstmin(stacks)

def SelfishStack(bot,stacks,maxstack):
	if maxstack-(stacks[owned]+bot.load)>0: 
		return owned
	else:
		return LazyStack(stacks)

def Iterate(bot,stacks,bins, maxstack):
	action = bot.actions[bot.ind]

	#figure out active stack
	if action == "LazyStack":
		pass
	if action == "GreedyStack":
		pass
	if action == "SelfishStack":
		pass
	#Assign time and point values for each action
	if action == 'move':
		dt = 1
		dp = 0
	elif action == 'LoadTote':
		bot.load +=1
	elif action == 'StackBin':
		dt= 4
		dp = 4*stack[activestack]
		stack[activestack]+=1
	elif action == 'RecieveTote':
		dt = 2
		dp = 0
		bot.load += 1
	elif action == 'RecieveLitter':
		dt =2
		dp = 0
	elif action == 'UseLitter':
		dt= 5
		dp = 6
	elif action == 'GreedyStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = GreedyStack()
		stacks[bot.owned]+=bot.load
		#update stacks
	elif action == 'LazyStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = LaztStack()
		stacks[bot.owned]+=bot.load
		#update stacks
	elif action == 'SelfishStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = SelfishStack()
		stacks[bot.owned]+=bot.load
		#update stacks
	elif action == 'CopStack':
		dt = 3
		#give points if there are 2 coop bins
		#remove Coop stack from actions
	else:
		raise TypeError

	bot.ind +=1
	return(bot, stacks,bins)


def pick(alliance):
	#might need to fix so that it picks the first one with the lowest time
	activebot = firstMin([sum(alliance[0].time),sum(alliance[0].time),sum(alliance[0].time)])
	return(activebot)

def RunMatch(alliance):
	elaspedtime = 0
	maxtime = 135
	bins = 4
	maxstack = 4
	#todo: add in coop thingy
	stacks = [0,0,0,0,0,0,0,0,0,0]
	while elaspedtime < maxtime:
		elaspedtime = max(sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time))
		activebot = pick(alliance)
		updatedbot,stacks,bins = Iterate(alliance[activebot],stacks,bins,maxstack)
		alliance[activebot]= updatedbot	
# def placebin



r1 = Robot(['LoadTote','move','LazyStack'])
r2 = Robot(['LoadTote','LoadTote','GreedyStack'])
r3 = Robot(['LoadTote','LoadTote','LoadTote','move','SelfishStack'])
alliance = [r1,r2,r3]