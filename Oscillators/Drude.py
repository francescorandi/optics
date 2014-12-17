# -*- coding: utf-8 -*-
"""
Drude family of oscillators.
"""

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

from Oscillator import oscillatorModel

class Drude(oscillatorModel):
    """Drude lineshape of the form 
    
    .. math::
    
        \epsilon(E) = -\frac{A}{E^2+\imath \gamma E}
        
        Where:
        $A$ is the amplitude (eV), 
        $\gamma$ is the width (eV).  
        
        
    """
    def __init__(self, amplitude, width):
        """Defines a Drude lineshape.
        
        input
        =====
        
        amplitude: Amplitude (eV)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert width >= 0
        
        self.amplitude = amplitude
        self.width = width
        
        self.representation = "standard"
        
        self.dfunc = None
        
    def __repr__(self):
        return 'Drude lineshape with intensity %s and width %s', (str(self.amplitude), str(self.width))
        
    def __str__(self):
        return 'Drude'
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        _den = energy + 1.j * self.width
        self.dfunc = np.divide(-self.amplitude, energy * _den)
        
        return self.dfunc

    def spectralWeight(self):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        raise NotImplementedError('Not implemented yet')
        
class Drude_genosc(Drude):
    """Drude lineshape of the form 
    
    .. math::

        \epsilon(E) = -\frac{AB}{E^2+\imath BE}    
        
        Where:
        $A$ is the amplitude (eV), 
        $B$ the width (eV).  
        
        As defined in WVase genosc.
    """
    
    def __init__(self, amplitude, width):
        """Defines a Drude lineshape.
        
        input
        =====
        
        amplitude: Amplitude (eV^2)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert width >= 0
        
        self.amplitude = amplitude
        self.width = width
        
        self.representation = "genosc"
        
    def __repr__(self):
        return 'Drude lineshape' #print also the parameters!
        
    def __str__(self):
        return 'Drude VWase/genosc representation.'
        
      
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Array specifying the energies to be evaluated.
        """
        
        num = -(self.amplitude*self.width)
        den = energy**2+1.j*self.width*energy
        
        self.dfunc = num/den
        
        return self.dfunc
        
    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        _hbar = physical_constants['natural unit of action in eV s'][0]
        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        return _preFactor*self.amplitude*self.width