# -*- coding: utf-8 -*-
"""
Basic attributes and methods shared by all oscillators.
"""
import abc

def _paramValidator(obj, types, value, default):
    """Checks if the input provided for the attribute is valid."""

    try:
        if not isinstance(value, types):
            obj._val = default
            raise TypeError
        if value < 0:
            obj._val = default
            raise ValueError
        else:
            obj._val = float(value)
    except ValueError:
        print("Should be a positive number. Value set at ", default)
    except TypeError:
        print("Should be a number type. Value set at ", default)

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
