# -*- coding: utf-8 -*-
"""
Tauc-Lorentz family of oscillators.
"""
from Oscillators.Oscillator import BaseOscillator, parameter, hbar

import numpy as np
import scipy.constants as constants
import cmath
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

    nparams = 4

    representation = "standard"

    amplitude = parameter('amplitude', 0.0)
    width = parameter('width', 0.0)
    position = parameter('position', 0.0)
    gap = parameter('gap', 0.0)

    def __init__(self, amplitude=0.0, width=0.0, position=0.0, gap=0.0):
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
        return "Tauc(amplitude = %f, width = %f, position = %f, gap = %f)" % (self.amplitude, self.width, self.position, self.gap)

    def __str__(self):
        return 'Tauc-Lorentz lineshape with intensity {:.5f} and width {:.5f}'.format(self.amplitude, self.width)

    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.

        input
        =====

        energy: Specified (range) of values to return.
        """
        return _compute_tauc_real(energy)+1.0j*_compute_tauc_imaginary(energy)
        
    def _compute_tauc_real(self, energy):
        E0 = self.position
        A = self.amplitude
        C = self.width #gamma
        Eg = self.gap
        x = energy
        
        epsinf = 0.0
	alfa = sqrt(4.0*np.power(E0,2) - np.power(C,2))
	g = cmath.sqrt(np.power(E0,2) - np.power(C,2) / 2.0)
	aln = (np.power(Eg,2) - np.power(E0,2))*np.power(x,2) + np.power(Eg,2) * np.power(C,2) - np.power(E0,2) * (np.power(E0,2) + 3.0 * np.power(Eg,2))
	aatan = (np.power(x,2) - np.power(E0,2))*(np.power(E0,2) + np.power(Eg,2)) + np.power(Eg,2)*np.power(C,2)
	csi4 = np.power( np.power(x,2) - np.power(g,2), 2) + np.power(alfa,2) * np.power(C,2) / 4.0
	tauc1 = epsinf + \
			0.5 * A * C / np.pi / csi4 * aln / alfa / E0 * np.log( (np.power(E0,2) + np.power(Eg,2) + alfa*Eg) / (np.power(E0,2) + np.power(Eg,2) - alfa*Eg) ) - \
			A / np.pi / csi4 * aatan / E0 * ( np.pi - np.arctan( (2.0*Eg + alfa)/C ) + np.arctan( (-2.0*Eg+alfa) / C ) ) + \
			2.0 * A * E0 / np.pi / csi4 / alfa * Eg * ( np.power(x,2) - np.power(g,2) ) * ( np.pi + 2.0 * np.arctan( 2.0 * (np.power(g,2) - np.power(Eg,2)) / alfa / C ) ) -\
			A * E0 * C / np.pi / csi4 * np.divide( np.power(x,2) + np.power(Eg,2) , x) * np.log( abs(x-Eg) / (x+Eg) ) +\
			2.0 * A * E0 * C / np.pi / csi4 * Eg * np.log( abs(x-Eg) * (x+Eg) / sqrt( np.power(np.power(E0,2)-np.power(Eg,2),2) + np.power(Eg,2)*np.power(C,2) ) )
			
	return tauc1
        
    
    def _compute_tauc_imaginary(self, energy):
        E0 = self.position
        A = self.amplitude
        C = self.width #gamma
        Eg = self.gap
        x = energy
        
        im = 0.5*(np.sign(x-Eg)+1.0) * A * E0 * C * np.divide( np.power(x-Eg,2), ( np.power( np.power(x,2) - np.power(E0,2), 2) + np.power(C,2) * np.power(x,2) ) * x )
        
        return im

    def spectralWeight(self):
        """Returns the spectral weight of the oscillator."""

        pass

    @property
    def params(self):
        return [self.amplitude, self.width, self.position, self.gap]

    @params.setter
    def params(self, p):
        self.amplitude = p[0]
        self.width = p[1]
        self.position = p[2]
        self.gap = p[3]


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

    nparams = 4

    def __init__(self, amplitude=0.0, energy=0.0, width=0.0, gap=0.0):
        """Defines a Tauc-Lorentz lineshape as described in
        FIX! Reutilize better code from the parent class!

        input
        =====

        amplitude: Amplitude (dimensionless)
        energy: Energy center (eV)
        width: width of the lineshape (eV)
        gap: energy gap (eV)
        """

        super().__init__()

        self.amplitude = amplitude
        self.energy = energy
        self.width = width
        self.gap = gap

    def __repr__(self):
        return 'Tauc-Lorentz lineshape'  # print also the parameters!

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

    @property
    def params(self):
        return [self.amplitude, self.width, self.position, self.gap]

    @params.setter
    def params(self, p):
        self.amplitude = p[0]
        self.width = p[1]
        self.position = p[2]
        self.gap = p[3]

    def __str__(self):
        return 'Tauc-Lorentz (VWase/genosc) lineshape with intensity {:.5f}, width {:.5f} and psition {:.5f}'.format(self.amplitude, self.width, self.position)

    # Placeholder for translation layer, TBD!
    def _translate_from_std(self):
        pass

    def _translate_to_std(self):
        pass
