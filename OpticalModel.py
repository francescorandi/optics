import collections
import json
from math import ceil, log

import h5py
import matplotlib.pyplot as pyplot
import numpy as np
from scipy.integrate import romb

import Oscillators
from Oscillators import Drude, Lorentz, Gauss

# Parameters for plots. Shouldn't be here!
params = {
   'axes.labelsize': 8,
   'text.fontsize': 8,
   'legend.fontsize': 10,
   'xtick.labelsize': 10,
   'ytick.labelsize': 10,
   'figure.figsize': [7, 9.3]
   }
pyplot.rc(params)


class OpticalModel(collections.MutableSequence):
    """Class to store and handle the oscillator model of the dielectric
    function.
    """

    __counter = 0

    def __init__(self, name=None, desc=None, label=None, oscillators=None):
        """Optical model built from a collection of oscillators.

        inputs (optional):
            name: name of the model being built.
            desc: description of the model.
            label: extra attribute to have an extra label, e.g., temperature.
            oscillators: an iterable of oscillator instances to be added when
            constructing the optical model."""

        # Metadata Section

        type(self).__counter += 1

        if name:
            self._name = name
        else:
            self._name = "Optical Model %d" % self.__counter

        self._desc = desc
        self._label = label

        # Physics section

        if oscillators:
            self.__oscillators = oscillators
        else:
            self.__oscillators = []

        self._einf = 1.0
        self._polelow = [0.1, 0]
        self._polehigh = [10, 0]

    def __del__(self):
        type(self).__counter -= 1

    @staticmethod
    def OpticalModelInstances():
        return OpticalModel.__counter

    @staticmethod
    def __checkValue(value):
        if not isinstance(value, Oscillators.BaseOscillator):
            raise TypeError("Only oscillators can be added.")

    def __str__(self):
        return str(self.name)

    # Following 5 methods to implement the MutableSequence

    def __len__(self):
        return len(self.__oscillators)

    def __getitem__(self, index):
        return self.__oscillators[index]

    def __delitem__(self, index):
        del self.__oscillators[index]

    def __setitem__(self, index, value):
        self.__checkValue(value)
        self.__oscillators[index] = value

    def insert(self, index, value):
        self.__checkValue(value)
        self.__oscillators.insert(index, value)

    def __add__(self, other):
        return OpticalModel(oscillators=self.__oscillators + other.__oscillators)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, string):
        self._name = string

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, string):
        self._desc = string

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def params(self):
        P = []
        for oscillator in self.__oscillators:
            P.extend(oscillator.params)

        return P

    @params.setter
    def params(self, P):
        for oscillator in self.__oscillators:
            oscillator.params = P[0:oscillator.nparams]
            np.delete(P, slice(0, oscillator.nparams))

    def sort(self):
        """Sorts the oscillators of the model in ascending order by energy."""
        self.__oscillators.sort(key=lambda oscillator: oscillator.position)

    def show(self):
        """Prints the collection of oscillators composing the model."""
        print("Composition of: %s" % self.name)
        print("Description: %s" % self.desc)
        print("======Epsilon 1==========")
        print("epsilon_1 at infinity: %f" % self.einf)
        print("Pole 1: {}@{} eV".format(*self.poles[0]))
        print("Pole 2: {}@{} eV".format(*self.poles[1]))
        print("======Oscillators (epsilon 2)=============")
        print("Index\t Type\t Attributes")
        print("==========================================")
        for index, oscillator in enumerate(self.__oscillators):
            print("\t".join([str(index), type(oscillator).__name__, str(oscillator)]))

    def add(self, oscillator):
        """Add one or more oscillators (iterable) to the model. Wrapper around
        append and extend methods.

        Parameters:
        oscillator: an oscillator object or iterable
        """
        if isinstance(oscillator, list):
            self.extend(oscillator)
        else:
            self.append(oscillator)

    def clear(self):
        """Removes all oscillators from the model."""

        self.__oscillators = []

    def save(self, filename):
        """Exports the model as a json file."""

        with open(filename, 'w') as f:
            _dump = dict()
            _dump['type'] = 'model'
            # Preparing metadata
            _dump['name'] = self.name
            _dump['desc'] = self.desc

            # Preparing epsilon1

            _dump['eps1'] = {'einf': self.einf,
                             'pole1': self._polelow,
                             'pole2': self._polehigh}

            # Preparing oscillators
            _dump['oscillators'] = []
            for osc in self.__oscillators:
                _dump['oscillators'].append(repr(osc))

            json.dump(_dump, f, sort_keys=True, indent=2)
            print("Model is saved as: ", filename)

    def load(self, filename):
        """Imports a model from a json file."""

        with open(filename, 'r') as f:
            _data = json.load(f)
            if 'type' in _data.keys() and _data['type'] == 'model':
                self.name = _data['name']
                self.desc = _data['desc']

                self.einf = _data['eps1']['einf']
                self.poles = [*_data['eps1']['pole1'], *_data['eps1']['pole2']]

                for osc in _data['oscillators']:
                    # Uses the representation of an oscillator to recreate it
                    self.add(eval(osc))
            print("Model '%s' was loaded!" % filename)

    def savetohdf5(self, target):
        """
        Saves model to hdf5 file. Can be used directly or called
        from a higher level function (e.g. system.save()).

        hdf5 can either be the filename or an hdf5 group.
        """

        # Testing if target is a string, if true creates an hdf5 file.
        if isinstance(target, str):
            hdf5 = h5py.File(target, "w")

        for index, oscillator in enumerate(self.__oscillators):
                h5osc = hdf5.create_group(str(index))
                h5osc.attrs['type'] = oscillator.__class__.__name__
                h5osc.create_dataset("params", data=oscillator.params)

        return True

    def loadfromhdf5(self, target):
        """
        Loads model from hdf5 file. Can be used directly or called
        from a higher level function (e.g. system.load()).

        hdf5 can either be the filename or an hdf5 group.
        """
        if isinstance(target, str):
            hdf5 = h5py.File(target, "r")

        for idx, h5osc in hdf5.items():
            osc = getattr(Oscillators, h5osc.attrs['type'])()
            osc.params = h5osc['params'][:]
            self.add(osc)

        return True

    def build_from_parameters(self, Parameter, Type, Constraint):
        self.clear()
        self.append(self.__params2oscillator(Parameter, Type, Constraint))

    @property
    def einf(self):
        return self._einf

    @einf.setter
    def einf(self, value):
        self._einf = value

    @property
    def poles(self):
        return self._polelow, self._polehigh

    @poles.setter
    def poles(self, value):
        self._polelow = value[0:2]
        self._polehigh = value[2:4]

    def _pole(self, window, intensity, position):
        # For a single value the ** operator is faster than the pow() function
        # For an array, apparently the pow() function is faster

        return np.divide(intensity, position ** 2 - pow(window, 2))

    def dielectricFunction(self, window):
        """Calculates the complex dielectric function of the model.

        Parameter:
        window -- Set of points where to calculate the dielectric function.

        Returns:
                The calculated dielectric function.
        """

        _eps = self._einf  # Broadcasting einf
        # _eps = np.zeros(len(window), dtype = np.cfloat)
        #_eps = np.ones(len(window), dtype=np.cfloat)

        for oscillator in self.__oscillators:
            _eps += oscillator.dielectricFunction(window)

        # Checking if poles have any intensity
        if self.poles[0][1] != 0:
            _eps += self._pole(window, *self.poles[0])
        if self.poles[1][1] != 0:
            _eps += self._pole(window, *self.poles[1])

        return _eps

    def opticalConductivity(self, window):
        """Calculates the complex optical conductivity of the model.

        Parameter:
        window -- Set of points where to calculate the optical conductivity.

        Returns:
                The calculated complex optical conductivity \sigma = \imath\omega\varepsilon.
        """
        # TODO: Check formula and units!
        return window * self.dielectricFunction(window)

    def spectralWeight(self, limits=None):
        """Calculates the spectral weight of the model. If an energy
         window is give, a partial spectral weight is returned.

         Parameter:
         limits -- A tuple indicating beginning and end where to calculate
                   the partial spectral weight of the model.

         Returns:
            The calculated dielectric function.
         """

        _sw = 0.0

        if not limits:
            for oscillator in self.__oscillators:
                _sw += oscillator.spectralWeight

        else:
            # Using Romberg: See http://young.physics.ucsc.edu/242/romberg.pdf
            interval = limits[1]-limits[0]

            # Finding minimal k for a smaller than 0.02 integration step
            k = ceil(log(interval/0.02-1)/log(2))

            # Determining final step size
            dx = interval/(2.0**k)

            # Create a 2**k+1 equally spaced sample
            x = np.linspace(limits[0], limits[1], 2**k+1)

            _sw = romb(np.imag(self.dielectricFunction(x)), dx)

        return _sw

    def refractiveIndex(self, window):
        """Calculates the complex refractive index of the model.

        Parameter:
        window -- Set of points where to calculate the complex refractive index.

        Returns:
                The calculated complex refractive index.
        """

        return np.sqrt(self.dielectricFunction(window))

    def reflectivity(self, window):
        """Calculates the reflectivity of the model.

        Parameter:
        window -- Set of points where to calculate the complex refractive index.

        Returns:
                The calculated complex refractive index.
        """
        __n = self.refractiveIndex(window)
        return np.abs((__n-1)/(__n+1))**2

    def __singleAxisPlot(self, x, y, label):
        pyplot.figure()
        pyplot.xticks(fontsize=14)
        pyplot.yticks(fontsize=14)
        pyplot.plot(x, y, 'r-')
        pyplot.ylabel(label, color='r', fontsize=22)
        pyplot.xlabel('Energy (eV)', fontsize=18)
        pyplot.title(self.name, fontsize=18)

    def __doubleAxisPlot(self, x, y, labels):
        # Split e1 and e2 in two different y-axis!
        # from http://matplotlib.org/examples/api/two_scales.html
        fig, ax1 = pyplot.subplots()
        ax1.plot(x, np.real(y), color='#1F0965', linestyle='-')
        ax1.set_ylabel(labels[0], color='#1F0965', fontsize=22)
        ax1.set_xlabel('Energy (eV)', fontsize=18)
        ax2 = ax1.twinx()
        ax2.plot(x, np.imag(y), color='#937A00', linestyle='-')
        ax2.set_ylabel(labels[1], color='#937A00', fontsize=22)
        pyplot.title(self.name, fontsize=18)

    def plot(self, window, *, flag=None, **kwargs):
        """Plots the dielectric function of the model.
        Possible flags"""

        if flag is "R":
            self.__singleAxisPlot(window, self.reflectivity(window), label='R')

        elif flag is "e1":
            self.__singleAxisPlot(window, np.real(self.dielectricFunction(window)), r'$\varepsilon_1$')

        elif flag is "e2":
            self.__singleAxisPlot(window, np.imag(self.dielectricFunction(window)), r'$\varepsilon_2$')

        elif flag is "s1":
            raise NotImplemented
            self.__singleAxisPlot(window, np.real(self.opticalConductivity(window)), r'$\sigma_1$')

        elif flag is "nk":
            self.__doubleAxisPlot(window, self.refractiveIndex(window), labels=['n', 'k'])

        else:
            self.__doubleAxisPlot(window, self.dielectricFunction(window), labels=[r'$\varepsilon_1$', r'$\varepsilon_2$'])
