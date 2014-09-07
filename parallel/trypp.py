import pp, time

def factorial(N):
    if N:
        return N*factorial(N-1)
    return 1

t0 = time.clock()
jobs = pp.Server()
print 'Traballando con ', jobs.get_ncpus(),' cpus'

job1 = jobs.submit(factorial,(10,) )

print '10! = ',job1()
print 'time = ', time.clock() - t0

t0 = time.clock()
print '10! = ',factorial(10)
print 'time = ', time.clock() - t0


