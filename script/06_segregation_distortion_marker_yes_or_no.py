import sys

f1 = open(sys.argv[1]) # input the  bottom and top valve of hist produced by R
f2 = open(sys.argv[2]) # input the norm reads matrix file
f3 = open(sys.argv[3],'w') # the contig scores
f4= open(sys.argv[4],'w') # output the middle file including yes no

dict_va={}
for eachline in f1:
	flag=0
	e_sp = eachline.strip().split('\t')
	x_y={}
	for i in range(0,len(e_sp)):
		if '/' in e_sp[i] and i%2==1:  ##only record the peaks
			x_y[float(e_sp[i].split('/')[0])]=float(e_sp[i].split('/')[1])  ##x_y[x]=y
	yvalues=list(x_y.values()) ; yvalues.sort() ;yvalues.reverse()  ##sort by  peak values
	allyvalues=[]
	allxvalues=[]
	for i in range(0,len(e_sp)):
		if '/' in e_sp[i]:
			allxvalues.append(float(e_sp[i].split('/')[0]))
			allyvalues.append(float(e_sp[i].split('/')[1]))
	if len(yvalues) ==1:
		f4.write('no\t%s'%(eachline))
		continue
	y1=yvalues[0]; y2=yvalues[1]  ###two yvalues.
	#if (len(yvalues) ==2 and y1/y2 <5) or (len(yvalues) >2 and y1/y2 <5 and y2>=15*yvalues[2]):  ##ignore the third small peak
	if len(yvalues) ==2 and y1/y2 <5 :
		x1=''; x2=''
		for x in allxvalues:
			if x not in x_y:
				continue
			if x_y[x]==y1 and x1=='':  ##"x1==''" works when y1=y2.
				x1=x
			if x_y[x]==y2 and x1 !=x : ##"x1 !=x" works when y1=y2.
				x2=x
		tmpx1=min(x1,x2); tmpx2=max(x1,x2);x1=tmpx1;x2=tmpx2  ##to ensure x1<x2
		if abs(allxvalues.index(x2) -allxvalues.index(x1)) !=2:  ##allow no unexpected peaks between y1 and y2
			f4.write('no\t%s'%(eachline))
			continue
		if allyvalues[allxvalues.index(x2)-1]/min(y1,y2) >0.5:
			f4.write('no\t%s'%(eachline))
			continue    ###the valley is too high to distinguish the y1 and y2
		if x1*3 < x2: ##x2/x1 >1,  persume the first peak presents 0 and the second peak presents 1
			va_1_x=allxvalues[allxvalues.index(x2)-1]
			va_2_x=x2+(x2-va_1_x)   ##va_2_x is an estimated vlaue
		else: ##means the first peak presents 1 and the second peak presents 2
			va_2_x=allxvalues[allxvalues.index(x2)-1]
			va_1_x=x1-(va_2_x-x1)  ##va_1_x is an estimated vlaue
		dict_va[e_sp[0].strip()] = [va_1_x,va_2_x]
		f4.write('yes\t%s'%(eachline))
		flag=1
	elif  len(yvalues) >2 and y1/y2 <5  and (len(yvalues)==3 or (len(yvalues)>3 and y2>=5*yvalues[2])): ### allow the y2/y3 to be infinite ##the exra peaks (if there are) are very small.
		y1=yvalues[0]; y2=yvalues[1]; y3=yvalues[2]   ###the max three yvalues.
		x1=0;x2=0;x3=0
		for x in allxvalues:
			if x not in x_y:
				continue
			if x_y[x]==y1:
				x1=x
			if x_y[x]==y2 and x2==0:  ##the conditional here can work well when y2==y3 and make the x2<x3.
				x2=x
			elif x_y[x]==y3 and (y2 !=y3 or (y2==y3 and x2!=0)):
				x3=x
		if max(x1,x2,x3)==x3 or min(x1,x2,x3)==x3:
			if abs(allxvalues.index(x2) -allxvalues.index(x1)) !=2:  ##allow no unexpected peaks between y1 and y2
				f4.write('no\t%s'%(eachline))
				continue
			if allyvalues[int((allxvalues.index(x2) +allxvalues.index(x1))/2)]/min(y1,y2) >0.5:
				f4.write('no\t%s'%(eachline))
				continue  ###the valley is too high to distinguish the y1 and y2
			tmpx=[x1,x2,x3]; tmpx.sort(); x1=tmpx[0]; x2=tmpx[1];x3=tmpx[2]   ###to ensure the x1<x2<x3
			if allxvalues.index(x2) -allxvalues.index(x1) ==2:
				va_1_x=allxvalues[allxvalues.index(x2)-1]  ##ideal condition
			else:
				va_1_x=(x1+x2)/2  ##there may be a small unexpected peak between x1 and x2
			if allxvalues.index(x3) -allxvalues.index(x2) ==2:
				va_2_x=allxvalues[allxvalues.index(x2)+1]  ##ideal condition
			else:
				va_2_x=(x2+x3)/2  ##there may be a small unexpected peak between x1 and x2
			dict_va[e_sp[0].strip()] = [va_1_x,va_2_x]
			f4.write('yes\t%s'%(eachline))
			flag=1  ##positive result
	if flag==0:
		f4.write('no\t%s'%(eachline))
for eachline in f2:
	esp = eachline.strip().split('\t')
	if esp[0] in dict_va:
		f3.write('%s'%esp[0])
		for it in  esp[1:]:
			if float(it)< dict_va[esp[0]][0]:
				f3.write('\t0')
			elif dict_va[esp[0]][0] <= float(it) <= dict_va[esp[0]][1] :
				f3.write('\t1')
			else:
				f3.write('\t2')
		f3.write('\n')
f1.close()
f2.close()
f3.close()
f4.close()
