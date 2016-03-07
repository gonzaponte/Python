import urllib

urlbase    = lambda x:'http://www.pythonchallenge.com/pc/def/{0}.html'.format(x)
urlbasephp = lambda x:'http://www.pythonchallenge.com/pc/def/{0}.php'.format(x)

def findguys(i):
    lowers = all( map( str.islower, [string[i-4],string[i], string[i+4]] ) )
    uppers = all( map( str.isupper, string[i-3:i]+string[i+1:i+4] ) )
    return lowers and uppers

page = urllib.urlopen(urlbase('equality')).fp
string = ''.join(page.readlines()[21:1272])
code = ''.join( map( string.__getitem__,filter( findguys, range(4,len(string)-4) ) ) )

print 'New URL:'
print urlbase(code)
print 'Well, it actually is...'
print urlbasephp(code)
