assign('stack',0,envir = .GlobalEnv)

# action<-c(
# 'UpTote'=3,
# 'UpBin'=3,
# 'LoadLitter'=3,
# 'UseLitter'=4,
# 'StackTote'=5,
# 'StackBin'=5,

#get means get from human player

# 'GetLitter'=6,
# 'GetTote'=7,
# 'BlockNoodle'=8,
# 'ReclaimLitter'=6)
increment <- function(action){
  dp <-0
#   
#     This swtich statement is the number of seconds it takes to do each action. Edit this if you want to customise it. 
#   
  dt <- switch(action,
               'UpTote'=4,
               'UpBin'=5,
               'UseLitter'=6,
               'StackTote'=3,
               'StackBin'=6,
               'GetLitter'=3,
               'GetTote'=8,
               'BlockNoodle'=9,
               'ReclaimLitter'=7)
# 
# The chance to knok over the stack.
# 
  messChance <- 10



  if(action == 'StackTote'){
    dp<-2
    assign('stack',stack+1,envir = .GlobalEnv)
    if (as.numeric(sample(c(1:100),1))<messChance){
      #magic numbers for time to pickup and load a tote
      dt <- dt+ ((stack)*(3+5))
      
    }
  }
  if(action == 'StackBin'){
    #4*stackheight
    dp<-12
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
  b <- a[2]
}

b <- 0
score <- c()
plot.new()
plot(c(0,135),c(0,100),col=rgb(0,0,0,0),xlab= 'Seconds', ylab = 'Points')
#   
#   Here are the actions to be done in order for a cycle. Edit them to whatber you want. Any length.
# 
actions <- c('UpTote',
               'StackTote',
               'UpTote',
               'StackTote',
               'UpTote',
               'StackTote',
               'UpTote',
               'StackTote',
               'UpTote',
               'StackTote',
               'UpTote',
               'StackTote',
               'GetLitter',
               'UseLitter',
               'UpBin',
               'StackBin')
  

runs <- 0
while (runs < 300){
  elaspedtime <- 0
  PointHold <- c(0)
  TimeHold <- c(0)
  assign('stack',0,envir = .GlobalEnv)
  while (elaspedtime <135){
    point <- lapply(actions,function(x)  runPoints(x))
    times <- lapply(actions,function(x)  runTime(x))
    elaspedtime <-Reduce("+",times) + elaspedtime
    PointHold <- c(PointHold, point)
    TimeHold <- c(TimeHold, times)
  }
  PointHold <- cumsum(PointHold)
  TimeHold <- cumsum(TimeHold)
  holder <- as.data.frame(matrix(c(PointHold,TimeHold),nrow=2,byrow=T),row.names=(c('Points','Times')))
  results<- t(holder)
  results<-subset(results,(results[,2])<135,select=c(Times,Points))
  score <- c(score, max(results[,2]))
  lines(results,col=rgb(0, 0, 0, 0.05))
  runs <- runs +1
}


lines(c(0,100, 200),c(mean(score),mean(score),mean(score)),col ='red')
text((135/2),mean(score),paste("Average points: ",mean(score)))
plot.window(c(0,200),c(0,max(score)))
plot(density(score),main="Disribution of Points",xlab="Points",ylab="Density")
text(mean(score),0.04,paste("Average points: ",mean(score)))