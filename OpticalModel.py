import numpy as np
import matplotlib.pyplot as pyplot

import json

class OpticalModel(object):
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

    def __add__(self, other):
        _tmp = []
        _tmp.append(self.oscillators)
        _tmp.append(other.oscillators)
        return OpticalModel(oscillators = _tmp)

    def __iadd__(self, other):
        self.oscillators.append(other.oscillators)
        return self

    def __radd__(self, other):
        if type(other) is list:
            self.addCollection(other)
        else:
            self.add(other)
            
        return self

    def __len__(self):
        return len(self.oscillators)

    def show(self):
        """Prints the collection of oscillators composing the model."""
        print("Index\t Oscillator name")
        print("========================")
        for index, oscillator in enumerate(self.oscillators):
            print("\t".join([str(index), type(oscillator).__init__name__]))

    def add(self, *oscillator):
        """Add one or more oscillators to the model.

        Parameters:
        oscillator: an oscillator object
        """

        self.oscillators.append(oscillator)

    def addCollection(self, oscillators):
       """Adds oscillators in an collection (iterable)."""

       for osc in oscillators:
           self.add(osc)

    def delete(self, index):
        """Removes an oscillator give by its index."""

        try:
            self.oscillators.pop(index)
        except IndexError:
            print("Index out of range")

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
        """Calculates the dielectric of the model.

        Parameter:
        window -- Set of points where to calculate the dielectric funtion

        Returns:
        		The calculated dielectric function.

        """

        _eps = np.zeros(len(window), dtype = complex)

        for oscillator in self.oscillators:
            _eps += oscillator.dielectricFunction(window)

        return _eps

    def plot(self, window):
        """Plots the dielectric function of the model."""

        # Split e1 and e2 in two different y-axis!
        pyplot.plot(window, np.real(self.dielectric_function(window)), label = "e1")
        pyplot.plot(window, np.imag(self.dielectric_function(window)), label = "e2")
        pyplot.legend(loc=0)
        pyplot.show()
