# -*- coding: utf-8 -*-
"""
Various kinds of relations and conversions
"""

import numpy as np
from scipy.constants import physical_constants

"""
Unit conversion
"""

class NotImplemented(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

availableEnergyUnits = ('eV', 'cm-1', 'THz', 'nm')

def xtoeV(x, unitX):
    if unitX == 'nm'    : return 1239.0/x
    elif unitX == 'um'  : return 1239.0/(1e3*x)
    elif unitX == 'THz' : return x/(physical_constants['electron volt-hertz relationship'][0]/10**12)
    elif unitX == 'cm-1': return x/(physical_constants['electron volt-inverse meter relationship'][0]/100)
    elif unitX == 'eV'  : return x
    else: raise NotImplemented("Conversion not implemented")

def eVtox(x, unitX):
    if unitX == 'nm'    : return 1239.0/x
    elif unitX == 'um'  : return 1239.0/(1e3*x)
    elif unitX == 'THz' : return x*(physical_constants['electron volt-hertz relationship'][0]/10**12)
    elif unitX == 'cm-1': return x*(physical_constants['electron volt-inverse meter relationship'][0]/100)
    elif unitX == 'eV'  : return x
    else: raise NotImplemented("Conversion not implemented")

"""
Optical relations
"""

def identity(epsilon):
    return epsilon

def reflectivity(epsilon, theta=0.0, polarization='s'):
    #TODO Fresnel
    n = refractive_index(epsilon)
    R = np.abs((n-1)/(n+1))**2

    return R

def refractive_index(epsilon):
    n = np.sqrt(epsilon)
    
    return n

def conductivity(x, epsilon):
    s = 0.0 + 0.0j

    return s
