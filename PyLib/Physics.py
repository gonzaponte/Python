'''
    Module with some useful physical data. Math constants not included because the math module is usually needed and those numbers are already defined there.
'''

from __future__ import division
from math import pi

class Constants:
    '''
        Physical constants.
    '''
    c         =   2.99792458e8           # speed of light in m/s
    e         =   1.602176565e-19        # fundamental charge in C
    hJ        =   6.62606896e-34         # Planck constant in J s
    heV       =   4.13566733e-15         # Planck constant in eV s
    hbarJ     =   1.054571628e-34        # Reduced Planck constant in J s
    hbareV    =   6.58211899e-16         # Reduced Planck constant in eV s
    eps0      =   8.854187817620391e-12  # Electromagnetic permittivity in F/m
    mu0       =   1.256637061435917e-6   # Electromagnetic permeability in N/A2
    Z0        = 376.7303134617706        # Electromagnetic impedance of vacuum
    G         =   6.6742e-11             # Gravitational constant in N m2/kg2
    EM        =   8.987551787368176e9    # Electromagnetic constant in N m2/C2
    muB       =   9.27400949e-24         # Bohr magneton in J/T
    muN       =   5.05078343e-27         # Nuclear magneton in J/T
    a0        =   5.291772108e-11        # Bohr radius in m
    alpha     =   7.297352568e-3         # Fine structure constant
    Rydberg   =   1.0973731568525e7      # Rydberg constant in 1/m
    Nav       =   6.02214199e23          # Avogadro constant in 1 / mol
    kBJ       =   1.3806505e-23          # Boltzmann constant in J / K
    kBeV      =   8.61733243e-5          # Boltzmann constant in eV / K
    R         =   8.314472               # Gas constant in J/ mol / K

class Units:
    '''
        Conversions factors among units. The international system of units is set to 1.
    '''
    m  = kg =  s =  C =  A =  J =  N = 1e+0
    mm =  g = ms = mC = mA = mJ = mN = 1e-3
    um = mg = us = uC = uA = uJ = uN = 1e-6
    nm = ug = ns = nC = nA = nJ = nN = 1e-9
    pm = ng = ps = pC = pA = pJ = pN = 1e-12
    fm = pg = fs = fC = fA = fJ = fN = 1e-15
    amu = 1.66053886e-27   * kg
    AU  = 1.49597870700e11 * m
    pc  = 3.08567758e16    * m
    ly  = 9.4605284e15     * m
    eV  = Constants.e      * J
    keV = 1e3              * eV
    MeV = 1e6              * eV
    GeV = 1e9              * eV
    TeV = 1e12             * eV
    PeV = 1e15             * eV

class Conversions:
    amu2kg    =   1.66053886e-27
    amu2MeV   = 931.4943551262353

class ParticlesMasses:
    '''
        Masses of some fundamental particles.
    '''
    e    =  0.510998928 * Units.MeV
    pi0  =  0.1349766   * Units.GeV
    pipm =  0.13957018  * Units.GeV
    p    =  0.938272013 * Units.GeV
    n    =  0.939565560 * Units.GeV
    mu   =  0.105658369 * Units.GeV
    W    = 80.401       * Units.GeV
    Z    = 91.1876      * Units.GeV

def Force( particle1, particle2, interaction_type = 'em' ):
    '''
        Force applied to particle1 due to the interaction of type interaction_type with particle2.
    '''
    if   interaction.upper() == 'G':
        constant = Constants.G * particle1.mass * particle2.mass
    elif interaction.upper() == 'EM':
        constant = Constants.EM * particle1.charge * particle2.charge

    relative_vector = particle1.pos - particle2.pos
    return constant * relative_vector.norm() / relative_vector.mag2

