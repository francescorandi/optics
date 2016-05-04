# -*- coding: utf-8 -*-
"""
Drude family of oscillators.
"""

from Oscillators.Oscillator import BaseOscillator

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

_hbar = physical_constants['natural unit of action in eV s'][0]

def validation(obj, types, value, default):
    """Checks if the input provided for the attribute is valid."""

    try:
        if not isinstance(value, types):
            obj._val = 0.
            raise TypeError
        if value < 0:
            obj._val = 0.
            raise ValueError
        else:
            obj._val = float(value)
    except ValueError:
        print("Should be a positive number. Value set at ", default)
    except TypeError:
        print("Should be a number type. Value set at ", default)

class Drude(BaseOscillator): # Using the base oscillator as parent
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
    def amplitude(self, value):
        validation(self, (int, float), value, 0.0)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        validation(self, (int, float), value, 0.0)

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
        """Returns the calculated spectral weight of the oscillator."""

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
