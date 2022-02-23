import sys
import os


lg={}; marker={}
f1=open(sys.argv[1])  #RH.200samples.combined.grpng.out
for line in f1:
	line=line.split()
	if 'LG' ==line[0]:
		continue
	if line[0] not in lg:
		lg[line[0]]=[]
	lg[line[0]].append(line[1])
	marker[line[1]]=line[2:]
f1.close()

f2=open(sys.argv[2])   ##readnum file

for a in lg:
	readnum_file=open('tmp.readnum_file','w')
	for line in f2:
		if line.split()[0] in lg[a]:
			readnum_file.write(line)
	f2.seek(0)
	readnum_file.close()
	os.system('Rscript cluster.R tmp.readnum_file {0}.readnum.hclust.output.k4 4'.format(a))
	os.system('rm tmp.readnum_file')
f2.close()


output=open(sys.argv[3],'w')
output.write('LG\tMarker\tLOD\n')
for a in lg:
	hclust_file=open(a+'.readnum.hclust.output.k4')
	for line in hclust_file:
		line=line.split()
		if len(line)==1:
			continue
		output.write('{0}_{1}\t{2}\n'.format(a,line[1],line[0].split('"')[1]))
output.close()
