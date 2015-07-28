from Array import Vector, Matrix
from copy import deepcopy
from Statistics import *
from ROOT import *
from math import *
from Plots import Graph
from numpy import linspace
from RandomNumbers import LCG

class Efficiency:
    def __init__( self, signal, background ):
        self.sig  = deepcopy( signal )
        self.bkg  = deepcopy( background )
        self.xmin = min( signal + background )
        self.xmax = max( signal + background )
        self.range = self.xmax - self.xmin
        self.nsig = len( self.sig ) * 1.0
        self.nbkg = len( self.bkg ) * 1.0
        self._f = (lambda c: (lambda x: x > c) ) if Median( signal ) > Median( background ) else (lambda c: ( lambda x: x < c) )
    
    def MakePlots( self, granularity = 1., varname = 'x' ):
        roc  = TGraph(); roc .SetLineWidth(2); roc .SetLineColor(kBlack)
        seff = TGraph(); seff.SetLineWidth(2); seff.SetLineColor(kGreen)
        beff = TGraph(); beff.SetLineWidth(2); beff.SetLineColor(kRed)
        sgf1 = TGraph(); sgf1.SetLineWidth(2); sgf1.SetLineColor(kMagenta)
        sgf2 = TGraph(); sgf2.SetLineWidth(2); sgf2.SetLineColor(kBlue)

        cuts = linspace( self.xmin, self.xmax, int( ceil( self.range / granularity ) ) )
        for i, cut in enumerate(cuts):
            f = self._f( cut )
            nsig = len( filter( f, self.sig ) )
            nbkg = len( filter( f, self.bkg ) )
            psig = nsig / self.nsig
            pbkg = nbkg / self.nbkg
            roc.SetPoint( i, psig, 1 - pbkg )
            seff.SetPoint( i, cut, psig )
            beff.SetPoint( i, cut, pbkg )
            sgf1.SetPoint( i, cut, nsig / ( nsig + nbkg )**0.5 if nsig else 0. )
            sgf2.SetPoint( i, cut, nsig /  nbkg**0.5 if nbkg else 0. )
        
        mgr  = TMultiGraph()
        seff.SetTitle('Signal efficiency')
        beff.SetTitle('Background efficiency')
        mgr.Add( seff )
        mgr.Add( beff )
        
        roc.GetXaxis().SetTitle('Signal efficiency')
        roc.GetYaxis().SetTitle('Background rejection')
        
        cvs  = TCanvas(); cvs.Divide(2,2)
        for i,g in enumerate([roc,mgr,sgf1,sgf2]):
            cvs.cd(i+1)
            g.Draw('AC')
        
        mgr.GetXaxis().SetTitle( varname )
        cvs.cd(2).BuildLegend()
        cvs.Update()

        self.graphics = [ cvs, roc, (mgr,seff,beff), sgf1, sgf2 ]
        return

class Dataset:
    '''
    '''
    def __init__( self, data, weights = None, iszipped = True, compute_statistics = True ):
        self.data     = deepcopy(data) if iszipped else deepcopy(zip(*data))
        self.vars     = zip(*self.data)
        self.ndata    = len(self.data)
        self.ndim     = len(self.vars)
        self.weights  = Vector( *deepcopy(weights)) if weights else None
        self.empty    = False if self.data and self.data[0] else True
        if not self.empty and compute_statistics:
            self.Analyze()
        
    def Analyze( self ):
        self.mean     = Vector( *map( Mean, self.vars, self.weights ) ) if self.weights else Vector( *map( Mean, self.vars ) )
        self.cvm      = CovarianceMatrix ( *self.vars, means = self.mean, weights = self.weights )
        self.corrm    = CorrelationMatrix( *self.vars, means = self.mean, weights = self.weights )
        self.RMSs     = Vector( *map( sqrt, self.cvm.Diag() ) )
        self._indices = None
        self._predictor = None
        self._eigenvalues  = None
        self._eigenvectors = None
        self._subspace = None

    def __iter__( self ):
        return iter( self.data )
    
    def Copy( self ):
        return Dataset( self.data, self.weights )
    
    def _ComputePredictor( self, indices ):
        remaining = [ i for i in range(self.ndim) if not i in indices ]
        new = self.cvm.Copy()
        
        current = 0
        for i in indices:
            new.Insert(current, new.Pop(i))
            new = new.T()
            new.Insert(current, new.Pop(i))
            current += 1

        cyy, cxy, cyx, cxx = new.Break( len(indices) )
        cxx = cxx.Inverse()
        xmean = self.mean[remaining]
        ymean = self.mean[indices]
        self._predictor = lambda x: ymean + cxy ** cxx ** ( x - xmean )
    
    def Predict( self, x, vars = (-1,) ):
        '''
            Get the best estimation of the variables with indices vars from the dataset.
        '''
        if vars != self._indices:
            self._indices = deepcopy(vars)
            self._ComputePredictor( vars )

        return self._predictor( Vector(*x) )
    
    def Eigenvalues( self ):
        '''
            Get eigenvalues.
        '''
        if not self._eigenvalues: self._ComputeEigenvalues()
        return self._eigenvalues
    
    def Eigenvectors( self ):
        '''
            Get eigenvectors.
        '''
        if not self._eigenvectors: self._ComputeEigenvalues()
        return self._eigenvectors
    
    def _ComputeEigenvalues( self ):
        '''
            Compute eigenvalues and eigenvectors.
        '''
        self._eigenvalues, self.eigenvectors = self.cvm.Diagonalize()

    def SortedEigenvalues( self ):
        '''
            Get the eigenvalues sorted with index.
        '''
        if not self._eigenvalues: self._ComputeEigenvalues()
        return sorted( zip( self._eigenvalues, range(self.ndim) ) )

    def SortedEigenvectors( self ):
        '''
            Get the eigenvalues sorted with index.
        '''
        indices = zip(*self.SortedEigenvalues())[1]
        return [ (self._eigenvectors[i],i) for i in indices ]

    def _ComputeProjector( self, indices ):
        subspace_projector = self.Eigenvectors().Pick( indices )
        self._projector = lambda x: subspace_projector ** Vector(*x)

    def ProjectInto( self, data, indices ):
        '''
            Project data into subspace given by indices.
        '''
        if self.subspace != indices:
            self._subspace = deepcopy(indices)
            self._ComputeProjector( indices )

        return self._projector( data )

    def SubDataset( self, indices ):
        '''
            Returns a new dataset with columns selected in indices.
        '''
        if isinstance(indices,int): indices = [indices]
        return Dataset( zip( *[ self.vars[i] for i in indices ] ), self.weights )

    def SplitVariables( self, indices ):
        '''
            Splits the Dataset into two with different variables
        '''
        secidni = range( ds.ndim )
        [ secidni.pop(k) for k in reversed(indices) ]
        return self.SubDataset( indices ), self.SubDataset( secidni )

    def SplitSample( self ):
        '''
            Randomly separate events from dataset.
        '''
        ### Not coded yet.
        pass

class kMeans:
    def __init__( self, DS ):
        self.DS = DS.Copy()
        self.random = LCG()

    def _Baricenter( self, x ):
        return Mean(x)

    def _Ndistance( self, u, v ):
        x = Vector(*u) - Vector(*v)
        return sqrt( x ** x )

    def _Clasify( self, x, points ):
        distances = [ self._Ndistance( x, point) for point in points ]
        return distances.index( min( distances ) )

    def _ComputeInitialGuess( self, Nclusters ):
        xmin = map( min, self.DS.vars )
        xmax = map( max, self.DS.vars )
        return Vector( *[ tuple( self.random.Uniform(minimum,maximum) for minimum,maximum in zip(xmin,xmax) ) for dim in range(Nclusters) ] )

    def FindClusters( self, Nclusters, guess = None, precision = 1e-3 ):
        baricenters = Vector(*guess) if guess else self._ComputeInitialGuess(Nclusters)
        difference = precision + 1
        while difference > precision:
            clusters = [ [] for c in range( Nclusters ) ]
            for data in self.DS:
                index = self._Clasify( data, baricenters )
                clusters[index].append( data )
            new_baricenters = [ Vector( *map(Mean,zip(*cluster) ) ) for cluster in clusters ]
            difference = sum( map( self._Ndistance, new_baricenters, baricenters ) )
            baricenters = new_baricenters
        clusters = map( Dataset, clusters )
        map( Dataset.Analyze, clusters )
        self.clusters = clusters
        self.baricenters = baricenters
        return clusters

    def Plot( self, datamarker = 20, datasize = 1., centermarker = 29, centersize = 2. ):
        assert self.DS.ndim <= 3,'Too many dimensions to be drawn!'
        if self.DS.ndim is 3: return self._Plot3D()

        h = Graph( self.DS.vars[0], self.DS.vars[1], 'x var', 'y var', '' )
        h.SetMarkerStyle( datamarker )
        h.SetMarkerSize( datasize )
        b = Graph( zip(*self.baricenters)[0], zip(*self.baricenters)[1], '', '', '' )
        b.SetMarkerStyle( centermarker )
        b.SetMarkerSize( centersize )
        b.SetMarkerColor(kRed)
        c = TCanvas()
        h.Draw('ap')
        b.Draw('psame')
        self._objects = [c,h,b]

class kNN:
    '''
        k-Nearest Neighboors classifier.
    '''
    def __init__( self, ds, targets, default_k = 5, normalize_data = True ):
        self.ds      = self._NormalizeDataset(ds) if normalize_data else deepcopy(ds)
        self.targets = deepcopy( targets )
        self.targset = list(set(self.targets))
        self.default_k = default_k
        self._normalize = normalize_data

    def _NormalizeDataset(self,ds):
        self.ds     = ds
        self.mins   = map( min, ds.vars )
        self.ranges = [ float( max(ds.vars[i]) - self.mins[i] ) for i in range(self.ds.ndim) ]
        return Dataset( map( self._NormalizeEvent, ds ), compute_statistics = False )
    
    def _NormalizeEvent( self, evt ):
        return tuple( (evt[i] - self.mins[i]) / self.ranges[i] for i in range(self.ds.ndim) )
    
    def _Ndistance( self, u, v ):
        return sqrt( sum( (i-j)**2 for i,j in zip(u,v) ) )

    def ClassifyEvent( self, evt, k = None ):
        if k is None: k = self.default_k
        if self._normalize: evt = self._NormalizeEvent( evt )
        check_distance  = lambda x: self._Ndistance( evt, x )
        distances       = map( check_distance, self.ds )
        closest_targets = zip( *sorted( zip( distances, self.targets ) ) )[1][:k]
        votes           = [ closest_targets.count(t) for t in self.targset ]
        nofvotes        = max(votes)
        return self.targset[votes.index(nofvotes)], nofvotes/float(k)

    def ClassifyEvents( self, evts, k = None ):
        return zip(*[ self.ClassifyEvent(evt,k) for evt in evts ])

    def Plot2D( self, evts = None, colors = [ kBlue, kRed, kViolet, kGreen, kYellow ] ):
        splitted = { t : [] for t in self.targset }
        for d,t in zip(self.ds.data,self.targets): splitted[t].append( d )
        graphs = []
        for i,t in enumerate(self.targset):
            x, y = zip( *splitted[t] )
            graphs.append( Graph( x, y, '', '', str(t) ) )
            graphs[-1].SetMarkerStyle( 21 + i )
            graphs[-1].SetMarkerColor( colors[i] )
        
        canvas = TCanvas()
        graphs[0].Draw('ap')
        for i in graphs[1:]: i.Draw('psame')

        if evts:
            if self._normalize: evts = map( self._NormalizeEvent, evts )
            x, y = zip(*evts)
            class_data = Graph( x, y )
            class_data.SetMarkerStyle(20)
            class_data.Draw('psame')
        else:
            class_data = None

        canvas.BuildLegend()
        self._objects = [ graphs, class_data, canvas ]


class Fisher:
    def __init__( self, signal, background ):
        self.sig = deepcopy( zip(*signal) )
        self.bkg = deepcopy( zip(*background) )
        self.Train()

    def Train( self, offset = 0., scale = 1. ):
        sig_means = Vector( *map( Mean, self.sig ) )
        bkg_means = Vector( *map( Mean, self.bkg ) )
        sig_covar = CovarianceMatrix( *self.sig, means = sig_means )
        bkg_covar = CovarianceMatrix( *self.bkg, means = sig_means )
        coefs = (sig_covar+bkg_covar).Inverse() ** ( sig_means - bkg_means )
        self.coefs = coefs
        self._fun = lambda x: offset + scale * self.coefs ** Vector( *x )

    def Apply( self, signal, background, nbins = 100 ):
        sig_values = map( self._fun, signal )
        bkg_values = map( self._fun, background )
        xmin  = min( sig_values + bkg_values ); xmin *= 0.99 if xmin>0 else 1.01
        xmax  = max( sig_values + bkg_values ); xmax *= 1.01 if xmax>0 else 0.99
        canvas = TCanvas()
        hsig   = TH1F('sig',';t-value;Entries', nbins, xmin, xmax )
        hbkg   = TH1F('bkg',';t-value;Entries', nbins, xmin, xmax )
        map( hsig.Fill, sig_values )
        map( hbkg.Fill, bkg_values )
        hsig.SetMaximum( max( hsig.GetMaximumStored(), hbkg.GetMaximumStored() ) )
        hsig.SetLineColor(kRed)
        hbkg.SetLineColor(kBlack)
        hsig.Draw()
        hbkg.Draw('same')
        canvas.BuildLegend()
        #### save stuff
        self._root_objs = [ canvas, hsig, hbkg ]
        self.sig_values = sig_values
        self.bkg_values = bkg_values

    def Plot( self ):
        self.effplots = Efficiency( self.sig_values, self.bkg_values )
        self.effplots.MakePlots(0.01)

class DecissionTree:
    def __init__( self, data, labels, properties = None ):
        self.data   = data
        self.labels = labels
        self.ndim   = len(data[0])
        self.prop   = properties if properties else map( str, range(self.ndim) )
        self._BuildTree()
    
    def _Train( self ):
        data   = self.data
        labels = self.labels
        self.cuts = []
        while len(set(labels)) != 1 and len(data[0]):
            f = self._choose_feature( data, labels )
            data, labels = self._split_by_feature( data, labels, f, )

    def _BuildTree( self ):
        self.tree = self._BuildBranch( self.data, self.labels )
    
    def _BuildBranch( self, data, labels ):
        feature = self._ChooseFeature( data, labels )
        tree = {}
        property = self.prop.pop(feature)
        for value in set( zip(*data)[feature] ):
            subdata, sublabels = self._SplitByFeature( data, labels, feature, value )
            key = (property,value)
            if len(set(sublabels)) is 1:
                tree[ key ] = sublabels[0]
            elif len(subdata[0]) is 1:
                tree[ key ] = sorted( (labels.count(subvalue),subvalue) for subvalue in set(sublabels) )[-1][1]
            else:
                tree[ key ] = self._BuildBranch( subdata, sublabels )
        return tree

    def _SplitByFeature( self, data, labels, feature, value ):
        pop = lambda x: x[:feature] + x[feature+1:]
        out = [ (pop(dt),lb) for dt, lb in zip(data,labels) if dt[feature] == value ]
        return zip( *out ) if out else ([], [])

    def _ChooseFeature( self, data, labels ):
        inv_n    = 1.0 / len(labels)
        entropy0 = ShannonEntropy(labels)
        
        zipped_data = zip(*data)
        gains  = []
        for feature in range( self.ndim ):
            entropy = 0.
            for split_value in set( zipped_data[feature] ):
                subds, sublb = self._SplitByFeature( data, labels, feature, split_value )
                p = len(sublb) * inv_n
                entropy += p * ShannonEntropy(sublb)
            gains.append( entropy0 - entropy )

        return gains.index( max(gains) )


if __name__ == '__main__':
    R = TRandom3(0)
    '''
    sig_train = [ ( R.Gaus(), R.Gaus(), R.Uniform(), R.Poisson(6) ) for i in xrange(int(1e3)) ]
    bkg_train = [ ( R.Uniform(-5,5), R.Uniform(-2,2), R.Uniform(-10,10), R.Poisson(12) ) for i in xrange(int(1e3)) ]
    sig_apply = [ ( R.Gaus(), R.Gaus(), R.Uniform(), R.Poisson(6) ) for i in xrange(int(1e3)) ]
    bkg_apply = [ ( R.Uniform(-5,5), R.Uniform(-2,2), R.Uniform(-10,10), R.Poisson(12) ) for i in xrange(int(1e3)) ]
    '''
    '''
    sig_train = [ ( R.Gaus(), R.Gaus(), R.Uniform() ) for i in xrange(int(1e3)) ]
    bkg_train = [ ( R.Uniform(-5,0), R.Uniform(0,5), R.Uniform(-10,10) ) for i in xrange(int(1e3)) ]
    sig_apply = [ ( R.Gaus(), R.Gaus(), R.Uniform() ) for i in xrange(int(1e3)) ]
    bkg_apply = [ ( R.Uniform(-5,0), R.Uniform(0,5), R.Uniform(-10,10) ) for i in xrange(int(1e3)) ]
    '''
    '''
    sig_train = [ ( R.Gaus(1.,1.), R.Gaus(1.,1.), R.Uniform(-1,1) ) for i in xrange(int(1e3)) ]
    bkg_train = [ ( R.Gaus(0,5), R.Gaus(0,5), R.Uniform() ) for i in xrange(int(1e3)) ]
    sig_apply = [ ( R.Gaus(1.,1.), R.Gaus(1.,1.), R.Uniform(-1,1) ) for i in xrange(int(1e3)) ]
    bkg_apply = [ ( R.Gaus(0,5), R.Gaus(0,5), R.Uniform() ) for i in xrange(int(1e3)) ]
    '''
    '''
    F = Fisher( sig_train, bkg_train )
    F.Apply( sig_apply, bkg_apply )
    F.Plot()
    '''
    
    N = 1000
    x = [ R.Gaus(1,.7) for i in range(N) ] + [ R.Gaus(-1,.7) for i in range(N) ] + [ R.Gaus(-1,.7) for i in range(N) ] + [ R.Gaus(+1,.7) for i in range(N) ]
    y = [ R.Gaus(1,.7) for i in range(N) ] + [ R.Gaus(-1,.7) for i in range(N) ] + [ R.Gaus(+1,.7) for i in range(N) ] + [ R.Gaus(-1,.7) for i in range(N) ]
    d = Dataset( zip(x,y) )
    k = kMeans( d )
    k.FindClusters(12)
    k.Plot()

    raw_input('done')