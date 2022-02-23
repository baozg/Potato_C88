import re
import sys

f1=open(sys.argv[1])  ##input window information  ###remove duplicated scaffold ids.
f2=open(sys.argv[2],'w')   ##output normalized reads number within a window.
mq=int(sys.argv[3])    ##MQ threshold

f2.write('#window\treal_reads\tratio\tnorm_reads\n')

ctg_win={}; win_num={}; win_srt=[]
for  line in f1:
	if '#' in line:
		continue
	lsp=line.split()
	win=lsp[0]; win_num[win]=0; win_srt.append(win)
	if lsp[1] not in ctg_win:
		ctg_win[lsp[1]]={}
	ctg_win[lsp[1]][win]=[int(lsp[-2]),int(lsp[-1])]  ##ct_win[Scaf16_lg0][Win18]=[1,89609]
f1.close()

total=0
for line in sys.stdin:  ##read in the sam lines from *.bam
	line=line.split()
	if line[5]=='*':
		continue
	if 'H' in line[5] or 'S' in line[5]  or ('NM:i:' in line[11] and int(line[11][5:]) >3) :
		continue
	if int(line[4]) <mq:   ##can add other criteria
		continue
	total+=1; ctg=line[2]
	if ctg not in ctg_win:
		continue
	wins=list(ctg_win[ctg].keys())
	if len(wins) ==1:
		w=wins[0]   ##find the right window
	else:
		flag=0
		for i in wins:
			if ctg_win[ctg][i][0] <=int(line[3]) <= ctg_win[ctg][i][1]:
				w=i ;flag=1
				break
		if flag==0:
			print('Error1')
	win_num[w]+=1
wins.sort()
for w in win_srt:
	f2.write('{0}\t{1}\t{2}\t{3}\n'.format(w,win_num[w],round(win_num[w]/total,10),int(win_num[w]/total*10000000)))
f2.close()
