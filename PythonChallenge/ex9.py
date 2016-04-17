import urllib
import urllib2

urlbase  = lambda x:'http://www.pythonchallenge.com/pc/def/{0}'.format(x)
folder = 'files/'

filecode = 'good.jpg'
download = urllib.urlretrieve(urlbase(filecode),folder+filecode)
print 'File ', filecode, 'downloaded and saved in', folder+filecode

website = 'http://www.pythonchallenge.com/pc/return/good.html'
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, website, 'huge', 'file')
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
req = urllib2.Request(website)
data = urllib2.urlopen(req).read()
first = map( int, map( str.rstrip, data.split('first:\n')[1].split('\n\nsecond:')[0].split(',') ) )
second = map( int, map( str.rstrip, data.split('second:\n')[1].split('\n\n-->')[0].split(',') ) )

get_pairs = lambda x: zip( x[::2], x[1::2] )
first = get_pairs(first)
second = get_pairs(second)

image = PIL.Image.open(folder+filecode)
print image.height, 'x', image.width

for i in range(image.height):
    string = ''
    for j in range(0,image.width,7):
        pix = image.getpixel((j,i))
        if pix[0] == pix[1] == pix[2]:
            string += chr(pix[0])
    # Avoid noise
    if len(string)>10:
        print string
        break
