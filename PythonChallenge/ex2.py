urlbase = lambda x:'http://www.pythonchallenge.com/pc/def/{0}.html'.format(x)

letters  = [
'a','b','c','d','e','f','g','h','i','j','k','l','m',
'n','o','p','q','r','s','t','u','v','w','x','y','z']

lettermap = dict( zip(letters,letters[2:]+letters[:2]) )

inputstr = '''g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'''

print ''.join( [ lettermap.get(l,l) for l in inputstr] )
print ''
print 'New URL:'
print urlbase( ''.join(map( lettermap.get, 'map' ) ) )
