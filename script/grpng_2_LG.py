import sys


f1=open(sys.argv[1])   ###f1=open('H4.grpng.txt')
f2=open(sys.argv[2],'w')  ##f2=open('LG'+str(i)+'.map','w')
f2.write('LG\tMarker\tLOD\n')
for line in f1:
	if 'LOD' in line or '--' in line:
		continue
	line=line.split()
	if len(line) <10 or int(line[10]) >10:
		continue
	f2.write('LG{0}\t{1}\t{2}\n'.format(line[10],line[1],'10'))
f1.close()
f2.close()
