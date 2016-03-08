import collections
import numpy as np
import matplotlib.pyplot as pyplot

import json

class OpticalModel(collections.MutableSequence):
    """Class to store and handle the oscillator model of the dielectric
    function.
    """

    __counter = 0

    def __init__(self, name = None, desc = None, oscillators = None):
        """Optical model built from a collection of oscillators.

        inputs (optional):
            name: name of the model being built.
            desc: description of the model.
            oscillators: an iterable of oscillator instances to be added when
            constructing the optical model."""

        type(self).__counter += 1
        if name:
            self.name = name
        else:
            self.name = "Optical Model %d" % self.__counter

        self.desc = desc

        if oscillators:
            self.oscillators = oscillators
        else:
            self.oscillators = []

    def __del__(self):
        type(self).__counter -= 1

    @staticmethod
    def OpticalModelInstances():
        return OpticalModel.__counter

    def __str__(self):
        pass

    def __len__(self):
        return len(self.oscillators)

    def __getitem__(self, index):
        return self.oscillators[index]

    def __delitem__(self, i):
        del self.oscillators[i]

    def __setitem__(self, index, value):
        # add check for oscillator subclass instance
        self.oscillators[index] = value

    def __add__(self, other):
        return OpticalModel(oscillators = self.oscillators + other.oscillators)

    def insert(self, index, value):
        # add check for oscillator subclass instance
        self.oscillators.insert(index, value)

    def sort(self):
        """Sorts the oscillators of the model in ascending order by energy."""
        self.oscillators.sort(key = lambda oscillator: oscillator.position)

    def show(self):
        """Prints the collection of oscillators composing the model."""
        print("Composition of: %s"% self.name)
        print("Index\t Type\t Attributes")
        print("========================")
        for index, oscillator in enumerate(self.oscillators):
            print("\t".join([str(index), type(oscillator).__name__, str(oscillator)]))

    def add(self, oscillator):
        """Add one or more oscillators to the model.

        Parameters:
        oscillator: an oscillator object
        """

        self.oscillators.append(oscillator)

    def addCollection(self, oscillators):
       """Adds oscillators in an collection (iterable)."""

       for osc in oscillators:
           self.add(osc)

    def clear(self):
        """Removes all oscillators from the model."""

        self.oscillators = []

    def save(self, filename):
        """Saves the model."""

        try:
            f = open(filename, 'w')
        except IOError:
            print("A file cannot be opened. Model not saved")
        else:
            json.dump(self.oscillators, f)
            f.close()
            print("Model is saved as: ", filename)

    def get(self, index = None):
        """Returns the list of oscillators composing the model.
        If a particular index is give, it returns only that oscillator."""

        if index:
            return self.oscillators[index]
        else:
            return self.oscillators

    def build_from_parameters(self, Parameter, Type, Constraint):
        self.clear()
        self.Oscillator = self.__params2oscillator(Parameter, Type, Constraint)

    def dielectric_function(self, window):
        """Calculates the complex dielectric function of the model.

        Parameter:
        window -- Set of points where to calculate the dielectric function.

        Returns:
                The calculated dielectric function.
        """

        _eps = np.zeros(len(window), dtype = complex)

        for oscillator in self.oscillators:
            _eps += oscillator.dielectricFunction(window)

        return _eps

    def refractive_index(self, window):
        """Calculates the complex refractive index of the model.

        Parameter:
        window -- Set of points where to calculate the complex refractive index.

        Returns:
                The calculated complex refractive index.
        """

        return np.sqrt(self.dielectric_function(window))

    def reflectivity(self, window):
        """Calculates the reflectivity of the model.

        Parameter:
        window -- Set of points where to calculate the complex refractive index.

        Returns:
                The calculated complex refractive index.
        """
        __n = self.refractive_index(window)
        return np.abs((__n-1)/(__n+1))**2


    def plot(self, window):
        """Plots the dielectric function of the model."""

        # Split e1 and e2 in two different y-axis!
        #from http://matplotlib.org/examples/api/two_scales.html
        fig, ax1 = pyplot.subplots()
        ax1.plot(window, np.real(self.dielectric_function(window)), 'g-')
        ax1.set_ylabel(r'$\varepsilon_1$', color = 'g', fontsize = 22)
        ax1.set_xlabel('Energy (eV)')
        ax2 = ax1.twinx()
        ax2.plot(window, np.imag(self.dielectric_function(window)), 'r-')
        ax2.set_ylabel(r'$\varepsilon_2$', color = 'r', fontsize = 22)
        pyplot.title(self.name)
        #pyplot.legend(loc=0)
        pyplot.show()
