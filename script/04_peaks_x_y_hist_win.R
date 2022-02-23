args<-commandArgs(TRUE)
d1 <- read.table(args[1],sep="\t",row.names=1)
library(boot)
library(pastecs)
sink(args[2])

for(i in 1:length(d1[,1])){
	d2 <- as.numeric(d1[i,]);
	d2_d<- density(na.omit(d2));
	d2_ts <- ts(d2_d$y);
	d2_tp <-turnpoints(d2_ts);
	cat(row.names(d1)[i],'\t')
	for(it in 1:length(d2_d$x[d2_tp$tppos]))
	{
		cat(d2_d$x[d2_tp$tppos][it],'/',d2_d$y[d2_tp$tppos][it],'\t')
	}
	cat('\n')
}
sink()
