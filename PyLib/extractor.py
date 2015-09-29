import os
import subprocess
import sys


REMOVEFOLDER = True


def selection(filename):
    answer = True
    if not 'Under' in filename: answer = False
    if '.m' in filename: answer = False
    if '.avi' in filename: answer = False
    return answer


thisdir = os.listdir('.') if len(sys.argv) is 1 else sys.argv[1:]
folders = filter( selection, thisdir )


filetypes = ['.mp4','.avi','.mkv']

for folder in folders:
    print folder
    folderfiles = os.listdir(folder)
    files = reduce( lambda x,y: x+y, [ filter( lambda x: filetype in x, folderfiles ) for filetype in filetypes ] )
    for file in files:
        print 'Moving file', folder + '/' + file
        subprocess.call(['mv', folder + '/' + file, '.'])
    if REMOVEFOLDER:
        print 'Removing folder ', folder
        subprocess.call(['rm','-rf',folder])


