from __future__ import division
from ROOT import TRandom3, TH1I, TH1F, TCanvas, gStyle
from math import log, exp

gStyle.SetOptStat('')
R = TRandom3(0)
dt = 1e-9
nHe = 1e3
nBe = 0
nC  = 0

t12 = 53.12 * 24 * 3600
lamb = log(2)/t12


c = TCanvas()
c.Divide(2)

c1 = c.cd(1)
c1.SetLogy()
abundances = TH1I('abundances','abundances',3,0,3)
abundances.GetXaxis().SetBinLabel(1,'He')
abundances.GetXaxis().SetBinLabel(2,'Be')
abundances.GetXaxis().SetBinLabel(3,'C')
abundances.SetMinimum(.1)

c2 = c.cd(2)
c2.SetLogy()
probabilities = TH1F('probabilities','probabilities',3,0,3)
probabilities.GetXaxis().SetBinLabel(1,'Be production')
probabilities.GetXaxis().SetBinLabel(2,'Be decay')
probabilities.GetXaxis().SetBinLabel(3,'C production')
probabilities.SetMinimum(1e-30)

i = 0
while nHe:
    PBeprod = 1e4 * nHe * dt
    PBedecay = 1 - exp( - nBe * lamb * dt )
    PCprod  = 1e4 * nBe * dt
#    print PBeprod
#    print PBedecay
#    print PCprod
#    raw_input()

    if nHe > 1 and R.Uniform() < PBeprod:
        nBe += 1
        nHe -= 2
    if nBe and R.Uniform() < PBedecay:
        nBe -= 1
        nHe += 2
    if nBe and nHe and R.Uniform() < PCprod:
        nBe -= 1
        nHe -= 1
        nC  += 1

    if not i % 10:
        c.cd(1)
        abundances.SetBinContent(1,nHe)
        abundances.SetBinContent(2,nBe)
        abundances.SetBinContent(3,nC)
        abundances.Draw()
        
        c.cd(2)
        probabilities.SetBinContent(1,PBeprod)
        probabilities.SetBinContent(2,PBedecay)
        probabilities.SetBinContent(3,PCprod)
        probabilities.Draw()
        c.Update()
