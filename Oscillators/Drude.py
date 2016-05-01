# -*- coding: utf-8 -*-
"""
Drude family of oscillators.
"""

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

class Drude: # Using the base oscillator as parent
    """Drude lineshape of the form

    .. math::

        \epsilon(E) = -\frac{A}{E^2+\imath \gamma E}

        Where:
        $A$ is the amplitude (eV^2),
        $\gamma$ is the width (eV).


    """
    _nparams = 2

    def __init__(self, amplitude=0., width=0.):
        """Defines a Drude lineshape.

        input
        =====

        amplitude: Amplitude (eV^2)
        width: width of the lineshape (eV)
        """

        assert amplitude >= 0
        assert width >= 0

        #super().__init__()

        self.amplitude = amplitude
        self.width = width
        self.position = 0

        self.representation = "standard"

    def __repr__(self):
        return "Drude(amplitude = %d, width = %d)" % (self.amplitude, self.width)

    def __str__(self):
        return 'Drude lineshape with intensity {:.5f} and width {:.5f}'.format(self.amplitude, self.width)
        
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
    def params(self):
        return [self.amplitude, self.width]
       
    @params.setter 
    def params(self, p):
        self.amplitude = p[0]
        self.width = p[1]
    
    @property    
    def spectralWeight(self):
        """Returns the calculated spectral weight of the oscillator."""

        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        self.SW = _preFactor*self.amplitude

        return self.SW

    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.

        input
        =====

        energy: Specified (range) of values to return.
        """

        _den = energy + 1.j * self.width
        self.dfunc = np.divide(-self.amplitude, energy * _den)

        return self.dfunc

class Drude_genosc(Drude):
    """Drude lineshape of the form

    .. math::

        \epsilon(E) = -\frac{AB}{E^2+\imath BE}

        Where:
        $A$ is the amplitude (eV),
        $B$ the width (eV).

        As defined in WVase genosc.
    """
    
    _nparams = 2

    def __init__(self, amplitude=0., width=0.):
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
        
    @property
    def params(self):
        return [self.amplitude, self.width]
       
    @params.setter 
    def params(self, p):
        self.amplitude = p[0]
        self.width = p[1]
