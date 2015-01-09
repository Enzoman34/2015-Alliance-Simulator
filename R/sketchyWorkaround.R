library(rPython)

# Load/run the main Python script
python.load("/Users/quinn/Documents/2015-Alliance-Simulator/2015\ Full\ Alliance.py")

# Get the variable
names <- python.get("col1")
times <- as.numeric(python.get("col2"))
points <- as.numeric(python.get("col3"))

plot(times,points)

Allthedata <- as.data.frame(matrix(c(names,times,points),ncol=3,dimnames=as.list(c("Names","Time","Points"))))
write.table(Allthedata,quote=F)
