#
# Module with the paralleling class.
#
#
# Author: Gonzalo Martinez
#
# Last update: 20 / 03 / 2014
#

import pp
from copy import copy

class Parallel:
    ''' Manager of parallel processing.'''

    def __init__( self, ncpus = 'autodetect'):
        ''' Constructor. Sets the number of cpus used. By default, it uses all the cpus available.'''
        
        self.ncpus   = ncpus
        self.server  = pp.Server( self.ncpus )
        self.jobs    = {}
        self.counter = 0

    def Send( self, function, args = (), otherfunctions = (), modules = (), callback = None, callbackargs = (), group = 'default', globals = None ):
        ''' Sends a job. If you send a jobs when all the cpus are busy, it will be waiting until a processor is free. It returns the job's key.'''
        
        if not isinstance( args, tuple ):
            args = args,
    
        if not isinstance( otherfunctions, tuple ):
            otherfunctions = otherfunctions,
        
        if not isinstance( modules, tuple ):
            modules = modules,

        self.jobs[ self.counter ] = self.server.submit( function, args, otherfunctions, modules, callback, callbackargs, group, globals )
        self.counter += 1
        
        return self.counter - 1

    def Get( self, key ):
        ''' Gets the result of a job.'''
                
        return self.jobs.pop( key )()


    def Wait( self, group = None ):
        ''' Waits for all the results in a group to finish. If group is None, waits for all the results.'''

        self.server.wait( group)
