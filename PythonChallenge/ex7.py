import urllib
import PIL.Image

urlbase = lambda x:'http://www.pythonchallenge.com/pc/def/{0}'.format(x)
folder = 'files/'

filecode = 'oxygen.png'
download = urllib.urlretrieve(urlbase(filecode),folder+filecode)
print 'File ', filecode, 'downloaded and saved in', folder+filecode

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

# Get list
number_list = map(int,string.split('[')[1].split(']')[0].split(', '))
char_list = map( chr, number_list )


print 'New URL:'
print urlbase(''.join(char_list)+'.html')
