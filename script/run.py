#!/public/agis/huangsanwen_group/zhouqian/bin/python3.2


import re


lg_chr={}    ###the key LG is random; the value LG is consistent with genome chromosome.
lg_chr['LG1']='LG1'
lg_chr['LG11']='LG2'
lg_chr['LG5']='LG3'
lg_chr['LG4']='LG4'
lg_chr['LG8']='LG5'
lg_chr['LG9']='LG6'
lg_chr['LG6']='LG7'
lg_chr['LG12']='LG8'
lg_chr['LG2']='LG9'
lg_chr['LG10']='LG10'
lg_chr['LG7']='LG11'
lg_chr['LG3']='LG12'

f1=open('marker_50kb_LG.tsv')
f2=open('marker_50kb_LG.new','w')

f2.write('LG\tMarker\tGeneticPos\tDMchr\tDMPos/M\tUtg\tNo.\n')
for line in f1:
	line=line.split()
	info=re.split(':|-',line[1])
	marker=info[0]+'_'+str(int(info[1])+1)
	lg=lg_chr[line[0].split('_')[0]]+'_'+line[0].split('_')[1]
	f2.write('{0}\t{1}\t0\t{2}\t{3}\t{4}\t{5}\n'.format(lg,marker,int(line[2][3:]),round(int(line[4])/1000000,2),line[1].split(':')[0],int(info[1])//50000))
f1.close()
f2.close()

