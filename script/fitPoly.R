args<-commandArgs(TRUE)
name <- args[1]

library(data.table)
library(fitPoly)

d <- fread("diplotig.fitPoly.input.tsv.gz",sep="\t",header=T)
saveMarkerModels(4,data=d,filePrefix=name,ncores=64)
