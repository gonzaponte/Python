#
# Module with input/output -related functions
#
#
# Author: Gonzalo Martinez
#
# Last update: 21 / 04 / 2015
#


def LoadFile( filename, separator = ' ', skip = 0, type = float, comments = '#', zipped = False ):
    '''
        Import data from file named >filename<. Data must be separated always with >separator<. They will be converted to the type indicated in >type<. Rows of the file may be skipped by using >skip<. Lines beggining with >comments< will be automatically skipped. The >zipped< parameter is used to selected the output format. By default the columns are returned. For the return to be in row-format set >zipped< to True.
    '''
    data = []
    n = len(comments)
    with open( filename, 'r' ) as f:
        for i, line in enumerate(f):
            if i<skip or line[:n] == comments:
                continue
            row = line.split( separator )
            try: data.append( map( type, row ) )
            except: raise RuntimeError('Error reading line {0}:\n{1}'.format(i,line) )
    if len( data ) is 1:
        return data[0]
    if len(data[0]) is 1:
        return reduce( list.extend, data )
    return data if zipped else zip(*data)

def DumpToFile( data, filename, separator = ' ', header = '' ):
    '''
        Dump list or array in >data< to file using >separator< to separate data. A header labeling columns (for instance) may be used.
    '''
    if not isinstance( data[0], (list,tuple) ):
        data = [data]
    with open( filename, 'w' ) as f:
        if header:
            f.write( header + '\n' )
        f.write( '\n'.join( separator.join( map( str, dat ) ) for dat in data ) )

    return


if __name__ == '__main__':
    DumpToFile( range(10), 'proba.txt', ' ', '##ola k ase' )
    for i in LoadFile('proba.txt'): print i
