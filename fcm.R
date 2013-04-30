library("e1071")
k <- read.csv('~/Equinight/result1.csv')
cl<-cmeans(k,2,20,verbose=TRUE,method="cmeans")
print(cl)
