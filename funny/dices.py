from ROOT import TRandom3,TH1I

random = TRandom3()
random.SetSeed(10)
r = lambda: 0.5 + 6*random.Uniform()
N= 1000000
h = TH1I('a','a',7,0,7)
roll = lambda n: map( lambda x: int(round(r())), range(n) )

is6in4 = 0
is66in24 = 0
for i in range(N):
    four = roll(4)
    dice1 = roll(24)
    dice2 = roll(24)
    if 6 in four:
        is6in4 += 1
    for d1,d2 in zip(dice1,dice2):
        if d1==d2 and d1==6:
            is66in24 += 1
            break

print 'Probabilidade de obter un 6 en 4 tiradas: ',is6in4,'/',N,' = ',float(is6in4)/N
print 'Probabilidade de obter dous 6s en 24 tiradas: ',is66in24,'/',N,' = ',float(is66in24)/N

