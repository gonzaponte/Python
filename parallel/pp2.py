import pp,time

def reach(N):
    i=0
    while i<N:
        i += 1
    return i

print 'Sen paralelizar:'

t0 = time.time()
n = 1e8
job1 = reach(n)
print 'check1'
job2 = reach(n)
print job1,job2
t1 = time.time()
print 'job time: ', t1-t0

print 'Paralelizando:'
t0 = time.time()
jobs = pp.Server()
job1 = jobs.submit(reach,(n,))
print 'check2'
job2 = jobs.submit(reach,(n,))
print job1()
print 'a'
print job2()
t1 = time.time()
print 'job time: ', t1-t0
