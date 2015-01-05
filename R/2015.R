
MatchLength <- 135

increment <- function(action){
  # Asign the delta points and time for an action

  #unless overriden, the action scores 0 poins
  dp <-0
  #     This is the number of seconds it takes to do each action. Edit this if you want to customise it.   
  dt <- switch(action,
               'UpTote'=4,
               'UpBin'=5,
               'UseLitter'=6,
               'StackTote'=3,
               'StackBin'=6,
               'GetLitter'=3,
               'GetTote'=8,
               'BlockNoodle'=9,
               'ReclaimLitter'=7,
               'CopDrop'=5,
               'CopStack'=6,
               'PrepStack'=2
               )
  # The chance to knok over the stack every time they place one on. Edit this.
  messChance <- 10
  
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
  if(action == 'StackBin'){
    #4*stackheigh

    if(bins>0){
      dp<-4*stack
    }
     else{
       dt<-0
     }
    assign('stack',0,envir = .GlobalEnv)
  }
  if(action == 'UseLitter'){
    dp <-6
  }
  if(action == 'ReclaimLitter'){
    dp -> 1
  }
  returnv <- c(dp,dt)
}

runPoints <- function(action){
  a <- increment(action)
  b <- a[1]
}

runTime <- function(action){
  a <- increment(action)
  if(action == 'StackBin' && as.numeric(bins)>0){assign('bins',bins-1,envir = .GlobalEnv)}
  b <- a[2]
}

score <- c()
plot.new()
plot(c(0,MatchLength),c(0,100),col=rgb(0,0,0,0),xlab= 'Seconds', ylab = 'Points')
#   
#   Here are the actions to be done in order for a cycle. Edit them to whatber you want. Any length.
# 
actions <- c('UpTote',
             'StackTote',
             'UpTote',
             'StackTote',
             'UpBin',
             'StackBin')


runs <- 0
while (runs < 100){
  #reset globals
  assign('stack',0,envir = .GlobalEnv)
  assign('bins',4,envir = .GlobalEnv)
  elaspedtime <- 0
  PointHold <- c(0)
  TimeHold <- c(0)
  assign('stack',0,envir = .GlobalEnv)
  while (elaspedtime <MatchLength){
    point <- lapply(actions,function(x)  runPoints(x))
    times <- lapply(actions,function(x)  runTime(x))
    elaspedtime <-Reduce("+",times) + elaspedtime
    PointHold <- c(PointHold, point)
    TimeHold <- c(TimeHold, times)
  }
  PointHold <- cumsum(PointHold)
  TimeHold <- cumsum(TimeHold)
  score <- c(score, max(PointHold))
  lines(TimeHold,y=PointHold,col=rgb(0, 0, 0, 0.05))
  runs <- runs +1
}

#Plotting this
lines(c(0,MatchLength/2, MatchLength),c(mean(score),mean(score),mean(score)),col ='red')
text((MatchLength/2),mean(score),paste("Average points: ",mean(score)))
plot.window(c(0,200),c(0,max(score)))
#plot(density(score),main="Disribution of Points",xlab="Points",ylab="Density")
text(mean(score),0.04,paste("Average points: ",mean(score)))