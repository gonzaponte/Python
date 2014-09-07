from ROOT import *


c = TCanvas()


p1 = TPad( 'xy', 'xy', 0.00,    0., 0.75, 1.00  )
p2 = TPad( 'xy', 'xy', 0.75, 2./3., 1.00, 1.00  )
p3 = TPad( 'xy', 'xy', 0.75, 1./3., 1.00, 2./3. )
p4 = TPad( 'xy', 'xy', 0.75,    0., 1.00, 1./3. )

p1.SetFillColor(9)
p2.SetFillColor(2)
p3.SetFillColor(3)
p4.SetFillColor(6)

p1.Draw()
p2.Draw()
p3.Draw()
p4.Draw()

h1 = TH1F()
h2 = TH2F()
h3 = TH3F()
h4 = TH3F()

p1.cd()
h1.Draw()
p2.cd()
h2.Draw()
p3.cd()
h3.Draw()
p4.cd()
h4.Draw()
