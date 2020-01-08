def BinaryToDecimal(Bin):   #function to convery binary no. to decimal
	dec=0 #decimal equivalent
	n=len(Bin)
	i=0
	for i in range(n):
		dec=dec+((int(Bin[i:i+1]))*(2**(n-i-1)))
	return dec
def DecimalToBinary(dec,NoOfBits): #function to convert decimal no. into binary
	Bin=''
	while dec>1:
		Bin+=str(dec%2)
		dec=int(dec/2)
	if dec == 1:
		Bin+='1'
	else:
		Bin+='0'
	Bin=Bin[::-1]
	if len(Bin)<NoOfBits:
		Bin='0'*(NoOfBits-len(Bin)) + Bin
	return Bin

def Get_PrimeImplicant(Min): #to generate prime implicants 
	M=''
	NoOfBits=len(Min)
	for i in range(NoOfBits):
		if Min[i]!='_':
			if i==0:
				if Min[i]=='0':
					M+='a\''
				else:
					M+='a'
			if i==1:
				if Min[i]=='0':
					M+='b\''
				else:
					M+='b'
			if i==2:
				if Min[i]=='0':
					M+='c\''
				else:
					M+='c'
			if i==3:
				if Min[i]=='0':
					M+='d\''
				else:
					M+='d'
	return(M)

def cases(Old,New,numVar): #various stages of the algorithm
	New=[]
	l=len(Old)
	for i in range(l-1):
		New.append([])
	l=len(New)
	A=[]
	for z in range(0,l):
		for i in range(1,len(Old[z]),2):
			for j in range(1,len(Old[z+1]),2):
				c=0
				k=0
				for k in range(numVar):
					if Old[z+1][j][k]!=Old[z][i][k]:
						c+=1
				if c==1:
					A.append(Old[z][i])
					A.append(Old[z+1][j])
					New[z].append([])
					New[z][len(New[z])-1]=[Old[z+1][j-1]+Old[z][i-1]]
					k=0
					while Old[z+1][j][k]==Old[z][i][k] and k<numVar:
						k+=1
					if k<numVar:
						h=Old[z+1][j][0:k] +'_' + Old[z+1][j][k+1:]
						New[z][len(New[z])-1].append(h)
	for i in range(len(Old)):
		for j in range(1,len(Old[i]),2):
			if Old[i][j] not in A:
				New.append([])
				New[len(New)-1].append(Old[i][j-1])
				New[len(New)-1].append(Old[i][j])
	if [] in New:
		New.remove([])
	return(New)

def PrimeImplicantTable(PIlist,minterms): #figuring out essential prime implicants
	P={}
	for i in minterms:
		P[int(i)]=0
	for i in PIlist:
		for j in PIlist[i]:
			if str(j) in minterms:
				P[j]+=1
	expr=''
	covered=[]
	for i in P:
		if P[i]==1:
			for j in PIlist:
				if i in PIlist[j] and i not in covered:
					expr=expr+j+'+'
					for k in PIlist[j]:
						if k not in covered:
							covered.append(k)
	
	for i in PIlist:
		w=0
		j=0
		for j in PIlist[i]:
			if j not in covered and str(j) in minterms:
				w+=1
		
		if w==len(PIlist[i]):
			expr=expr+ i +'+'
			for j in PIlist[i]:
				covered.append(j)
			

	for i in PIlist:
		for j in PIlist[i]:
			if j not in covered and str(j) in minterms:
				expr=expr+i+'+'
				for k in PIlist[i]:
					covered.append(k)
	
	expr=expr[0:len(expr)-1]
	return expr

def Kmap(m,x,numVar):
	n=len(m)
	p=len(x)
	if n+p == int(2**numVar):
		return 1
	b=[]
	if x=='-':
		All=m[0:n-1]
	else:
		All=m+x
	if '' in All:
		All.remove('')
	for i in All:
		b.append(DecimalToBinary(int(i),numVar))
	b=sorted(b)
	i=0
	B1=[[],[],[],[],[]]
	q=len(All)
	for i in range(q):
		j=b[i].count('1')
		B1[j].append(b[i])
	if [] in B1:		
		B1.remove([])
	l=len(B1)
	B2=[]
	for i in range(0,l-1):
		B2.append([])
	i=0
	j=0
	r=[]
	for q in range(16):
		r.append(0)
	l=len(B2)
	for z in range(0,l):
		for i in B1[z]:
			for j in B1[z+1]:
				c=0
				k=0
				for k in range(numVar):
					if j[k]!=i[k]:
						c+=1
				if c==1:
					B2[z].append([BinaryToDecimal(i),BinaryToDecimal(j)])
					r[int(BinaryToDecimal(i))]+=1
					r[int(BinaryToDecimal(j))]+=1
					k=0
					while j[k]==i[k] and k<numVar:
						k+=1
					if k<numVar:
						h=j[0:k] +'_' + j[k+1:]
						B2[z].append(h)
	q=0
	for q in range(16):
		if r[q]==0 and q in m:
			B2.append([DecimalToBinary(q,numVar)])
			B2.append([q])

	if [] in B2:
		B2.remove([])
	o=B2
	n=[]
	N=[]
	while cases(o,n,numVar)!=[]:
		N=cases(o,n,numVar)
		o=n
		n=N
	if [] in N:
		N.remove([])
	F=[]
	for i in N:
		for j in i:
				F.append(j)
	X=[]
	for i in F:
		if type(i[0])==list:
			for j in i:
				X.append(j)
		else:
			 X.append(i)

	Final={}
	for i in range(1,len(X),2):
		Final[Get_PrimeImplicant(X[i])]=X[i-1]
	
	E=PrimeImplicantTable(Final,m)
	return E


def minFunc(numVar, stringIn):
	minterms,dontcare=stringIn.split(' d ') #splitting the function for minterms and dont care's
	minterms=minterms[1:len(minterms)-1]
	dontcare=dontcare[1:len(dontcare)-1]
	minterms=minterms.split(',')
	dontcare=dontcare.split(',')
	if numVar==1:
		if '0' in minterms and '1' in minterms:
			print(1)

		elif '0' in minterms:
			print('a\'')
		else :
			print('a')
	else:
			t=Kmap(minterms,dontcare,numVar)
			print(t)
	