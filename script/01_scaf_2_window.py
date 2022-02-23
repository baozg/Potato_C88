import os
import sys

f1=open(sys.argv[1])   ##  scaf_len file
win=int(sys.argv[2])  ##window size
f2=open(sys.argv[3],'w')   ##output scaf_window_id

f2.write('#win\tscaf\tscaf_len\tstart\tend\n')
flag=1
for line in f1:
	line=line.split()
	start=1
	for i in range(0,int(line[-1])//win):
		f2.write('Win{0}\t{1}\t{2}\t{3}\t{4}\n'.format(flag,line[0],line[-1],start,start+win-1))
		start += win
		flag+=1
	if start <int(line[-1]):
		f2.write('Win{0}\t{1}\t{2}\t{3}\t{4}\n'.format(flag,line[0],line[-1],start,line[-1]))
		flag+=1
f1.close()
f2.close()
