# -*- coding: utf-8 -*-
"""
Basic attributes and methods shared by all oscillators.
"""
import abc

import scipy.constants as constants
from scipy.constants import physical_constants

hbar = physical_constants['natural unit of action in eV s'][0]

def paramValidator(value, types, default = 0.0):
    """Checks if the input provided for the attribute is valid."""
    try:
        if not isinstance(value, types) or value < 0:
            print("Should be a positive number. Setting on default ", default)
            return default
        else:
            return float(value)
    except:
        print("Unexpected error in input!")

class BaseOscillator(metaclass=abc.ABCMeta):
    """Base class for all oscillator implementations."""

    @abc.abstractmethod
    def dielectricFunction(self, energy):
        """Computes and returns the complex dielectric function of the oscillator."""
        pass

    # @abc.abstractmethod
    # def opticalConductivity(self, window):
    #     """Computes and returns the optical conductivity of the oscillator.
    #
    #     \sigma(E) = \epsilon_2(E)*\epsilon_0*E/\hbar^2
    #     """
    #     pass

    @abc.abstractmethod
    def spectralWeight(self, window):
        """Calculates and returns the area of the oscillator analitically or numerically."""
        pass

    # @abc.abstractmethod
    # def plasmaFrequency(self):
    #     """Calculates the square of plasma frequency in eV^2 of
    #     the oscillator given its parameters."""
    #     pass

    # def _translate_from_std(self):
    #     #Implemented only in non standard representations
    #     pass
    #
    # def _translate_to_std(self):
    #     #Implemented only in non standard representations
    #     pass
