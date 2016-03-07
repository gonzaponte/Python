from prime import prime
from ROOT import *

digits = range(10)
strdigits = map( str, digits )

prime = prime.replace('\n','').replace('.','')
print 'CHECK:',all(map(str.isdigit,prime))

hdigit = TH1I('digit',';;# of ocurrences',10,0,10)
hlargest = TH1I('largest','Largest # consecutive digit;;Max',10,0,10)
hconsecutive = TH1I('consecutive','# consecutive digits;#Consecutives;',10,0,10)
hdigits = TH1I('digits',';;# of ocurrences',10,0,10)
[ hdigit.GetXaxis().SetBinLabel(d+1,str(d)) for d in digits ]
[ hlargest.GetXaxis().SetBinLabel(d+1,str(d)) for d in digits ]



last    = None
counter = 0
maxs    = [ 0 for d in digits ]
for d in prime:
    dint = int(d)
    hdigit.Fill( dint )
    if dint != last:
        hconsecutive.Fill( counter )
        maxs[dint] = max( counter, maxs[dint] )
        counter = 0
        last = dint

    counter += 1

for i,m in enumerate(maxs): hlargest.SetBinContent(i+1,m)
for d in digits: hdigits.SetBinContent(d+1,prime.count(''.join(strdigits[:d+1])))


for h in (hdigit,hlargest,hconsecutive):
    h.SetLineWidth(2)

c = TCanvas()
c.Divide(2,2)
c.cd(1);hdigit.Draw()
c.cd(2);hlargest.Draw()
c.cd(3);hconsecutive.Draw()
c.cd(4);hdigits.Draw()

raw_input()
