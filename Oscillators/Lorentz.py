# -*- coding: utf-8 -*-
"""
Lorentz family of oscillators.
"""

# import Oscillator

import math
import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

class Lorentz(object):
    """Lorentzian lineshape of the form

    .. math::

        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}

        Where:
        $A$ is the amplitude (dimensionless),
        $B$ the width (eV),
        $E_c$ energy center (eV).
    """

    _nparams = 3

    def __init__(self, amplitude=0.0, width=0.0, position=0.0):
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
        return 'Lorentz lineshape with intensity {:.5f}, width {:.5f}, and position {:-5f}'.format(self.amplitude, self.width, self.position)
        
    @property
    def amplitude(self):
        return self._amplitude
    
    @amplitude.setter
    def amplitude(self, a):
        self._amplitude = abs(a)
        
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = abs(w)
        
    @property
    def position(self):
        return self._position
        
    @position.setter
    def position(self, p):
        self._position = abs(p)
        
    @property
    def params(self):
        return [self.amplitude, self.width, self.position]
       
    @params.setter 
    def params(self, p):
        self.amplitude = p[0]
        self.width = p[1]
        self.position = p[2]
        
    @property
    def spectralWeight(self):
        """Returns the spectral weight of the oscillator."""

        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        self.SW = _preFactor*self.amplitude*self.energy*self.width

        return self.SW

    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.

        input
        =====

        energy: Specified (range) of values to return.
        """

        _den = math.pow(self.position,2) - np.power(energy,2) - 1.j * energy * self.width

        self.dfunc = self.amplitude * np.divide(self.width * self.position, _den)

        return self.dfunc
