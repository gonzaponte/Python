from Array import Vector, Matrix
from copy import deepcopy as _deepcopy

class DataSet:
    '''
    '''
    def __init__( self, data, zipped = False ):
        self.data  = Matrix(*data) if zipped else Matrix(*zip(*data))
        self.vars  = self.data.T()
        shape      = self.data.Size()
        self.N     = shape[0] # number of points
        self.D     = shape[1] # number of dimensions
        self.means = Vector( *map(Mean, self.vars ) )
        self.C     = CovarianceMatrix(  *self.vars, means = list(self.means) )
        self.R     = CorrelationMatrix( *self.vars, means = list(self.means) )
        self.RMSs  = Vector( *[ s2**0.5 for s2 in self.C.Diag() ] )
    
    def GetPredictor( self, indices ):
        if not isinstance( indices, (list,tuple,Vector) ):
            indices = [ indices ]
        new = self.C.Copy()
        current = 0
        for i in indices:
            new.Insert(current, new.Pop(i))
            new = new.T()
            new.Insert(current, new.Pop(i))
            current += 1
        Cyy, Cxy, CxyT, Cxx = new.Break(len(indices))
        Cxx = Cxx.Inverse()
        xmean = Vector( *[ self.means[i] for i in range(self.D) if not i in indices ] )
        ymean = Vector( *[ self.means[i] for i in indices ] )
        return lambda x: ymean + Cxy ** Cxx ** ( Vector(*x) - xmean )

#
#class Dataset:
#    '''
#        Generic class for data storage.
#    '''
#    def __init__( self, name = 'DataSet', **kwargs ):
#        '''
#            Initialize with a name (default is DataSet) and any number of variables.
#            Target variable must be named target. Example:
#            Dataset( 'Prediction', temperature = [ 12, 13, 13, 12, 11 ],
#                                   litresperm2 = [0.1, 1.1, 1.2, 4.3, 4.4 ],
#                                   target = ['sunny','normal','normal','rains','rains'] )
#        '''
#        self.name     = name
#        self.features = sorted(kwargs)
#        self.dataT    = Matrix( [_deepcopy(kwargs[key]) for key in self.features ] )
#        self.data     = self.dataT.T()
#
#    def __getitem__( self, key ):
#        '''
#            Get feature.
#        '''
#        if not key in self.values:
#            raise KeyError('Key {0} not found in data set {1}'.format( key, self.name ) )
#        return self.values[key]
#
#    def __iter__( self ):
#        '''
#            Get event.
#        '''
#        for vector in self.data:
#            yield list(vector)
#        raise StopIteration()
#
#
#class Classifier:
#    def __init__( self, name, axes ):
#        self.name = name
#        self.labels = axes
#
#class kNN(Classifier):
#    
#    def __init__( self, dataset, k = 5 ):
#        self.data = dataset
#    
#    def __call__( self, test ):
#        ds = [ distance( test, data ) for data in self.data ]
#        d = zip( )
#
