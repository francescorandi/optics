# -*- coding: utf-8 -*-
"""
Lorentz family of oscillators.
"""

import Oscillator

import math
import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

class Lorentz(Oscillator.oscillator):
    """Lorentzian lineshape of the form 
    
    .. math::
    
        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}
        
        Where:
        $A$ is the amplitude (dimensionless), 
        $B$ the width (eV), 
        $E_c$ energy center (eV).         
    """
    
    def __init__(self, amplitude, width, position):
        """Defines a Lorentz lineshape.
        
        input
        =====
        
        amplitude: Amplitude (dimensionless)
        width: width of the lineshape (eV)
        position: center position of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert width >= 0
        assert position >= 0
        
        super().__init__()
        
        self.amplitude = amplitude
        self.width = width
        self.position = position
        
        self.representation = "standard"
        
    def __repr__(self):
        pass
        
    def __str__(self):
        return 'Lorentz lineshape with \
                        intensity {:.5f}, \
                        width {:.5f}, and \
                        position {:-5f}'.format(self.amplitude, self.width, self.position)
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        _den = math.pow(self.position,2) - np.power(energy,2) - 1.j * energy * self.width
        
        self.dfunc = self.amplitude * np.divide(self.width * self.position, _den)
        
        return self.dfunc

    def spectralWeight(self):
        """Returns the spectral weight of the oscillator."""

        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        self.SW = _preFactor*self.amplitude*self.energy*self.width
        
        return self.SW