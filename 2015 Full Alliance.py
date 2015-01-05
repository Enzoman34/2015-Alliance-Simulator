class Robot(object):
	"""Holding all of the variables"""
	def __init__(self, actions,name):
		super(Robot, self).__init__()
		self.ind = 0
		self.actions = actions
		self.time = [0]
		self.points = [0]
		self.owned = 1
		self.load = 0
		self.name = name


def cumsum(lis):
	"""Converts the list into a cumulative sum"""
	total = 0
	for x in lis:
		total += x
		yield total

def firstMin(lis):
	return lis.index(min(lis))


def GreedyStack(bot, stacks, maxstack):
	for i in stacks:
		if i == maxstack:
			i=0
	owned = stacks.index(max(stacks))
	return owned

def LazyStack(stacks):
	return firstMin(stacks)

def SelfishStack(bot,stacks,maxstack):
	if maxstack-(stacks[bot.owned]+bot.load)>0: 
		return bot.owned
	else:
		return LazyStack(stacks)

def Iterate(bot,stacks,bins, maxstack):
	action = bot.actions[bot.ind]

	#Assign time and point values for each action

	dp=0
	dt=0
	if action == 'move':
		dt = 1
	elif action == 'LoadTote':
		dt = 2
		bot.load +=1
	elif action == 'StackBin':
		dt= 4
		dp = 4*stack[activestack]
		stack[activestack]+=1
	elif action == 'RecieveTote':
		dt = 2
		bot.load += 1
	elif action == 'RecieveLitter':
		dt =2
	elif action == 'UseLitter':
		dt= 5
		dp = 6
	elif action == 'GreedyStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = GreedyStack(bot, stacks, maxstack)
		stacks[bot.owned]+=bot.load
	elif action == 'LazyStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = LazyStack(stacks)
		stacks[bot.owned]+=bot.load
	elif action == 'SelfishStack':
		dt = 3
		dp = 2*bot.load
		bot.owned = SelfishStack(bot,stacks,maxstack)
		stacks[bot.owned]+=bot.load
	elif action == 'CopStack':
		dt = 3
		#give points if there are 2 coop bins
		#remove Coop stack from actions
	else:
		raise TypeError
	if (bot.ind+1) == len(bot.actions):
		bot.ind=0
	else:
		bot.ind +=1
	bot.time.append(dt)
	bot.points.append(dp)
	return(bot, stacks,bins)


def pick(alliance):
	#might need to fix so that it picks the first one with the lowest time
	activebot = firstMin([sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time)])
	return(activebot)

def RunMatch(alliance):
	elaspedtime = 0
	maxtime = 135
	bins = 4
	maxstack = 4
	#todo: add in coop thingy
	stacks = [0,0,0,0,0,0,0,0,0,0]
	while elaspedtime < maxtime:
		print elaspedtime, "\t",
		elaspedtime = max(sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time))
		activebot = pick(alliance)
		print alliance[activebot].name
		updatedbot,stacks,bins = Iterate(alliance[activebot],stacks,bins,maxstack)
		alliance[activebot]= updatedbot
	robotresults = []
	for i in alliance:
		print i.points
		i.points= list(cumsum(i.points))
		i.time = list(cumsum(i.points))
		print
		print i.points
		robotresults.append([i.time,i.points])
		print "----------"
	return robotresults
# def placebin



r1 = Robot(['LoadTote','move','LazyStack'],"first bot")
r2 = Robot(['LoadTote','LoadTote','GreedyStack'],"second bot")
r3 = Robot(['LoadTote','LoadTote','LoadTote','move','SelfishStack'],"third bot")
alliance = [r1,r2,r3]
Results=RunMatch(alliance)
