import os
import sys

flag=0
f1=open(sys.argv[1]) ##f1=open('marker.correlation.out')  correlation.out
f2=open(sys.argv[2],'w')   ####f2=open('strong_correlations_marker_tmp','w')  correlation>0.99 marker
linked={}
for line in f1:
	line =line.split()
	if flag==0:
		names=line
	elif flag >1:
		linked[line[0].split('"')[1]]=[]
		for i in range(1,flag):
			if line[i] =='NA':
				print(line[0].split('"')[1],names[i-1].split('"')[1],line[i])
				continue
			if round(float(line[i]),2)>=0.99:
				f2.write('{0}\t{1}\t{2}\n'.format(line[0].split('"')[1],names[i-1].split('"')[1],line[i]))
	flag+=1
f1.close()
f2.close()

linked={}
ref=''
f1=open(sys.argv[2])  ##f1=open('strong_correlations_marker_tmp')   correlation>0.99 marker
for line in f1:
	line =line.split()
	if round(float(line[-1]),2)  <=0.995:
		continue
	if line[0] != ref and ref !='':
		map.sort()
		if map[0] not in linked:
			linked[map[0]]=[]
		linked[map[0]].append(ref)
	if line[0] != ref:
		ref =line[0]
		map=[]
	if line[0] == ref:
		map.append(line[1])
map.sort()
if map[0] not in linked:
	linked[map[0]]=[]
linked[map[0]].append(ref)

f2=open(sys.argv[3],'w')  ## redundant markers #f2=open('strong_correlations_marker','w')
for i in linked:
	f2.write('{0}\t'.format(i))
	for j in linked[i]:
		f2.write('{0},'.format(j))
	f2.write('\n')
f2.close()
