﻿# -*- coding: utf-8 -*-
"""
Tauc-Lorentz family of oscillators.
"""
from Oscillators.Oscillator import BaseOscillator, paramValidator, hbar

import numpy as np
import scipy.constants as constants
#from math import log, pow, sqrt

#import scipy.special

class Tauc(BaseOscillator):
    """Tauc-Lorentz lineshape of the form

    .. math::
        FIX DOC!
        \epsilon(E) = -\frac{A}{E^2+\imath \gamma E}

        Where:
        $A$ is the amplitude (eV^2),
        $\gamma$ is the width (eV).


    """

    representation = "standard"

    def __init__(self, amplitude, width, position, gap):
        """Defines a Tauc-Lorentz lineshape as described in
        FIND REFERENCE

        input
        =====

        amplitude: Amplitude (dimensionless)
        width: width of the lineshape (eV)
        position: center position of the oscillator (eV)
        gap: energy gap
        """

        super().__init__()

        self.amplitude = amplitude
        self.width = width
        self.position = position
        self.gap = gap

    def __repr__(self):
        pass

    def __str__(self):
        return 'Tauc-Lorentz lineshape with intensity {:.5f} and width {:.5f}'.format(self.amplitude, self.width)

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = paramValidator(value, (int, float))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = paramValidator(value, (int, float))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = paramValidator(value, (int, float))

    @property
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, value):
        self._gap = paramValidator(value, (int, float))

    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.

        input
        =====

        energy: Specified (range) of values to return.
        """
        raise NotImplementedError

    def spectralWeight(self):
        """Returns the spectral weight of the oscillator."""

        pass

class Tauc_genosc(Tauc):
    """Tauc-Lorentz lineshapeof the form

    .. math::

        \epsilon_2(E) = \frac{ACE_c(E-E_g)^2}{(E^2-E_c^2)^2 +C^2E_c^2}\frac{1}{E} \quad E>E_g, 0 otherwise

        Where:
        $A$ is the amplitude (dimensionless),
        $C$ the width (eV),
        $E_c$ energy center (eV),
        $E_g$ energy gap

        and \epsilon_1 is determined via Kronig-Kramers.
    """

    def __init__(self, amplitude, energy, width, gap):
        """Defines a Tauc-Lorentz lineshape as described in
        FIX! Reutilize better code from the parent class!

        input
        =====

        amplitude: Amplitude (dimensionless)
        energy: Energy center (eV)
        width: width of the lineshape (eV)
        gap: energy gap (eV)
        """

        assert amplitude >= 0
        assert energy >= 0
        assert width >= 0
        assert gap >= 0

        self.amplitude = amplitude
        self.energy = energy
        self.width = width

    def __repr__(self):
        return 'Tauc-Lorentz lineshape' #print also the parameters!

    def dielectricFunction(self, energy):
        """

        input
        =====

        energy: Specified (range) of values to return.
        """
        def _tauc_lorentz():
            """Compute Tauc-Lorentz. It seems that it it still incomplete.

            The function is protected against unphysical values of the args.
            """

            if min(energy) > self.gap:
                return _compute_tauc()

            else:
                dist = np.abs(energy-self.gap)
                ind = dist.argmin()
                _tmp = np.zeros(ind+1)
                _tauc = _compute_tauc(energy[ind+1:])
                return np.concatenate((_tmp, _tauc))

        def _compute_tauc(energy):
            num = self.amplitude*energy*self.width*(energy-self.gap)**2
            den = energy*((energy**2-self.energy**2)**2+(self.width*energy)**2)
            return np.divide(num,den)

        def _reallDF(imaginaryPart):
            #Add KK consistent part
            return np.zeros(len(imaginaryPart))

        #_imaginaryPart = _imagDF(energy)
        #_realPart = _realDF(_imaginaryPart)

        #self.dfunc = _realPart + 1.j*_imaginaryPart

        return self.dfunc

    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.

        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')

        else:
            pass

    def __str__(self):
        return 'Tauc-Lorentz (VWase/genosc) lineshape with intensity {:.5f}, width {:.5f} and psition {:.5f}'.format(self.amplitude, self.width, self.position)

    # Placeholder for translation layer, TBD!
    def _translate_from_std(self):
        pass

    def _translate_to_std(self):
        pass
