import sys
f1 =open(sys.argv[1],'r')
f2 =open(sys.argv[2],'w')

for le in f1:
	esp = le.strip().split()
#	print(esp[0],esp[1:].count('0'))
	if esp[1:].count('0') <= (len(esp[1:])*0.85):
		f2.write(le)
f1.close()
f2.close()
