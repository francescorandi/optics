# -*- coding: utf-8 -*-
"""
Lorentz family of oscillators.
"""

from Oscillators.Oscillator import BaseOscillator, parameter, hbar

import math
import numpy as np
import scipy.constants as constants


class Lorentz(BaseOscillator):
    """Lorentzian lineshape of the form

    .. math::

        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}

        Where:
        $A$ is the amplitude (dimensionless),
        $B$ the width (eV),
        $E_c$ energy center (eV).
    """

    nparams = 3

    representation = "standard"

    amplitude = parameter('amplitude', 0.0)
    width = parameter('width', 0.0)
    position = parameter('position', 0.0)

    def __init__(self, amplitude=0.0, width=0.0, position=0.0):
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
        return "Lorentz(amplitude = %f, width = %f, position = %f)" % (self.amplitude, self.width, self.position)

    def __str__(self):
        return 'Lorentz lineshape with intensity {:.5f}, width {:.5f}, and position {:-5f}'.format(self.amplitude, self.width, self.position)

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

        _preFactor = constants.epsilon_0*constants.pi/2/hbar**2
        self.SW = _preFactor*self.amplitude*self.position*self.width

        return self.SW

    def dielectricFunction(self, window):
        """Returns the complex dielectric function at the specified window.

        input
        =====

        window: Specified (range) of values to return.
        """

        _den = math.pow(self.position, 2) - np.power(window, 2) - 1.j * window * self.width

        self.dfunc = self.amplitude * np.divide(self.width * self.position, _den)

        return self.dfunc