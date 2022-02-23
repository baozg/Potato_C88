#!/public/agis/huangsanwen_group/zhouqian/bin/python3.2


import os
import sys

"""
scaf={}
f1=open('marker_50kb_LG.new')
f2=open('multiple.LG.utg','w')
for line in f1:
	line=line.split()
	if line[5] not in scaf:
		scaf[line[5]]={}
	if line[0] not in scaf[line[5]]:
		scaf[line[5]][line[0]]=[]
	scaf[line[5]][line[0]].append(line[1])
f1.close()
for s in scaf:
	if len(scaf[s])>1:
		f2.write(s)
		for i in scaf[s]:
			f2.write('\t{0}\t{1}'.format(i,len(scaf[s][i])))
		f2.write('\n')
f2.close()

f3=open('decided.multiple.LG.utg','w')
for s in scaf:
	if len(scaf[s])==1:
		continue
	win_num={}
	for lg in scaf[s]:
		win_num[lg]=len(scaf[s][lg])
	num=list(win_num.values()); num.sort(); num.reverse()
	if num[0]<2:
		f3.write(s+'\t-\n')  ###  too few markers.
		continue
	for lg in  scaf[s]:
		if win_num[lg]==num[0] and win_num[lg] >num[1]: ###only one lg has the most marker
			f3.write('{0}\t{1}\n'.format(s,lg))
			break
		elif win_num[lg]==num[0] and win_num[lg] ==num[1]: ###more than one lg has the most marker
			f3.write('{0}\t{1}\n'.format(s,lg))   ###just chose one randomly
			break
f3.close()



decided_utg={}
f1=open('decided.multiple.LG.utg')
for line in f1:
	line=line.split()
	decided_utg[line[0]]=line[1]
f1.close()

f2=open('marker_50kb_LG.new')
f3=open('marker_50kb_LG.flt','w')
for line in f2:
	if 'Marker' in line:
		f3.write(line)
	else:
		utg=line.split()[-2]
		if utg not in decided_utg:
			f3.write(line)
		elif  utg  in decided_utg and  decided_utg[utg]==line.split()[0]:
			f3.write(line)
f2.close()
f3.close()

"""

decided_utg={}
f1=open('ctg_with_multiple_DM_chr')
for line in f1:
	line=line.split()
	if line[1] not in decided_utg and int(line[0]) >2:
		decided_utg[line[1]]=line[2]
	elif line[1] not in decided_utg and int(line[0]) <=2:
		decided_utg[line[1]]='-'
f1.close()

f2=open('marker_50kb_LG.flt')
f3=open('marker_50kb_LG.flt2','w')
for line in f2:
	if 'Marker' in line:
		f3.write(line)
	else:
		utg=line.split()[-2]
		if utg not in decided_utg:
			f3.write(line)
		elif  utg  in decided_utg and  decided_utg[utg]==line.split()[3]:
			f3.write(line)
f2.close()
f3.close()

