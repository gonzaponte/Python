#Funcions utiles e xerais

from constants import *
from numpy import *
from array import array
from math import *
import sys

LETRAS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letras=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

DIC,dic={},{}

print '\n'
print 'For checking the functions and variables defined in the module funs use printfuns()'
print '\n'

def printfuns():
    printconstants()
    print 'minus(palabra) returns a string'
    print 'maius(palabra) returns a string'
    print 'capit(palabra) returns a string'
    print 'getname(variable,exception=0) returns a string'
    print 'readdata(fname,n,sep=" ",type="float") returns n variables of type "type"'
    print 'statistics(data,sdata=0) returns 3 floats'
    print 'chi2(exp,sexp,teo,gdl) returns a float'
    print 'solve2(p2,p1,p0) returns 2 floats'
    print 'roots(fun,min,max) returns a float'
    print 'sign(x) returns an int'
    print 'recursive(fun,x0) returns a float'
    print 'deg2rad(deg) returns a float'
    print 'rad2deg(rad) returns a float'
    print 'lambda2E(l) returns a float'
    print 'E2lambda(E) returns a float'
    print 'data2sec(data) returns a float'
    print 'solidangle(r,d) returns a float'
    print 'gaussint(a,c,sa=0,sc=0) returns 2 floats'
    print 'makedic(keys,values) returns a dictionary'
    print 'makedoubledic(data1,data2) returns a dictionary'
    print 'inevertdic(keys,values) returns a dictionary'
    print 'doubledic(keys,values) returns a dictionary'
    print 'printdic(dic) returns nothing'
    print 'gammaL(v) returns a float'
    print 'E2p(E,m) returns a float'
    print 'T2p(T,m) returns a float'
    print 'T2E(T) returns a float'
    print 'numint(fun,min,max) returns a float'
    print 'bin2phase(c,i=0) returns 2 floats'
    print 'phase2bin(mod,phase) returns a complex'
    print 'csqrt(a) returns type of a'
    print 'nroot(a,n) returns type of a'
    print 'zeros(rows,cols=0) returns a list of zeros or a matrix with all zeros (floats)'
    print 'ones(rows,cols=0) returns a list of ones of a matrix with all ones (floats)'
    print 'identity(size) returns a identity matrix (floats)'
    print 'interpolate(x1,y1,x2,y2.x0) returns a float'
    print 'factorial(x) returns a float'
    print 'bessel(x,n) returns a float'
    print 'derivative(f,n,x) returns a float'
    print 'maxminfinder(fun,low,up,n=100000) returns 2 lists'
    print 'printmatrix(m) returns anything'
    print 'maxfinder(a,absolute=False,location=False) returns a number of the type of m and 2 ints'
    print 'randommatrix(rows,cols) returns a rows x cols matrix'
    print 'det3x3(m) returns a number of the type of m'
    print 'mxm(a,b) returns a matrix of size rows(a) x cols(b)'
    print 'pivoteoparcial(m,x,P=False) returns a matrix with the same size of m and another one if P is given'
    print 'gauss(m,n=False) returns a list of length size of m'
    print 'LUdecomp(m) returns 3 matrix with the same size as m'
    print 'LU(m,n=False) returns a list of length size of m'
    print 'inverseLU(m) not implemented yet'
    print 'inverse(m) returns a matrix of same size as m'
    print 'ordering(v,order=True) returns a list like v'
    print 'isin(valor,where) returns a boolean'

for i in range(len(LETRAS)):
	DIC[LETRAS[i]]=letras[i]
	dic[letras[i]]=LETRAS[i]

SUM  = lambda x,y: x + y
SUBS = lambda x,y: x - y
MULT = lambda x,y: x * y
DIV  = lambda x,y: x / y

minus = lambda word: reduce( SUM, map( lambda x: DIC[x], word ) )
def maius(palabra):
	for i in letras:
		palabra=palabra.replace(i,dic[i])
	return palabra

def capit(palabra):
	palabra=minus(palabra)
	palabra=palabra.replace(palabra[0],maius(palabra[0]),1)
	return palabra

def getname(variable,exception=0):
    for i in vars().keys():
        if i==exception:
            continue
        if vars()[i]==variable:
            varname = str( i )
    return varname

#def readdata(fname,sep=' ',type='float'):
#    f=open(fname,'r')
#    lines = f.readlines()
#    f.close()
#    
#    n = lines[0].count(sep)
#    vars=[[]]*(n+1)
#    
#    l=len(lines)
#    for line in lines:
#        index=0
#        n0=0
#        for i in range(1,len(line)):
#            if index<n:
#            	if (line[i]==sep):
#            		if type=='float':
#            			vars[index].append( float(line[n0:i]) )
#            		elif type=='int':
#            			vars[index].append( int(line[n0:i]) )
#            		n0=i+1
#            		index += 1
#        if type=='float':
#            vars[index].append( float( line[n0:]))
#        if type=='int':
#            vars[index].append( int( line[n0:] ) )
#    if not n:
#        return vars[0]
#    return vars

def readdata(fname,sep=' ',type='float'):
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    
    ndata = len ( lines[0].split(sep) )
    vars=[]
    for i in range(ndata):
        vars.append([])
    
    for line in lines:
        aux = line.split(sep)
        if type=='float':
            map( lambda i,x: vars[i].append(float(x)), range(len(aux)), aux )
        elif type=='int':
            map( lambda i,x: vars[i].append(int(x)), range(len(aux)), aux )

    if ndata==1:
        return vars[0]
    return vars

def statistics(data,sdata=0):
    l = len( data )
    if sdata==0:
       sdata=[]
       for i in range(l):
           sdata.append(1.)
    if len(sdata)!=l:
       sys.exit('Lists length mismatch')
    w=[]
    for s in sdata:
        if s==0.:
        	w.append(1.e100)
        else:
        	w.append(1./s**2)
    wtotal=sum(w)
    mean=0
    for i in range(l):
        mean += data[i]*w[i]
    mean = mean/wtotal
    
    s2=0
    for i in range(l):
        s2 += w[i]*(data[i]-mean)**2.
    s2=s2/( wtotal*(l-1) )
    s=sqrt(s2)
        
    return mean,s2,s

def chi2(exp,sexp,teo,gdl):
	chi2=0
	if (len(exp)!=len(sexp)) or (len(exp)!=len(teo)):
		sys.exit('Variable size mismatch')
	for i in range( len(exp) ):
		chi2 += ((exp[i]-teo[i])/float(sexp[i]))**2
	chi2=chi2/gdl
	return chi2

def solve2(p2,p1,p0):
    a=p1**2-4*p2*p0
    if sign(a)+1:
        return (-p1 + sqrt(p1**2-4*p2*p0))/(2*p2),(-p1 - sqrt(p1**2-4*p2*p0))/(2*p2)
    else:
            return (-p1 + (p1**2-4*p2*p0+0j)**0.5)/(2*p0),(-p1 - (p1**2-4*p2*p0+0j)**0.5)/(2*p0)

def roots(fun,min,max):
    divs=99999
    div=(max-min)/divs
    f0=fun(min)
    for i in range(divs+1):
        f=fun(min+i*div)
        if (sign(f)!= sign(f0)):
           return (min+(i+0.5)*div)
        f0=f
    print 'There were no roots in that interval'
    return float('Inf')
           
def sign(x):
    if x<0:
    	return -1
    else:
    	return +1

def recursive(fun,x0): #fun debe estar na forma x=f(x)
    dif=1
    while dif>0.001:
        if dif>1:
            print 'Error: The solution does not converge'
            return -1
        x=fun(x0)
        dif = abs(x-x0)
        x0=x
    return x

def deg2rad(deg):
    return deg*pi/180.

def rad2deg(rad):
    return rad*180./pi

def lambda2E(l):
    return 2*pi*197.3/l

def E2lambda(E):
    return 2*pi*197.3/E
    
def date2sec(date):
	if (date[1]<1)or(date[1]>31): print sys.exit('Incorrect date\n')
	if (date[1]<1)or(date[1]>12): print sys.exit('Incorrect date\n')
	date = date[0]+date[1]*30+date[2]*365.25
	today = 1+3*30+2013*365.25
	return (today - date)*24*3600

def solidangle(r,d):
    return (1. - 1./sqrt(1+float(r)**2/d**2))

def gaussint(a,c,sa=0,sc=0):
	i=a*c*sqrt(pi)
	si=i*sqrt( (sa/a)**2 + (sc/c)**2 )
	return i,si

def makedic(keys,values):
    if not ( len(keys)==len(values) ):
        sys.exit( 'Arguments must have the same length' )
    return dict( zip(keys, values) )

def makedoubledic(data1,data2):
    if not ( len(data1)==len(data2) ):
       sys.exit('Arguments must have the same length')
    
    return makedic(data1,data2).update( makedic(data2, data1) )

def invertdic( dic ):
    return makedic( dic.values(), dic.keys() )

def doubledic( dic ):
    return dic.update( invertdic( dic ) )

def printdic( dic ):
    a = dic.keys()
    a.sort()
    for i in range( len(dic) ):
        print a[i],dic[ a[i] ]

def gammaL(v): #Lorentz gamma
    if v<=1.:
    	return 1./sqrt(1-v**2)
    else:
    	return 1./sqrt(1-v**2/299792458.**2)

def E2p(E,m): # Energy to momenta
    return sqrt(E**2-m**2)

def T2p(T,m): # Kinetic energy to momenta
    return sqrt(T**2+2*T*m)

def T2E(T): #Temeperature to energy
    return Boltzmann*T

def numint(fun,min,max):
    p=0.001
    d=max-min
    error=1+p
    f,f2,counter=0,0,0
    while (error>p):
          counter += 1
          r=min+d*random.rand()
          feval=fun(r)
          f  += feval
          f2 += feval**2
          error = d*sqrt(abs(f2/counter**2-f**2/counter**3))
          if abs(error)<1e-12:
          	error=1
    return d*f/counter,error

def bin2phase(c,i=0):
	if not i:
		r=c.real
		i=c.imag
	else:
		r=c
	mod=sqrt(r**2+i**2)
	phase=atan(float(i)/r)
	return mod,phase

def phase2bin(mod,phase):
	return complex(mod*cos(phase),mod*sin(phase))

#def csqrt(a):
#	if a.imag==0:
#		if a>=0:
#			return sqrt(a)
#		else:
#			return complex(0,sqrt(-a))
#	else:
#		mod,phase=bin2phase(a)
#		smod=sqrt(mod)
#		sphase=phase/2.
#		return phase2bin(smod,sphase)

def csqrt(a):
	return a**(1/2.)

def nroot(a,n):
	return a**(1./n)
	
def zeros(rows,cols=False):
	z=[]
	if not cols:
		for i in range(rows):
			z.append(0.0)
	else:
		for i in range(rows):
			z.append(zeros(cols))
	return z
	
def ones(rows,cols=False):
	o=[]
	if not cols:
		for i in range(rows):
			o.append(1.0)
	else:
		for i in range(rows):
			o.append(ones(cols))
	return o
	
def identity(size):
	m=zeros(size,size)
	for i in range(size):
		m[i][i]=1.0
	return m

def interpolate(x1,y1,x2,y2,x0):
    try:
        m=atan( (y2-y1)/(x2-x1) )
    except:
        sys.exit( 'Wrong parameters: the function is not well defined in that point' )
    n = y1 - m*x1
    return m*x0+n

def factorial( x ):
    if ( not isinstance(x, int) ) or ( x<0 ):
        sys.exit( 'Error, n must be an positive integer' )
    if x:
        return x*factorial(x-1)
    else:
        return 1

def bessel(x,n):
    def funct(t):
        return cos(n*t-x*sin(t))
    J,sJ=numint(funct,0,numberpi)
    J/=numberpi
    sJ/=numberpi
    return J

def derivative(f,n,x):
    h=0.0001
    m=[[],[],[],[],[]]
    
    for i in range(5):
        for j in range(5):
            m[j].append((float(i-2.))**j)
    for i in range(5):
        if i==n:
            m[i].append(factorial(n))
        else:
            m[i].append(0.0)

    a=gauss(m)

    fn=0.0
    for i in range(5):
        fn+=a[i]*f(x+(i-2)*h)
    fn/=(h**n)

    return fn

def maxminfinder(fun,low,up,n=100000):
	interval  = up - low
	increment = float(interval)/n
	feval=[]
	for i in range(n):
		feval.append(fun(low+i*increment))
	maxs,mins=[],[]
	f0=feval[0]
	f1=feval[1]
	if f0:
		delta=f1/f0
	else:
		print 'Wrong interval: limit must not be a root of the equation'
		return 0
	
	if abs(delta)>=1:
		slope=1
	else:
		slope=-1
	
	if delta>=0:
		sign=1
	else:
		sign=-1
	
	for i in range(1,n-1):
		f0=feval[i]
		f1=feval[i+1]
		if f0:
			deltanew=f1/f0
			if abs(deltanew)>=1:
				newslope=1
			else:
				newslope=-1
			
			if deltanew>=0:
				newsign=1
			else:
				newsign=-1
			
			if newslope!=slope:
				if newslope>0:
					mins.append(low+(i+0.5)*increment)
				else:
					maxs.append(low+(i+0.5)*increment)
				slope=newslope
		else:
			if slope<0:
				mins.append(low+i*increment)
			else:
				maxs.append(low+i*increment)
			slope=-slope
	return maxs,mins				

def printmatrix(m):
	for line in m:
		print line

def maxfinder(m,absolute=False,location=False):
	rows=len(m)
	cols=len(m[0])
	if absolute:
		max=abs(m[0][0])
	else:
		max=m[0][0]
	maxrow,maxcol=0,0
	for i in range(rows):
		for j in range(cols):
			if absolute:
				if abs(m[i][j])>max:
					max=abs(m[i][j])
					maxrow=i
					maxcol=j
			else:
				if m[i][j]>max:
					max=m[i][j]
					maxrow=i
					maxcol=j
	if location:
		return max,i,j
	else:
		return max	

def randommatrix(rows,cols):
	m=zeros(rows,cols)
	for i in range(rows):
		for j in range(cols):
			m[i][j]=random.rand()
	return m

def det3x3(m):
    det=0
    det+=m[0][0]*m[1][1]*m[2][2]
    det+=m[0][1]*m[1][2]*m[2][0]
    det+=m[0][2]*m[1][0]*m[2][1]
    det-=m[0][2]*m[1][1]*m[2][0]
    det-=m[0][1]*m[1][0]*m[2][2]
    det-=m[0][0]*m[1][2]*m[2][1]
    return det

def mxm(a,b):
    f1=len(a)
    f2=len(b)
    condition=0
    if isinstance(a[0], float) or isinstance(a[0], int):
        condition=1
        for i in range(f1):
            a[i]=[a[i]]
    if isinstance(b[0], float) or isinstance(b[0], int):
        condition=1
        for i in range(f2):
            b[i]=[b[i]]
    c1=len(a[0])
    c2=len(b[0])
    
    if c1-f2:
        print 'matrix dimensions mismatch'
    
    M=zeros(f1,c2)
    for i in range(f1):
        for j in range(c2):
            for k in range(c1):
                M[i][j]+= a[i][k]*b[k][j]
    
    if condition:
        for i in range(len(M)):
            M[i]=M[i][0]
    return M

def pivoteoparcial(m,x,P=False):
    f=len(m)
    c=len(m[0])
    maxval=abs(m[x][x])
    maxpos=x
    for i in range(x+1,f):
        if abs(m[i][x])>maxval:
            maxval=abs(m[i][x])
            maxpos=i
    for i in range(c):
        aux=m[x][i]
        m[x][i]=m[maxpos][i]
        m[maxpos][i]=aux
    if P:
        for i in range(len(P)):
            aux=P[x][i]
            P[x][i]=P[maxpos][i]
            P[maxpos][i]=aux
    if P:
        return m,P
    else:
        return m

def gauss(m,n=False):
    f=len(m)
    if n:
        for i in range(f):
            m[i].append(n[i])
    c=len(m[0])
    
    for i in range(f):
        m=pivoteoparcial(m,i)
        for j in range(i+1,f):
            factor=m[j][i]/m[i][i]
            for k in range(i,c):
                m[j][k]-=factor*m[i][k]
    
    x=zeros(f)
    for i in range(f-1,-1,-1):
        x[i]=m[i][c-1]
        for j in range(c-1):
            if j==i: continue
            x[i]-=m[i][j]*x[j]
        x[i]/=m[i][i]
    
    return x

def LUdecomp(m):
    f=c=len(m)
    
    L=identity(f)
    P=identity(f)
    
    print '\n', 0, '\n'
    for j in range(f):
        print m[j]
    print '\n \n'
    for j in range(f):
        print P[j]
    print '\n \n'
    
    for i in range(f):
        
        m,P=pivoteoparcial(m,i,P)
        for j in range(i+1,f):
            factor=m[j][i]/m[i][i]
            for k in range(i,c):
                m[j][k]-=factor*m[i][k]
            L[j][i]=factor
        
        
        print '\n', i+1, '\n'
        for j in range(f):
            print m[j]
        print '\n \n'
        for j in range(f):
            print P[j]
        print '\n \n'
        for j in range(f):
            print L[j]
        print '\n \n'
    
    U=m

    return L,U,P


def LU(m,n=False):
    f=len(m)
    if not n:
        n=zeros(f)
        for i in range(f):
            m[i][f]=n[i]
            del m[i][f]
    c=f


    L,U,P=LUdecomp(m)
    
    print '\n', 'L', '\n'
    for j in range(f):
        print L[j]
    print '\n \n'
    print '\n', 'U', '\n'
    for j in range(f):
        print U[j]
    print '\n \n'
    
    U=m
    n=mxm(P,n)
    x=zeros(f)
    y=zeros(f)
    
    print '\n', 'LU', '\n'
    for j in range(f):
        print (mxm(L,U))[j]
    print '\n \n'
    
    
    print '\n', 'n', '\n'
    for j in range(f):
        print n[j]
    print '\n \n'
    
    for i in range(f):
        y[i]=n[i]
        for j in range(i):
            y[i]-=L[i][j]*y[j]
    
    print '\n', 'y', '\n'
    for j in range(f):
        print y[j]
    print '\n \n'
    
    for i in range(f-1,-1,-1):
        x[i]=y[i]
        for j in range(f-1,i,-1):
            x[i]-=U[i][j]*x[j]
        x[i]/=U[i][i]
    
    print '\n', 'x', '\n'
    for j in range(f):
        print x[j]
    print '\n \n'
    
    return x

def inverseLU(m):
    return 0

def inverse(m):
    
    f=c=len(m)
    
    for i in range(f):
        for j in range(c):
            if i==j:
                m[i].append(1.0)
            else:
                m[i].append(0.0)

    sol=range(f)
    
    def findmax(x):
        max=abs(m[x][x])
        row=x
        col=x
        for i in range(x,f):
            for j in range(x,c):
                if abs(m[i][j])>max:
                    max=abs(m[i][j])
                    row=i
                    col=j
        return row,col

    def interchangerows(a,b):
        for k in range(2*f):
            aux=m[a][k]
            m[a][k]=m[b][k]
            m[b][k]=aux

    def interchangecols(a,b):
        aux=sol[a]
        sol[a]=sol[b]
        sol[b]=aux
        for k in range(f):
            aux=m[k][a]
            m[k][a]=m[k][b]
            m[k][b]=aux

    for i in range(f):
        row,col=findmax(i)
        interchangerows(i,row)
        interchangecols(i,col)
        
        for j in range(i+1,f):
            factor=m[j][i]/m[i][i]
            for k in range(i,2*f):
                m[j][k]-=factor*m[i][k]    
    for i in range(f-1,-1,-1):
        
        factor=m[i][i]
        for j in range(i,2*f):
            m[i][j]/=factor
        
        for j in range(i):
            factor=m[j][i]
            for k in range(i,2*f):
                m[j][k]-=factor*m[i][k]

    M=zeros(f,f)

    for i in range(f):
        for k in range(f):
            M[sol[i]][k]=m[i][k+3]
    return M

def ordering(v,order=True):
    w=[]
    l=len(v)
    if order:
        for i in range(l):
            min=v[0]
            pos=0
            for j in range(len(v)):
                if v[j]<min:
                    min=v[j]
                    pos=j
            w.append(min)
            del v[pos]
    else:
        for i in range(l):
            max=v[0]
            pos=0
            for j in range(len(v)):
                if v[j]>max:
                    max=v[j]
                    pos=j
            w.append(max)
            del v[pos]
    return w

def isin(valor,lista): #Para buscar nun diccionario usar nome_dicionario.keys(). Para buscar nos valores usar nome_dicionario.values()
    for i in lista:
        if i==valor:
            return True
    return False













