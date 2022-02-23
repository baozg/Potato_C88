args<-commandArgs(TRUE)

data<-read.table(args[1],head=FALSE,row.names=1)
data <- t(as.matrix(data))
write.table(WGCNA::cor(data),file=args[2])
