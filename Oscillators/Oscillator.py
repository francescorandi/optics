# -*- coding: utf-8 -*-
"""
Basic attributes and methods shared by all oscillators.
"""

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

class oscillator(object):
    """Base class for all kinds of oscillators."""
    
    def __init__(self):
        
        # String giving a name to the representation
        self.representation = None 

        # Attribute for quick lookup for calculated dielectric function values
        self.dfunc = None
        
        # Attribute for quick lookup for calculated spectral weight (SW) value
        self.SW = None 
    
    def __repr__(self):
        return 'Null Oscillator' #print also the parameters!
        
    def __str__(self):
        return 'Base oscillator object.'
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function."""
        pass
    
    def opticalConductivity(self, window):
        """Returns the optical conductivity of the oscillator.
        
        \sigma(E) = \epsilon_2(E)*\epsilon_0*E/\hbar^2
        """
        
        # Fix units!
        _hbar = physical_constants['natural unit of action in eV s'][0]
        _preFactor = constants.epsilon_0/_hbar

        return _preFactor*np.imag(self.dielectricFunction(window))*window
    
    def refractionIndex(self):
        """Returns the complex refractive index."""
        pass
    
    def spectralWeight(self, window):
        """Calculates the area of the oscillator given its
           parameters."""
        pass
    
    def plasmaFrequency(self):
        """Calculates the square of plasma frequency in eV^2 of
        the oscillator given its parameters."""
        pass