import os
import subprocess

def Code(filename):
    return filename.split('.')[3]

def Extension(filename):
    return filename.split('.')[-1]

def Transform(filename):
    code = Code(filename)
    ext  = Extension(filename)
    return code[2] + 'x' + code[-2:] + '.' + ext

def selection(filename):
    answer = False
#    types = ['.avi','.mp4','.mkv']
#    for type in types:
#        if type in filename:
#            answer = True
    if 'Under' in filename:
        answer = True
    return answer

thisdir  = os.listdir('.')
oldnames = filter(selection,thisdir)
newnames = map( Transform, oldnames )

for old,new in zip(oldnames,newnames):
    print 'renaming',old,'to',new
    subprocess.call(['mv',old,new])
