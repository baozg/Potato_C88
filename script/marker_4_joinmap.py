import os
import sys

f1=open(sys.argv[1])  ##input   H*_marker
f2=open(sys.argv[2],'w')  ##output file

f2.write('marker')
for i in range(1,109):
	f2.write('\tRH-'+str(i))
f2.write('\n')

for line in f1:
	line=line.split()
	f2.write(line[0])
	for i in line[1:]:
		if i=='0':
			f2.write('\ta')
		elif i =='1':
			f2.write('\th')
		elif i=='2':
			f2.write('\tb')
	f2.write('\n')
f2.close()
f1.close()
