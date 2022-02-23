import os
import sys


f1=open(sys.argv[1])  ##input ref_window_marker.id
win_ctg={};ctg_name={}
for line in f1:
	if '#' ==line[0]:
		continue
	line=line.split()
	win_ctg[line[0]]=line[1]
	ctg_name[line[1]]=int(line[2])

f1.close()

ctg_map_pos={}
f2=open(sys.argv[2])  ##utg.map.pos
for line in f2:
	if '#' in line[0]:
		continue
	line=line.split()
	ctg_map_pos[line[0]]=[line[2],line[3]]
f2.close()

ctg_group={}
f3=open(sys.argv[3])  ## win group
for line in f3:
	line=line.split()
	if win_ctg[line[0]] not in ctg_group:
		ctg_group[win_ctg[line[0]]]={}
	if line[1] not in ctg_group[win_ctg[line[0]]]:
		ctg_group[win_ctg[line[0]]][line[1]]=0
	ctg_group[win_ctg[line[0]]][line[1]] +=1
f3.close()


f4=open(sys.argv[4],'w')  ##output file
for c in ctg_group:
	if c in ctg_map_pos:
		f4.write('{0}\t{1}\t{2}'.format(c,ctg_name[c],'\t'.join(ctg_map_pos[c])))
	else:
		f4.write('{0}\t{1}\t-\t-'.format(c,ctg_name[c]))
	num=list(ctg_group[c].values())
	num.sort()
	num.reverse()
	for i in num:
		for j in ctg_group[c]:
			if ctg_group[c][j]==i:
				f4.write('\t{0}:{1}'.format(j,i))
				ctg_group[c].pop(j)
				break
	f4.write('\n')
	ctg_name.pop(c)
for c in ctg_name:
	if c in ctg_map_pos:
		f4.write('{0}\t{1}\t{2}\t-\n'.format(c,ctg_name[c],'\t'.join(ctg_map_pos[c])))
	else:
		f4.write('{0}\t{1}\t-\t-\t-\n'.format(c,ctg_name[c]))
f4.close()
