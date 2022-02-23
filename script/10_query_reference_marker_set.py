import os
import sys

f1=open(sys.argv[1])  ##readnum file of all markers
f2=open(sys.argv[2])  ##anchored markers
f3=open(sys.argv[3],'w')  ##output target.marker.readnum
f4=open(sys.argv[4],'w')  ##output query.marker.readnum

target={}
for line in f2:
	if 'LG' !=line.split()[0]:
		target[line.split()[1]]=0
f2.close()

for line in f1:
	if line.split()[0] in target:
		f3.write(line)
	elif line.split()[0] not in target:
		f4.write(line)
f3.close()
f4.close()
f1.close()
