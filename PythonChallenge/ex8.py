import urllib
import urllib2
import bz2

urlbase  = lambda x:'http://www.pythonchallenge.com/pc/def/{0}'.format(x)
folder = 'files/'

filecode = 'integrity.jpg'
download = urllib.urlretrieve(urlbase(filecode),folder+filecode)
print 'File ', filecode, 'downloaded and saved in', folder+filecode

website = urllib.urlopen(urlbase(filecode[:-4]+'.html'))
webcode = website.readlines()

user = filter( lambda x: 'un' == x[:2], webcode )[0].split("'")[1]
pswd = filter( lambda x: 'pw' == x[:2], webcode )[0].split("'")[1]

username = bz2.decompress(user.decode('string_escape'))
password = bz2.decompress(pswd.decode('string_escape'))
print 'Username:', username
print 'Password:', password

print 'New URL (with user and password):'
print 'http://www.pythonchallenge.com/pc/return/good.html'



url2 = 'http://www.pythonchallenge.com/pc/return/good.html'
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url2, username, password)
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
req = urllib2.Request(url2)
f = urllib2.urlopen(req)
data = f.read()
print(data)
