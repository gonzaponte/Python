import urllib
import zipfile

urlbase = lambda x:'http://www.pythonchallenge.com/pc/def/{0}'.format(x)
folder = 'files/'

filecode = 'channel.zip'
download = urllib.urlretrieve(urlbase(filecode),folder+filecode)
print 'File ', filecode, 'downloaded and saved in', folder+filecode

zfile = zipfile.ZipFile(open(folder+filecode))

basemsg = 'Next nothing is'
read =  basemsg

comments = []
nothing = '90052'
while basemsg in read:
    comments.append(zfile.getinfo(nothing+'.txt').comment)
    read = zfile.read( nothing + '.txt' )
    nothing = read.split()[-1]
    print read

print ''
print ''.join(comments)

print 'New URL:'
print urlbase('oxygen.html')
