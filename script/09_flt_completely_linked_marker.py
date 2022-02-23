import sys
import re

f1=open(sys.argv[1])  ##Input all scaffolds
f2=open(sys.argv[2]) ##input strong_correlations_marker
f3=open(sys.argv[3],'w')  ##output file

rmd={}
for line in f2:
	line=line.split()
	for i in line[1].split(',')[:-1]:
		rmd[i]=line[0]
f2.close()
for line in f1:
	if line.split()[0] not in rmd:
		f3.write(line)
f3.close()
f1.close()
