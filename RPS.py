from __future__ import division
from ROOT import *

RPS = {  1  : 'R',
         2  : 'P',
         3  : 'S',
        'R' :  1 ,
        'P' :  2 ,
        'S' :  3 }

class player:
    def __init__( self, seed = 0 ):
        self.Rwins  = 0
        self.Pwins  = 0
        self.Swins  = 0
        self.Rlost  = 0
        self.Plost  = 0
        self.Slost  = 0
        self.Prob   = { 'R' : 1/3,
                        'P' : 2/3,
                        'S' : 3/3}
        self.total  = 0
        self.Random = TRandom3(seed)

    def Choice( self ):
        if self.maxwins()/self.minwins()>3:
            return self.maxwins()
