from ROOT import TH2I,TCanvas,gStyle
from copy import deepcopy
from time import sleep
from sys import argv

N = 50
M = 50

gStyle.SetOptStat('')
C  = TCanvas()
H  = TH2I('Gol','GoL',N,0,N,M,0,M); H.Draw('zcol')
A0 = [[0 for j in range(M+2)] for i in range(N+2)]
A  = deepcopy(A0)

def Beacon():
    A[2][2] = A[2][3] = A[3][2] = A[3][3] = 1
    A[4][4] = A[4][5] = A[5][4] = A[5][5] = 1

def Blinker():
    A[3][2] = A[3][3] = A[3][4] = 1

def Toad():
    A[3][3] = A[3][4] = A[3][5] = 1
    A[4][2] = A[4][3] = A[4][4] = 1

def Spaceships():
    A[5][2]  = A[6][2]  = 1
    A[5][1]  = A[6][1]  = 1
    A[5][11] = A[6][11] = A[7][11] = 1
    A[4][12] = A[8][12] = 1
    A[3][13] = A[9][13] = 1
    A[3][14] = A[9][14] = 1
    A[6][15] = 1
    A[4][16] = A[8][16] = 1
    A[5][17] = A[6][17] = A[7][17] = 1
    A[6][18] = 1
    A[3][21] = A[4][21] = A[5][21] = 1
    A[3][22] = A[4][22] = A[5][22] = 1
    A[2][23] = A[6][23] = 1
    A[1][25] = A[2][25] = A[6][25] = A[7][25] = 1
    A[3][35] = A[4][35] = 1
    A[3][36] = A[4][36] = 1

def NewStatus( i, j ):
    n  = A[i-1][j] + A[i+1][j] + A[i][j-1] + A[i][j+1]
    n += A[i-1][j-1] + A[i+1][j-1] + A[i+1][j+1] + A[i-1][j+1]
    
    if A[i][j]:
        return 1 if n is 2 or n is 3 else 0
    else:
        return 1 if n is 3 else 0

def BuildNext():
    global A
    B = deepcopy(A0)
    for i in range(1,N+1):
        for j in range(1,M+1):
            B[i][j] = NewStatus(i,j)
    A = deepcopy(B)

def Fill():
    for i in range(1,N+1):
        for j in range(1,M+1):
            H.SetBinContent(j,M+1-i,A[i][j])
    H.Draw('col')
    C.Update()

try:
    exec(argv[1].capitalize()+'()')
except:
    Blinker()

Fill()
while sum(map(sum,A)):
    BuildNext()
    Fill()
    sleep(0.05)

