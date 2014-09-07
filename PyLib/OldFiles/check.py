import sys

def wrong( fun ):
    ''' This function throughs an error for wrong parameters.'''
    
    sys.exit('Error in ' + fun.__name__ + ': wrong parameters.' )

def isint(x):
    ''' This function checks if the argument is an integer. It returns a boolean'''
    
    return isinstance(x,int)

def islong(x):
    ''' This function checks if the argument is a long integer. It returns a boolean'''
    
    return isinstance(x,long)

def isfloat(x):
    ''' This function checks if the argument is a float. It returns a boolean'''
    
    return isinstance(x,float)

def isreal(x):
    ''' This function checks if the argument is a real number. It returns a boolean'''
    
    return isinstance( x, (int,float,long) )

def iscomplex(x):
    ''' This function checks if the argument is a complex number. It returns a boolean'''
    
    return isinstance(x,complex)

def isnumber(x):
    ''' This function checks if the argument is a number. It returns a boolean.'''
    
    return isinstance( x, (int,float,long,complex) )

def isstring(x):
    ''' This function checks if the argument is a string. It returns a boolean'''
    
    return isinstance(x,(str,unicode))

def islist(x):
    ''' This function checks if the argument is a list. It returns a boolean'''
    
    return isinstance(x,list)

def istuple(x):
    ''' This function checks if the argument is a tuple. It returns a boolean'''
    
    return isinstance(x,tuple)

def isdic(x):
    ''' This function checks if the argument is a dictionary. It returns a boolean'''
    
    return isinstance(x,dict)

def isset(x):
    ''' This function checks if the argument is a set. It returns a boolean'''
    
    return isinstance(x,set)

def isfrozen(x):
    ''' This function checks if the argument is a frozen set. It returns a boolean'''
    
    return isinstance(x,frozenset)

def iscontainer(x):
    ''' This function checks if the argument is a container. It returns a boolean'''
    
    return isinstance( x, (list,tuple,dict,set,frozenset) )

def isbool(x):
    ''' This function checks if the argument is a boolean. It returns a boolean'''
    
    return isinstance(x,bool)

def HaveSameLength( *l ):
    ''' This function checks whether the arguments have the same size.'''
    
    try:
        l0=len(l[0])
    except:
        l0=0
    
    for i in l:
        if not iscontainer(i):
            wrong(HaveSameLength)
        if not len(i)==l0:
            return False
    return True
