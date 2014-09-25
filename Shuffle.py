import os
import sys
import random

try:
    sys.argv[1]
    verbose = True
except:
    verbose = False

R = random.Random() # Random generator
cwd = os.getcwd() + '/' # Current directory
allfiles = os.listdir( cwd ) # List of files in this directory
files = list() # The files I really want to shuffle

if verbose:
    print 'all files ='
    for file in allfiles:
        print file

# Save files that are not directories, hidden files or this file
for file in allfiles:
    if not os.path.isdir( cwd + file ) and not file[0] == '.' and not file == 'Shuffle.py':
        files.append( file )

if verbose:
    print 'to be changed files ='
    for file in files:
        print file

indices = range(len(files)) # List of new indices to pick (will be randomized)

# Remove previos numbering
for file in files:
    newindex = R.choice(indices)
    command = '''mv {0} {1}'''.format( cwd + file, cwd + '''{:0>3d}'''.format(newindex) + file[3:] )
    print '{0} -> {1}'.format( file, '{:0>3d}'.format(newindex) + file[3:] )
    os.system( command )
    indices.pop(indices.index(newindex))

