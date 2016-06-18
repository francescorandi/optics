# -*- coding: utf-8 -*-
"""
Basic attributes and methods shared by all oscillators.
"""
import abc
from numbers import Number

#  import scipy.constants as constants
from scipy.constants import physical_constants

hbar = physical_constants['natural unit of action in eV s'][0]


def _parameter(name, default=0.0):
    """Checks if the input provided for the attribute is valid."""

    storage_name = '_' + name

    @property
    def attribute(self):
        return getattr(self, storage_name)

    @attribute.setter
    def attribute(self, value):
        try:
            # If it's a number
            if not isinstance(value, Number):
                if not value.isdigit():
                    raise TypeError
            if isinstance(value, complex):
                raise TypeError
            if value < 0.0:  # no value should be below 0?
                raise ValueError
            setattr(self, storage_name, float(value))  # casting to float
        except:
            print("The parameter '{}' should be a positive number. Value set at {}".format(name, default))
            setattr(self, storage_name, default)

    return attribute


class BaseOscillator(metaclass=abc.ABCMeta):
    """Base class for all oscillator implementations."""

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

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
        """Calculates and returns the area of the oscillator analytically or numerically."""
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
