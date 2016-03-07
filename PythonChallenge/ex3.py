import urllib

urlbase = lambda x:'http://www.pythonchallenge.com/pc/def/{0}.html'.format(x)

page = urllib.urlopen(urlbase('ocr')).fp
string = ''.join(page.readlines()[37:1257])
code = ''.join( filter( str.isalpha, string ) )

print 'New URL:'
print urlbase(code)
