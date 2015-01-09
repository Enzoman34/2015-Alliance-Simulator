
class Robot(object):
	"""Holding all of the variables"""
	def __init__(self, actions,name,risk):
		super(Robot, self).__init__()
		self.ind = 0
		self.actions = actions
		self.time = [0]
		self.points = [0]
		self.owned = 1
		self.load = 0
		self.name = name
		self.timesum = [0]
		self.pointsum = [0]
		self.risk = risk

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

def stack(bot, stacks, maxstack, action):
	#figure out target stack
	try:
		if action=="GreedyStack":
			bot.owned = GreedyStack(bot, stacks, maxstack)
		elif action == "LazyStack":
			bot.owned = LazyStack(bot, stacks, maxstack)
			#hotfix
		elif action == "SelfishStack":
			bot.owned = SelfishStack(bot, stacks, maxstack)
	except:
		print ("Out of stacking space")
	dt = 3
	#print
	#print action,"load",bot.load, "targetstack",stacks[bot.owned], "ind",bot.ind
	if stacks[bot.owned]+bot.load > maxstack:
		stacks[bot.owned]+= float(maxstack-stacks[bot.owned])
		bot.load = bot.load -((maxstack-stacks[bot.owned])+1)
		dp = 2* ((maxstack-stacks[bot.owned])+1)
		if bot.load >0:
			bot.ind += -1
	else:
		stacks[bot.owned]+=float(bot.load)
		dp = 2*bot.load
		bot.load=0
	#print "load",bot.load, "ind",bot.ind
	return bot, stacks, dt, dp

def Iterate(bot,stacks,bins, maxstack,value):
	action = bot.actions[bot.ind]
	#print action, bot.load,
	#Assign time and point values for each action

	Atotes=28

	dp=0
	dt=0
	if action == 'move':
		dt = 1
		dp = 0
	elif action == 'LoadTote':
		if sum(stacks)-Atotes>0:
			dt = 4
			bot.load +=1
		else:
			bot.actions[bot.ind]="RecieveTote"
			return(Iterate(bot,stacks,bins, maxstack,value))
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
		dt = 7
		bot.load += 1
	elif action == 'RecieveLitter':
		dt =2
	elif action == 'UseLitter':
		dt= value
		dp = 6
	elif action == 'GreedyStack':
		bot, stacks,dt, dp =stack(bot, stacks, maxstack, action)
	elif action == 'LazyStack':
		bot, stacks,dt, dp =stack(bot, stacks, maxstack, action)
	elif action == 'SelfishStack':
		bot, stacks,dt, dp =stack(bot, stacks, maxstack, action)
	elif action == 'CopStack':
		dt = 3
		#give points if there are 2 coop bins
		#remove Coop stack from actions
	else:
		raise TypeError
	bot.time.append(dt)
	bot.points.append(dp)
	return(bot, stacks,bins)

def pick(alliance):
	#might need to fix so that it picks the first one with the lowest time
	activebot = firstMin([sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time)])
	return(activebot)

def RunMatch(alliance,bins,maxstack,value):
	elaspedtime = 0
	maxtime = 135
	#todo: add in coop thingy
	stacks = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	while elaspedtime < maxtime:
		#print sum(alliance[0].time)
		elaspedtime = max(sum(alliance[0].time),sum(alliance[1].time),sum(alliance[2].time))
		activebot = pick(alliance)
		updatedbot,stacks,bins = Iterate(alliance[activebot],stacks,bins,maxstack,value)
		if (updatedbot.ind+1) >= len(updatedbot.actions):
			updatedbot.ind=0
		else:
			updatedbot.ind +=1
		alliance[activebot].timesum.append(sum(alliance[activebot].time))
		alliance[activebot].pointsum.append(sum(alliance[activebot].points))
		alliance[activebot]= updatedbot
	robotresults = []
	for i in alliance:
		robotresults.append([i.timesum,i.points])
	return robotresults
r1 = Robot(['move','LoadTote','move','LoadTote','move','SelfishStack','move'],"First bot",1)
r2 = Robot(['LoadTote','move','LoadTote','move','SelfishStack','move'],"Second bot",1)
r3 = Robot(['LoadTote','move','LoadTote','move','LoadTote','SelfishStack','move','move','RecieveLitter','UseLitter','LoadBin','move','move','StackBin','move'],"Noodles",1)
r4 = Robot(['LoadTote','move','LoadTote','move','LoadTote','SelfishStack','move','move','LoadBin','move','move','StackBin','move'],"No Noodles",1)
alliance1 = [r1,r2,r3]
alliance2 = [r1,r2,r4]
Results=[]
for a in range(1,10):
	match = RunMatch(alliance1,4,4,a)
	Results.append(['noodmore',match])
	match = RunMatch(alliance2,4,4,a)
	Results.append(['noodless',match])

resultTable=[]
for match in range(1,10):
        for robot in range(0,3):
                row=[]
                for action in range(0,len(Results[match][1][robot])):
                        row.append(alliance1[robot].name)
                        row.append(Results[match][1][robot][action][0])
                        row.append(Results[match][1][robot][action][1])
                        row.append(match)
                        row.append(Results[match][0])
                resultTable.append(row)

print (resultTable)
##print "col1"
##print col1
##print "col2"
##print col2
##print "col3"
##print col3
##print "col4"
##print col4
##print "col5"
##print col5
