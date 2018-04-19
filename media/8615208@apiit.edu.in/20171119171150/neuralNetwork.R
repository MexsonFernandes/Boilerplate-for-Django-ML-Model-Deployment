
#--------------------------------------------------------------
# Step 0: Start; Getting the starting time
#--------------------------------------------------------------
cat("\nSTART\n")
startTime = proc.time()[3]
startTime

args<-commandArgs(TRUE)
nameofFile = args[1]
input = args[2]

#--------------------------------------------------------------
# Step 1: Include Library
#--------------------------------------------------------------
cat("\nStep 1: Library Inclusion")
library(nnet)



#--------------------------------------------------------------
# Step 2: Variable Declaration
#--------------------------------------------------------------
cat("\nStep 2: Variable Declaration")
modelName <- "neuralNetwork"
modelName

InputDataFileName=nameofFile
InputDataFileName

training = 50      # Defining Training Percentage; Testing = 100 - Training



#--------------------------------------------------------------
# Step 3: Data Loading
#--------------------------------------------------------------
cat("\nStep 3: Data Loading")
dataset <- read.csv(InputDataFileName)      # Read the datafile
dataset <- dataset[sample(nrow(dataset)),]  # Shuffle the data row wise.

head(dataset)   # Show Top 6 records
nrow(dataset)   # Show number of records
names(dataset)  # Show fields names or columns names



#--------------------------------------------------------------
# Step 4: Count total number of observations/rows.
#--------------------------------------------------------------
cat("\nStep 4: Counting dataset")
totalDataset <- nrow(dataset)
totalDataset



#--------------------------------------------------------------
# Step 5: Choose Target variable
#--------------------------------------------------------------
cat("\nStep 5: Choose Target Variable")
target  <- names(dataset)[integer(input)]   # i.e. RMSD
target



#--------------------------------------------------------------
# Step 6: Choose inputs Variables
#--------------------------------------------------------------
cat("\nStep 6: Choose Inputs Variable")
inputs <- setdiff(names(dataset),target)
inputs
length(inputs)

#Feature Selection
#n=4
#inputs <-sample(inputs, n)



#--------------------------------------------------------------
# Step 7: Select Training Data Set
#--------------------------------------------------------------
cat("\nStep 7: Select training dataset")
trainDataset <- dataset[1:(totalDataset * training/100),c(inputs, target)]
head(trainDataset)    # Show Top 6 records
nrow(trainDataset)    # Show number of train Dataset



#--------------------------------------------------------------
# Step 8: Select Testing Data Set
#--------------------------------------------------------------
cat("\nStep 8: Select testing dataset")
testDataset <- dataset[(totalDataset * training/100):totalDataset,c(inputs, target)]
head(testDataset)
nrow(testDataset)




#--------------------------------------------------------------
# Step 9: Model Building (Training)
#--------------------------------------------------------------
cat("\nStep 9: Model Building -> ", modelName)
formula <- as.formula(paste(target, "~", paste(c(inputs), collapse = "+")))
formula
           
model   <- nnet(formula, trainDataset, size=10, linout=TRUE, skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100)
model



#--------------------------------------------------------------
# Step 10: Prediction (Testing)
#--------------------------------------------------------------
cat("\nStep 10: Prediction using -> ", modelName)
Predicted <- predict(model, testDataset)
head(Predicted)



#--------------------------------------------------------------
# Step 11: Extracting Actual
#--------------------------------------------------------------
cat("\nStep 11: Extracting Actual")
Actual <- as.double(unlist(testDataset[target]))
head(Actual)



#--------------------------------------------------------------
# Step 12: Model Evaluation
#--------------------------------------------------------------
cat("\nStep 12: Model Evaluation")

# Step 12.1: Correlation
r <- cor(Actual,Predicted )
r <- round(r,2)
r

# Step 12.2: RSquare
R <- r * r 
R <- round(R,2)
R

# Step 12.3: RMSE
rmse <- mean(abs(Actual-Predicted))
rmse <- round(rmse,2)
rmse

# Step 12.4: Accuracy
accuracy <- mean(abs(Actual-Predicted) <=1)
accuracy <- round(accuracy,4) *100
accuracy

# Step 12.5: Total Time
totalTime = proc.time()[3] - startTime
totalTime

# Step 12.6: Scatter Plot
png(filename=paste(modelName,"-ScatterPlot.png",sep=''))

plot(Actual,Predicted,main=paste("Actual Vs Predicted\n",modelName),xlab="Predicted", ylab="Actual")#, pch=19)

abline(lm(Actual ~ Predicted,),col="White") 

dev.off()

# Step 12.7: Save evaluation resut 
result <- data.frame(modelName,r,R,rmse,accuracy, totalTime)[1:1,]
result



#--------------------------------------------------------------
# Step 13: Writing to file
#--------------------------------------------------------------
cat("\nStep 13: Writing to file")

# Step 13.1: Writing to file (evaluation result)
write.csv(result, file=paste(modelName,"-Evaluation-Result.csv",sep=''), row.names=FALSE)

# Step 13.2: Writing to file (Actual and Predicted)
write.csv(data.frame(Actual,Predicted), file=paste(modelName,"-ActualPredicted-Result.csv",sep=''), row.names=FALSE)



#--------------------------------------------------------------
# Step 14: Saving the Model
#--------------------------------------------------------------
cat("\nStep 14: Saving the Model ->",modelName)
save.image(file=paste(modelName,"-Model.RData",sep=''))


cat("\nDone")
cat("\nTotal Time Taken: ", totalTime," sec")


#--------------------------------------------------------------
#                           END 
#--------------------------------------------------------------

