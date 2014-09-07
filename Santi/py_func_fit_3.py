from ROOT import TF1, TH1F, TCanvas, gRandom, TMath, gStyle, TFile

#Gaussian with linear background
class mygauss:
  def __call__( self, x, par ):
    norm = 1. / TMath.Sqrt(2.*TMath.Pi()) / par[2]**2 
    exp  = TMath.Exp( -(x[0]-par[3])**2 /  par[2]**2 / 2. )
    return  par[0] + x[0]*par[1] + par[4]*norm*exp

#Linear background
class Linear:
  def __call__( self, x, par ):
    return par[0] + x[0]*par[1]

gStyle.SetOptFit(1111)
gStyle.SetOptStat("e")

# create a linear function for fitting
fuli = TF1('fuli',Linear(),-4.,4.,2)

# create and fill a histogram
h1 = TH1F('h1','test',100,-4.,4.)
f1 = TF1('f1','6.+x*0.5',-4.,4.)

niter = 25000
h1.FillRandom('f1',niter)

h2 = h1.Clone('h1')
h2.SetName('Another histo')

for i in xrange(niter):
  px = gRandom.Gaus()
  h2.Fill(px)

mc = TCanvas()
mc.Divide(1,2)
mc.cd(1)
h1.Fit(fuli)
h1.Draw("E")

mc.cd(2)

myga = TF1("myga",mygauss(),-4., 4., 5)

#Set initial values for the fit parameters
myga.SetParameters(1.,1.,1.,0.,1.)

#Do the fit
h2.Fit(myga)
h2.Draw("E")

mc.Print("example.pdf")

# print results
parL = fuli.GetParameters()
print '\nLinear fit results: const =',parL[0],',pitch =',parL[1]

parLG = myga.GetParameters()
print '\nGauss plus Linear fit results\n'
for ii in range(0,5): print 'parameter ', ii,': ', parLG[ii]

# Save histograms
histofile = TFile("histos.root","recreate")
h1.Write()
h2.Write()
histofile.Close()

