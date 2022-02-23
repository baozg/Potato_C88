args<-commandArgs(TRUE)

data<-read.table(args[1],head=FALSE,row.names=1)
data <- t(as.matrix(data))
cordata <- WGCNA::cor(data)
write.table(cordata,file=args[2])

library(pheatmap)

#pdf(args[3])
png(args[3],res=600,width=2000,height=2000,units="px")
pheatmap(cordata,cluster_row=F,cluster_cols=F,show_rowname=F,show_colnames=F)
dev.off()
