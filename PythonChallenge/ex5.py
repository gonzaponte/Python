import urllib

urlbase    = lambda x:'http://www.pythonchallenge.com/pc/def/{0}'.format(x)
urlbasephp = lambda x:'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={0}'.format(x)

def findnextnothing(nothing):
    page = urllib.urlopen(urlbasephp(nothing)).fp
    line = ''.join(page.readlines())
    nothing = line.split()[-1]
    return nothing, line

basemsg = 'and the next nothing is'
read =  basemsg

nothing = 12345
while basemsg in read:
    nothing, read = findnextnothing(nothing)
    print read

read = basemsg
nothing = 16044/2
while basemsg in read:
    nothing, read = findnextnothing(nothing)
    print read

code = read
print 'New URL:'
print urlbase(code)
