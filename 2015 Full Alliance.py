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

def valid(bot,stacks,maxstack):
	for i in stacks:
		if i < maxstack:
			yield i

def firstMin(lis):
	return lis.index(min(lis))

def GreedyStack(bot, stacks, maxstack,):
	if min(stacks) >= maxstack:
		return ValueError
	validstack = list(valid(bot, stacks, maxstack))
	print validstack
	return stacks.index(max(validstack))

def LazyStack(bot,stacks,maxstack):
	if min(stacks) >= maxstack:
		return ValueError
	else:
		return firstMin(stacks)

def SelfishStack(bot,stacks,maxstack):
	if min(stacks) >= maxstack:
		return ValueError
	if maxstack-(stacks[bot.owned]+bot.load)>0: 
		return bot.owned
	else:
		return LazyStack(bot,stacks,maxstack)

def Iterate(bot,stacks,bins, maxstack):
	action = bot.actions[bot.ind]
	print action, bot.load,
	#Assign time and point values for each action
	dp=0
	dt=0
	if action == 'move':
		dt = 1
	elif action == 'LoadTote':
		dt = 6
		bot.load +=1
	elif action == 'LoadBin':
		if(bins >0):
			dt = 6
			bins += -1
		else:
			dt <-0
			dp <- 0
			#remove load bins and stack bins from actions
	elif action == 'StackBin':
		try:
			target =stacks.index(maxstack)
		except :
			target = stacks.index(max(stacks))
		else:
			pass
		finally:
			dt= 4
			dp = 4*stacks[target]
			stacks[target]+=10
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
		exc = -1
		bot.owned = GreedyStack(bot, stacks, maxstack)
		print bot.owned,
		if stacks[bot.owned]+bot.load > maxstack:
			print "g",
			stacks[bot.owned]+= maxstack-stacks[bot.owned]
			bot.load = bot.load-(maxstack-stacks[bot.owned])
			bot.ind += -1
		else:
			stacks[bot.owned]+=bot.load
			dp = 2*bot.load
			bot.load=0
	elif action == 'LazyStack':
		dt = 2
		bot.owned = LazyStack(bot,stacks,maxstack)
		if stacks[bot.owned]+bot.load > maxstack:
			print 'l',
			stacks[bot.owned]+= maxstack-stacks[bot.owned]
			dp <- maxstack-stacks[bot.owned]*2
			bot.load = bot.load-(maxstack-stacks[bot.owned])
			bot.ind += -1
		else:
			stacks[bot.owned]+=bot.load
			dp = 2*bot.load
			bot.load=0
	elif action == 'SelfishStack':
		dt = 3
		bot.owned = SelfishStack(bot,stacks,maxstack)
		if stacks[bot.owned]+bot.load > maxstack:
			print "s",
			stacks[bot.owned]+= maxstack-stacks[bot.owned]
			dp <- maxstack-stacks[bot.owned]*2
			bot.load = bot.load-(maxstack-stacks[bot.owned])
			bot.ind += -1
		else:
			stacks[bot.owned]+=bot.load
			dp = 2*bot.load
			bot.load=0
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
	print stacks
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
		print
		print elaspedtime, "\t",
		elaspedtime = max(sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time))
		activebot = pick(alliance)
		print alliance[activebot].name
		updatedbot,stacks,bins = Iterate(alliance[activebot],stacks,bins,maxstack)
		alliance[activebot]= updatedbot
	robotresults = []
	for i in alliance:
		i.points= list(cumsum(i.points))
		i.time = list(cumsum(i.points))
		robotresults.append([i.time,i.points])
	return robotresults


r1 = Robot(['LoadTote','LoadTote','LazyStack'],"first bot")
r2 = Robot(['LoadTote','LoadTote','GreedyStack'],"second bot")
r3 = Robot(['LoadTote','LoadTote','LoadTote','SelfishStack','LoadBin','StackBin'],"third bot")
alliance = [r1,r2,r3]
Results=RunMatch(alliance)
