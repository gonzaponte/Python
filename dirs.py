from os import *

path = getcwd() + '/'

files = listdir(path)

avis = filter( lambda x: x[-4:] == '.avi', files )
#srts = filter( lambda x: x[-4:] == '.srt', files )
#
for i in range(13):
    j = i + 1
    avi = avis[i].replace('The Sopranos S05E','5x')
#    avi = avi.replace(' -','')
#    srt = srts[i].replace('The Sopranos - S05E','5x')
#    srt = srt.replace(' -','')
#    AVI = ''
#    SRT = ''
#    for j in range(len(avi)):
#        if j==5:
#            AVI += avi[j]
##            SRT += srt[j]
#            continue
#        AVI += avi[j].lower()
#        SRT += srt[j].lower()
    rename( avis[i], avi )
#    rename( srts[i], SRT )
#
#mp4s = filter( lambda x: x[-4:] == '.mp4', files )
#for i in range(21):
#    j = i+1
#    mp4 = mp4s[i].replace('[720pMkv.Com]_The.Sopranos.S06E','6x')
#    mp4 = mp4.replace('.Members.Only.480p.BluRay.x264-GAnGSteR','')
#
#    rename( mp4s[i], mp4 )
