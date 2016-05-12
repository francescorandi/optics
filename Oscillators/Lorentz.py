# -*- coding: utf-8 -*-
"""
Lorentz family of oscillators.
"""

from Oscillators.Oscillator import BaseOscillator, paramValidator, hbar

import math
import numpy as np

class Lorentz(BaseOscillator):
    """Lorentzian lineshape of the form

    .. math::

        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}

        Where:
        $A$ is the amplitude (dimensionless),
        $B$ the width (eV),
        $E_c$ energy center (eV).
    """

    representation = "standard"

    def __init__(self, amplitude, width, position):
        """Defines a Lorentz lineshape.

        input
        =====

        amplitude: Amplitude (dimensionless)
        width: width of the lineshape (eV)
        position: center position of the lineshape (eV)
        """

        super().__init__()

        self.amplitude = amplitude
        self.width = width
        self.position = position

    def __repr__(self):
        pass

    def __str__(self):
        return 'Lorentz lineshape with intensity {:.5f}, width {:.5f}, and position {:-5f}'.format(self.amplitude, self.width, self.position)

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = 0.0
        self._amplitude = paramValidator(value, (int, float))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = 0.0
        self._width = paramValidator(value, (int, float))

    @property
    def position(self):
        return self.position

    @width.setter
    def position(self, value):
            self._position = 0.0
            self._position = paramValidator(value, (int, float))

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
