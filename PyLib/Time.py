from time import time as _time
from math import log10 as _log, floor as _floor

def BestUnits( dt, name = 'unknown' ):
    '''
        Returns a string with the time interval in the best posible units.
    '''
    if dt < 1:
        dt *= 1e3
        unit = 'us' if dt < 1 else 'ms'
        dt *= 1e3 if dt < 1 else 1
        return 'Ellapsed time in {2}: {0} {1}'.format(dt,unit,name)
    if dt < 60:
        return 'Ellapsed time in {1}: {0:.3f} s'.format(dt,name)
    if dt < 3600:
        mins = dt//60
        dt -= mins * 60
        return 'Ellapsed time in {2}: {0} min {1:d} s'.format(mins,dt,name)
    if dt < 86400:
        hours = dt // 3600
        dt -= hours * 3600
        mins = dt // 60
        dt -= mins * 60
        return 'Ellapsed time in {3}: {0} h {1} min {2:d} s'.format(hours,mins,dt,name)

    days = dt // 86400
    dt -= days * 86400
    hours = dt // 3600
    dt -= hours * 3600
    mins = dt // 60
    dt -= mins * 60
    return 'Ellapsed time in {4}: {0} days {1} h {2} min {3:d} s'.format(days,hours,mins,dt,name)


def ExecutionTime( function ):
    def TimedFunction( *args, **kargs ):
        t0 = _time()
        result = function( *args, **kargs )
        print BestUnits( _time() - t0 , function.__name__ )
        return result
    
    return TimedFunction