library(rPython)

# Load/run the main Python script
python.load("/Users/quinn/Documents/2015-Alliance-Simulator/2015\ Full\ Alliance.py")

# Get the variable
# names <- python.get("col1")
# times <- as.numeric(python.get("col2"))
# points <- as.numeric(python.get("col3"))
test <-as.numeric(python.get(resultTable))

plot(times,points)

Allthedata <- as.data.frame(matrix(c(names,times,points),ncol=3))
names(Allthedata)<- c("Robot","Time","Points")
write.csv(Allthedata,quote=F,row.names=F,file="checkthisout.csv")
