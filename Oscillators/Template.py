# -*- coding: utf-8 -*-
"""
Basic attributes and methods shared by all oscillators.
"""

from Oscillators.Oscillator import BaseOscillator, paramValidator, hbar

import numpy as np

class oscillator(BaseOscillator):
    """Base class for all kinds of oscillators."""

    # String giving a name to the representation to the class
    representation = None

    def __init__(self):

        # Attribute for quick lookup for calculated dielectric function values
        self.dfunc = None

        # Attribute for quick lookup for calculated spectral weight (SW) value
        self.SW = None

    # Probably __repr__ is not needed here
    def __repr__(self):
        return 'Null Oscillator'

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

    def spectralWeight(self, window):
        """Calculates the area of the oscillator given its
           parameters."""
        pass

    def plasmaFrequency(self):
        """Calculates the square of plasma frequency in eV^2 of
        the oscillator given its parameters."""
        pass

    def _translate_from_std(self):
        #Implemented only in non standard representations
        pass

    def _translate_to_std(self):
        #Implemented only in non standard representations
        pass
