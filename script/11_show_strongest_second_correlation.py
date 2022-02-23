import sys
import pprint

f1=open(sys.argv[1])   ###input query items file
f2=open(sys.argv[2])  ##input target items file
f3=open(sys.argv[3])  ##marker.correlation.out
f4=open(sys.argv[4],'w')  ##Output file

f4.write('#Query_marker\tStrongest_cor_marker\tStrongest_cor_value\tLG\tSecond_cor_marker\tSecond_cor_value\tLG\tThird_cor_marker\tThrid_cor_value\tLG\tForth_cor_marker\tForth_cor_value\tLG\tFifth_cor_marker\tFifth_cor_value\tLG\n')

pp = pprint.PrettyPrinter(indent=4)


query={}
for line in f1:
    query[line.split()[0]]=0
f1.close()

target_iterm={}
for line in f2:
    if line.split()[0]=="LG":
        continue
    target_iterm[line.split()[1]]=line.split()[0]
f2.close()


flag=0
for line in f3:
    line=line.strip().split()
    if flag==0:
        pos={}
        for i in range(0,len(line)):
            if line[i].split('"')[1] in target_iterm:
                pos[i+1]=line[i].split('"')[1]
    if flag:
        if line[0].split('"')[1] in query:
            f4.write(line[0].split('"')[1]+'\t')
            q_corr={}
            for i in range(1,len(line)):
                if i in pos:
                    q_corr[pos[i]]=float(line[i])
            cor_value=list(q_corr.values()); cor_value.sort(); cor_value.reverse()
            for ref in q_corr:
                if q_corr[ref]==cor_value[0]:
                    f4.write('{0}\t{1}\t{2}\t'.format(ref,round(q_corr[ref],3),target_iterm[ref]))
                    break
            q_corr.pop(ref)   ##incase the cor_value[0]==cor_value[1]
            for ref in q_corr:
                if q_corr[ref]==cor_value[1]:
                    f4.write('{0}\t{1}\t{2}\t'.format(ref,round(q_corr[ref],3),target_iterm[ref]))
                    break
            q_corr.pop(ref)   ##incase the cor_value[0]==cor_value[1]
            for ref in q_corr:
                if q_corr[ref]==cor_value[2]:
                    f4.write('{0}\t{1}\t{2}\t'.format(ref,round(q_corr[ref],3),target_iterm[ref]))
                    break
            for ref in q_corr:
                if q_corr[ref]==cor_value[3]:
                    f4.write('{0}\t{1}\t{2}\t'.format(ref,round(q_corr[ref],3),target_iterm[ref]))
                    break
            q_corr.pop(ref)   ##incase the cor_value[0]==cor_value[1]
            for ref in q_corr:
                if q_corr[ref]==cor_value[4]:
                    f4.write('{0}\t{1}\t{2}\n'.format(ref,round(q_corr[ref],3),target_iterm[ref]))
                    break
    flag+=1
f3.close()
f4.close()
