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
	xvalues=list(x_y.keys()) ; xvalues.sort()   ##sort by  xvalues
	if len(yvalues) <3:
		f4.write('no\t%s'%(eachline))
		continue
	y1=yvalues[0]; y2=yvalues[1]; y3=yvalues[2]   ###the max three yvalues.
	if 1 < y1/y2 <10 and 1< y1/y3 <10 and 1/4 <=y2/y3<= 4 and (len(yvalues)==3 or (len(yvalues)>3 and min(y2,y3)>=5*yvalues[3])):  ##the exra peaks (if there are) are very small.
		x1=0;x2=0;x3=0
		for x in xvalues:
			if x_y[x]==y1:
				x1=x
			if x_y[x]==y2 and x2==0:  ##the conditional here can work well when y2==y3 and make the x2<x3.
				x2=x
			elif x_y[x]==y3 and (y2 !=y3 or (y2==y3 and x2!=0)):
				x3=x
		if x2>x3:
			tmpx=x2;tmpy=y2
			x2=x3; y2=y3
			x3=tmpx; y3=tmpy ##change the information of x2/y2 and x3/y3 to ensure the x2<x3
		if x1>x2 and x1<x3: #x1 is the middle point
			xvalues=[]
			for i in range(0,len(e_sp)):
				if '/' in e_sp[i]:
					xvalues.append(float(e_sp[i].split('/')[0]))  ##record all of the peaks and troughs
			if xvalues.index(x1) -xvalues.index(x2) ==2:
				va_1_x=xvalues[xvalues.index(x1)-1]  ##ideal condition
			else:
				va_1_x=(x1+x2)/2  ##there may be a small unexpected peak between x1 and x2
			if xvalues.index(x3) -xvalues.index(x1) ==2:
				va_2_x=xvalues[xvalues.index(x1)+1]  ##ideal condition
			else:
				va_2_x=(x1+x3)/2  ##there may be a small unexpected peak between x1 and x2
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
