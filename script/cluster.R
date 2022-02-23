args<-commandArgs(TRUE)

data<- read.table(args[1],head=FALSE,row.names=1,sep="\t")
data <- t(as.matrix(data))
dd <- as.dist(1 - cor(data))
hc <- hclust(dd,method = "ward.D2")
groups<-cutree(hc, k=args[3])
write.table(groups,file=args[2])
q()
