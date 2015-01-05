 
  
  MatchLength <- 135
  stacks<-c(0,0,0,0,0,0,0,0,0,0)
  Robot1Time <-c(0)
  Robot1Points<-c(0)
  Robot1Index <- 1
  Robot1Actions <- c('UpTote','UpTote','Uptote','LazyStack')

  Robot2Time<-c(0)
  Robot2Points<-c(0)
  Robot2Index <-1
  Robot2Actions <- c('UpTote','Uptote','GreedyStack')

  Robot3Time<-c(0)
  Robot3Points<-c(0)
  Robot3Index <-1
  Robot3Actions <- c('UpTote','UpTote','Uptote','SelfishStack')

  load
  activestack
  owners <- c(0,0,0)

increment <- function(action){
  # Asign the delta points and time for an action
  
  #unless overriden, the action scores 0 poins
  dp <-0
  #     This is the number of seconds it takes to do each action. Edit this if you want to customise it.   

  #make sure there are enough bins
  if(action == 'StackBin' && as.numeric(bins)>0){assign('bins',bins-1,envir = .GlobalEnv)}

  # The chance to knok over the stack every time they place one on. Edit this.
  messChance <- 10

  dt <- switch(action,
              'UpTote'=4,
              'UpBin'=5,
              'UseLitter'=6,
              'StackTote'=3,
              'LazyStack'=,
              'SelfishStack'=,
              'GreedyStack'=,
              'StackBin'=6,
              'GetLitter'=3,
              'GetTote'=8,
              'BlockNoodle'=9,
              'ReclaimLitter'=7,
              'CopDrop'=5,
              'CopStack'=6,
              'PrepStack'=2
  )
  index <-switch(action,
    'LazyStack'= LazyStack(),
    'SelfishStack'= SelfishStack(4,load,stackindex),
    'GreedyStack'=GreedyStack)

  dp <- switch(action,
    'Upbin'= if(bins>0){4*stacks[index]}


    'LazyStack'=
    'SelfishStack'=
    'GreedyStack'=
    'UseLitter'=,
    'ReclaimLitter'=,
    'UpBin'=)
  #Don't pick up a bin if there are no bins
  if(action == 'UpBin' && bins==0){dt<-0}
  
  if(action == 'StackTote'){
    dp<-2
    assign('stack',stack+1,envir = .GlobalEnv)
    if (as.numeric(sample(c(1:100),1))<messChance){
      #magic numbers for time to pickup and load a tote
      dt <- dt+ ((stack)*(3+5))
      
    }
  }
  if(action == 'LazyStack'){
    dp <- 2*load
    stacks[LazyStack()]<-stacks[LazyStack()]+load
 }
  if(action == 'UseLitter'){
    dp <-6
  }
  if(action == 'ReclaimLitter'){
    dp -> 1
  }
  returnv <- c(dt,dp)
}


runTime <- function(action){
  a <- increment(action)
  if(action == 'StackBin' && as.numeric(bins)>0){assign('bins',bins-1,envir = .GlobalEnv)}
  b <- a[1]
}
runPoints <- function(action){
  a <- increment(action)
  b <- a[2]
}




###################################
# TODO, move robot actions to a global variable here
###################################

LazyStack<-function(){
  openstacks <- which(stacks == min(stacks))
  assign('activestack',openstacks[1],envir=.GlobalEnv)
  index <- openstacks[1]
}

GreedyStack<-function(maxstack, load){
  openstacks <- subset(stacks, stacks < (maxstack-load))
  beststack <- which(openstacks==max(openstacks))
  assign('activestack',beststacks[1],envir=.GlobalEnv)
  index <- beststack[1]
}

SelfishStack <-function(maxstack,load, owner){
  if (owner != 0  && stacks[owner]< maxstack-load){
    assign('activestack',owner,envir=.GlobalEnv)
    assign('owners'[activebot],owner)
    return(owner)
  }
  else{
    index <-LazyStack(maxstack,load)
    assign('owners'[activebot],index)
    returnv <-index
  }
}

Turn <- function(){
  #which robot is furthest behind in time
  fix<-which.max(max(Robot1Time,Robot2Time,Robot3Time))
  #find out how many they cary in a load and assign it
  actions <- switch(toString(fix),
    "1"=Robot1Actions,
    "2"=Robot2Actions,
    "3"=Robot3Actions)
  loadsize <- length(which(actions == "UpTote" || actions == "GetTote"))
  assign('load',loadsize, envir=.GlobalEnv)

  #return robot number
  returnv <-toString(fix[1])
}

Step <- function(robot){
  actions <- switch(toString(robot),
    "1"=Robot1Actions,
    "2"=Robot2Actions,
    "3"=Robot3Actions)
  index <- switch(toString(robot),
    "1"=Robot1Index,
    "2"=Robot2Index,
    "3"=Robot3Index)
  #find the the dt and dp from the action
  values <- increment(actions[index])

#assign values to the global point holders
  if (toString(robot)== 1){
    assign('Robot1Time',c(Robot1Time,values[1]),envir=.GlobalEnv)
    assign('Robot1Points', c(Robot1Points,values[2]),envir=.GlobalEnv)
  }
  else if (toString(robot) == 2){
    assign('Robot2Time',c(Robot2Time,values[1]),envir=.GlobalEnv)
    assign('Robot2Points', c(Robot2Points,values[2]),envir=.GlobalEnv)
  }
  else if (toString(robot)==3){
    assign('Robot3Time',c(Robot3Time,values[1]),envir=.GlobalEnv)
    assign('Robot3Points', c(Robot3Points,values[2]),envir=.GlobalEnv)
  }

#incriment index

  if (toString(robot)== 1){
      if (index == length(Robot1Index)){
        assign('Robot1Index',1,envir=.GlobalEnv)
      }
      else{
        assign('Robot1Index',Robot1Index+1,envir=.GlobalEnv)
      }
  }

  else if (toString(robot) == 2){
    if (index == length(Robot2Index)){
        assign('Robot2Index',1,envir=.GlobalEnv)
      }
    else{
      assign('Robot2Index',Robot2Index+1,envir=.GlobalEnv)
    }
  }

  else if (toString(robot)==3){
      if (index == length(Robot3Index)){
        assign('Robot3Index',1,envir=.GlobalEnv)
      }
      else{
        assign('Robot3Index',Robot3Index+1,envir=.GlobalEnv)
      }
  }

hotfix <- 0
}

#Reset Score
score <- c()

#Set up Graph
  plot.new()
  plot(c(0,MatchLength),c(0,100),col=rgb(0,0,0,0),xlab= 'Seconds', ylab = 'Points')

runs <- 0
#run the matches
while (runs < 100){
  #reset globals
  assign('bins',4,envir = .GlobalEnv)
  assign('Stacks',stacks<-c(0,0,0,0,0,0,0,0,0,0),envir = .GlobalEnv)
  elaspedtime <- 0
  
  while (elaspedtime <MatchLength){
    #find which robot is most behind and run it
    activebot <- Turn()
    #assign the points for that bot
    hotfixbad<-step(activebot)
    #find how long the match is
    elaspedtime <- max(c(cumsum(Robot1Time),cumsum(Robot2Time),cumsum(Robot3Time)))
  }
  PointHold <- cumsum(PointHold)
  TimeHold <- cumsum(TimeHold)
  score <- c(score, max(PointHold))
  lines(TimeHold,y=PointHold,col=rgb(0, 0, 0, 0.05))
  runs <- runs +1
}


#Plotting stuff for the end
  lines(c(0,MatchLength/2, MatchLength),c(mean(score),mean(score),mean(score)),col ='red')
  text((MatchLength/2),mean(score),paste("Average points: ",mean(score)))
  plot.window(c(0,200),c(0,max(score)))
  #plot(density(score),main="Disribution of Points",xlab="Points",ylab="Density")
  text(mean(score),0.04,paste("Average points: ",mean(score)))