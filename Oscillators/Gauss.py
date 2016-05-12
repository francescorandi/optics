# -*- coding: utf-8 -*-
"""
Gaussian family of oscillators.
"""
from Oscillators.Oscillator import BaseOscillator, paramValidator, hbar

import numpy as np
import scipy.special
from math import log, pow, sqrt

class Gauss(BaseOscillator):
    """Gausian lineshape of the form

    .. math::

        \epsilon(E) = -\frac{A}{E^2+\imath \gamma E}

        Where:
        $A$ is the amplitude (eV^2),
        $\gamma$ is the width (eV).


    """

    representation = "standard"

    def __init__(self, amplitude, width, position):
        """Defines a Gaussian lineshape as described in
        D. De Sousa Meneses, J. Non-Cryst. Solids 351 no.2 (2006) 769-776

        input
        =====

        amplitude: Amplitude (dimensionless)
        width: width of the lineshape (eV)
        position: center position of the oscillator (eV)
        """

        super().__init__()

        self.amplitude = amplitude
        self.width = width
        self.position = position

    def __repr__(self):
        pass

    def __str__(self):
        return 'Gaussian lineshape with intensity {:.5f}, width {:.5f}, and position {:.5f}'.format(self.amplitude, self.width, self.position)

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

    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.

        input
        =====

        energy: Specified (range) of values to return.
        """

        LN2 = log(2)
        SLN2 = sqrt(LN2)
        G2 = pow(self.width, 2)

        _imag = self.amplitude * \
                ( np.exp(-4.0 * LN2 * np.power(energy-self.position,2) / G2) \
                - np.exp(-4.0 * LN2 * np.power(energy+self.position,2) / G2))

        _real = self.amplitude * 2.0 / sqrt(np.pi) * \
        (scipy.special.dawsn(2.0*SLN2 * (energy+self.position) / self.width) \
        -scipy.special.dawsn(2.0*SLN2 * (energy-self.position) / self.width))

        _den = energy + 1.j * self.width
        self.dfunc = np.divide(-self.amplitude, energy * _den)

        return _real + 1.j*_imag

    def spectralWeight(self):
        """Returns the spectral weight of the oscillator."""

        _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
        self.SW = _preFactor*self.amplitude

        return self.SW

class Gauss_genosc(Gauss):
    """Gaussian lineshapeof the form

    .. math::

        \epsilon_2(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}

        Where:
        $A$ is the amplitude (dimensionless),
        $B$ the width (eV),
        $E_c$ energy center (eV),

        and \epsilon_1 is determined via Dawson function Kronig-Kramers
        consistent.
    """

    def __init__(self, amplitude, energy, width):
        """Defines a Gaussian lineshape as described in
        D. De Sousa Meneses, J. Non-Cryst. Solids 351 no.2 (2006) 769-776

        input
        =====

        amplitude: Amplitude (dimensionless)
        energy: Energy center (eV)
        width: width of the lineshape (eV)
        """

        assert amplitude >= 0
        assert energy >= 0
        assert width >= 0

        self.amplitude = amplitude
        self.energy = energy
        self.width = width

    def __repr__(self):
        return 'Gaussian lineshape' #print also the parameters!

    def dielectricFunction(self, energy):
        """

        input
        =====

        energy: Specified (range) of values to return.
        """

        def _realDF(imaginatyPart):
            #Add KK consistent part
            return 0

        def _imagDF(energy):
            sigma = self.width/(2*sqrt(log(2)))
            e1 = np.exp(-((energy-self.energy)/sigma)**2)
            e2 = np.exp(-((energy+self.energy)/sigma)**2)

            return self.amplitude*(e1-e2)

        _imaginaryPart = _imagDF(energy)
        _realPart = _realDF(_imaginaryPart)

        self.dfunc = _realPart + 1.j*_imaginaryPart

        return self.dfunc

    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.

        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')

        else:
            _hbar = physical_constants['natural unit of action in eV s'][0]
            _preFactor = constants.epsilon_0*sqrt(constants.pi)/4*(log(2))/_hbar**2
            return _preFactor*self.amplitude*self.energy*self.width


    def __str__(self):
        return 'Gaussian (VWase/genosc) lineshape with intensity {:.5f}, width {:.5f} and psition {:.5f}'.format(self.amplitude, self.width, self.position)

    # Placeholder for translation layer, TBD!
    def _translate_from_std(self):
        self._width = self.width
        self._amplitude = self.amplitude/self.width

    def _translate_to_std(self):
        self.width = self._width
        self.amplitude = self._amplitude*self._width
