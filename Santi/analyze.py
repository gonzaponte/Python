from numpy import *
from datetime import date
import scipy
import scipy.special as spc
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib
import pylab
import subprocess
matplotlib.rc('text',usetex=1)
print 'Loaded\n'

def latexNumber(f,ferr=None,ferr2=None,exp=None):
    if exp == None:
        exp = floor(log10(abs(f)))
    man = f / (10**exp)
    if ferr == None:
        format = '%.2f'
        if exp==0:
            return (format%man)
        else:
            return r'' + (format%man) + r'\cdot 10^{' + ('%d'%int(exp)) + r'}'
        pass
    else:
        if ferr2==None:
            experr = floor(log10(abs(ferr)))
            manerr = ferr / (10**exp)
            format = '%.'+('%d'%int(1+exp-experr))+'f'
            if exp==0:
                return (format%man) + r'\pm' + (format%manerr)
            else:
                return r'\left(' + (format%man) + r'\pm' + (format%manerr) + r'\right)\cdot 10^{' + ('%d'%int(exp)) + r'}'
        else:
            experr = min(floor(log10(abs(ferr))),floor(log10(abs(ferr2))))
            manerr = ferr / (10**exp)
            manerr2= ferr2/ (10**exp)
            format = '%.'+('%d'%int(1+exp-experr))+'f'
            if exp==0:
                return (format%man) + r'^{+' + (format%manerr) + r'}_{-'+(format%manerr2)+r'}' 
            else:
                return r'\left(' + (format%man) + r'^{+' + (format%manerr) + r'}_{-'+(format%manerr2)+r'}\right)\cdot 10^{' + ('%d'%int(exp)) + r'}'  
def rate(N,t):
    n = N / t
    nE = sqrt(N) / t
    return n,nE
def attenuationFit(xrho,murho,r):
    return r*exp(-xrho*murho)


class attenuation:
    def __init__(self,dataFile,title):
        self.dataFile = dataFile
        self.title = title
        data = genfromtxt(fname=dataFile,comments='//',delimiter=';',names=['xrho','counts','t'])
        
        self.N = data['counts']
        self.t = data['t']
        self.nf,self.nfE = rate(self.N,self.t)
        self.xrho = data['xrho'][1:]
        self.a = self.nf[1:]/self.nf[0]
        self.aE = sqrt(pow(self.nfE[1:]/self.nf[0],2)+pow(self.nf[1:]*self.nfE[0]*pow(self.nf[0],-2),2))

        fit,fitVar = opt.curve_fit(attenuationFit,self.xrho,self.a,sigma=pow(self.aE,2))
        self.murho = fit[0]
        self.r = fit[1]
        self.murhoE = sqrt(fitVar[0][0])
        self.rE = sqrt(fitVar[1][1])
        self.aTh = attenuationFit(self.xrho,self.murho,self.r)

        self.fitRange = arange(min(self.xrho)*0.7,max(self.xrho)*1.2,(max(self.xrho)-min(self.xrho))/100)
        self.fitVals = attenuationFit(self.fitRange,self.murho,self.r)

        self.chiSquare = sum(pow(self.a-self.aTh,2)*pow(self.aE,-2))
        self.qChi = self.chiSquare / (len(self.a) - 2)
gatt = attenuation('datos',r'Atenuaci\'on de Bi-207 en Pb')
print 'Calculated'
    
graphFile = "grafica.pdf"
xmin = min(gatt.xrho) * 0.7
xmax = max(gatt.xrho) * 1.2
plt.figure( figsize=(6,4) )
plt.errorbar(gatt.xrho,gatt.a,yerr=gatt.aE,fmt='ro',markersize=0.5,label='Datos')
plt.plot(gatt.fitRange,gatt.fitVals,label='Ajuste')
plt.legend(loc=1)
plt.xlim([xmin,xmax])
plt.ylim([min(gatt.a)*0.6,max(gatt.a)*1.1])
plt.xlabel(r'$x_m (g/cm^2)$')
plt.ylabel(r'$a$')
plt.title(gatt.title)
plt.text(xmin+(xmax-xmin)*0.1,min(gatt.a)*0.7,r'~\\$\mu_m='+latexNumber(gatt.murho,gatt.murhoE)+r' cm^2/g$\\$r='+
         latexNumber(gatt.r,gatt.rE)+r'$\\$q_{\chi^2}='+latexNumber(gatt.qChi)+r'$')
plt.yscale('linear')
pylab.savefig(graphFile,bbox_inches=0)
print 'Printed'

latexOutput = r'''
\documentclass[10pt]{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\begin{document}

En el siguiente ejemplo vemos el ajuste de la atenuaci\'on gamma frente al espesor m\'asico del plomo atenuante. \\
\includegraphics[width=\textwidth]{''' + graphFile + r'''}

Las medidas fueron las siguientes \\
\begin{centering}
\begin{tabular}{|c|c|c|c|c|}
\hline
$x_{m} (g/cm^2)$ & N & t (s) & n & a \\ '''

for i in range(len(gatt.xrho)):
    latexOutput += r'\hline $'+latexNumber(gatt.xrho[i])+r'$ & $'+latexNumber(gatt.N[i])+r'$ & $'+latexNumber(gatt.t[i])+r'$ & $'
    latexOutput += latexNumber(gatt.nf[i],gatt.nfE[i])+r'$ & $'+latexNumber(gatt.a[i],gatt.aE[i])+r'$\\'

latexOutput += r'''
\hline
\end{tabular}
\end{centering}
\end{document}
'''
output = open('geiger.tex', 'w')
output.write(latexOutput)
output.close()
subprocess.call(['pdflatex','geiger.tex'])
print 'Saved'
