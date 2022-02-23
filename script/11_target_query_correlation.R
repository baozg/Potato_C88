args<-commandArgs(TRUE)

data1<-read.table(args[1],head=FALSE,row.names=1)
data1 <- t(as.matrix(data1))
data2<-read.table(args[2],head=FALSE,row.names=1)
data2 <- t(as.matrix(data2))
write.table(WGCNA::cor(data1,data2),file=args[3])    ###x is the row name; y is the cloumn name
