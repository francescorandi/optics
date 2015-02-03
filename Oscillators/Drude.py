# -*- coding: utf-8 -*-
"""
Drude family of oscillators.
"""

import Oscillator

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

class Drude(Oscillator.oscillator):
    """Drude lineshape of the form 
    
    .. math::
    
        \epsilon(E) = -\frac{A}{E^2+\imath \gamma E}
        
        Where:
        $A$ is the amplitude (eV^2), 
        $\gamma$ is the width (eV).  
        
        
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
        
        super().__init__()
        
        self.amplitude = amplitude
        self.width = width
        
        self.representation = "standard"
        
    def __repr__(self):
        pass
        
    def __str__(self):
        return 'Drude lineshape with intensity {:.5f} and width {:.5f}'.format(self.amplitude, self.width)
        
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
        """Returns the spectral weight of the oscillator."""

        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        self.SW = _preFactor*self.amplitude
        
        return self.SW
        
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
        
        amplitude: Amplitude (eV)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert width >= 0
        
        # Genosc representation        
        self._amplitude = amplitude
        self._width = width
        
        # Translation of parameter representations "hidden".
        super().__init__(amplitude/width, width)
        
        self.representation = "genosc"
        
    def __repr__(self):
        pass
        
    def __str__(self):
        return 'Drude (VWase/genosc) lineshape with intensity {:.5f} and width {:.5f}'.format(self.amplitude, self.width)
        
    def _translate_from_std(self):
        self._width = self.width
        self._amplitude = self.amplitude/self.width
    
    def _translate_to_std(self):
        self.width = self._width
        self.amplitude = self._amplitude*self._width
    
# Legacy code. Not needed because of inheritance. To be removed.
    
#    def dielectricFunction(self, energy):
#        """Returns the complex dielectric function at the specified energy.
#        
#        input
#        =====
#        
#        energy: Array specifying the energies to be evaluated.
#        """
#        
#        num = -(self._amplitude*self._width)
#        den = energy**2+1.j*self._width*energy
#        
#        self.dfunc = num/den
#        
#        return self.dfunc
        
#    def spectralWeight(self):
#        """Returns the spectral weight of the oscillator."""
#
#        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
#        return _preFactor*self._amplitude*self._width