# -*- coding: utf-8 -*-
"""
Dataset class.
"""
import matplotlib.pyplot as pyplot

from numpy import array, loadtxt, savetxt, imag, real, dtype
from scipy.constants import physical_constants

energyUnits = ('eV', 'cm-1', 'THz') #List of energy units available

__wavelength = 'electron volt-inverse meter relationship'
__herz = 'electron volt-hertz relationship'

unitTransform = {'cm-1': physical_constants[__wavelength][0]/100,
                 'THz': physical_constants[__herz][0]/10**12,
                 'eV': 1}

class Dataset():
    """Base class for datasets. Generic type."""

    __counter = 0

    def __init__(self, x = None, y = None, name = None, inputFile = None, unit = "eV", desc = None):
        """ Write some documentation. """

        type(self).__counter += 1

        self.type = "Generic"
        self.unit = unit

        if name:
            self._name = name
        else:
            self._name = "Dataset %d" % self.__counter

        if inputFile:
            self.loadRaw(inputFile, unit)

        else:
            self.x = array(x, dtype = float)
            self.y = array(y, dtype = float)

        self.description = desc

    def __del__(self):
        type(self).__counter -= 1

    # How to use decorators to define "setters" and "getters"
    # http://www.python-course.eu/python3_properties.php
    # https://docs.python.org/3/library/functions.html#property
    # Maybe this use is a bit too trivial to need a setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def desc(self):
        return self.name

    @desc.setter
    def desc(self, string):
         self._desc = string

    def __repr__(self):
        #Find a better representation
        return str(self.x), str(self.y)

    def __str__(self):
        return self.type + ' dataset.\n' + str(self._name)

    def loadRaw(self, spectraFile, unit = 'eV', **kwargs):
        """
        Loads the data from a textfile.

        If there is an error column, use the flag 'error = True'

        Parameters:

            unit: Defines the energy unit of the imported data.
            Automatic transformation to eV possible for units listed
            in the list energyUnits.

            Also possible to use any other argument defined in numpy.loadtxt()
            (see numpy documentation).
        """

        self.x, self.y = loadtxt(spectraFile, unpack = True, *kwargs)

        if unit is not 'eV':
            self.x /= unitTransform[unit]

    def clone(self, subset = None, scale = None, shift = None, name = None):
        """Clones/duplicates the dataset."""

        #Would it be better to use deepcopy implementing a __deepcopy__ method?
        __clone = Dataset(self.x, self.y)

        if scale:
            __clone.scale(scale)

        if shift:
            __clone.shift(shift)

        if subset:
            __clone.subset(*subset)

        if name:
            __clone.name = name
        else:
            name = "clone of %s" % self.name

        #How to deal with the clone afterwards?
        #As it is, it cannot be accessed from the originating instance because
        #of the __, but it seems that the daugher instance still lives inside
        #the parent instance which is a memory issue.
        #Maybe this will be reason enough to go for __deepcopy__ method which
        #also could be used to copy all metadata.

        return __clone

    def subset(self, window, stride = 1):
        """Takes a subset of the data available."""

        __index = range(len(self.x))
        # Returning the index position with the smalles "distance" (min)
        # between the available data and the requested boundary

        __lIndex = min(__index, key=lambda i: abs(self.x[i]-window[0]))
        __hIndex = min(__index, key=lambda i: abs(self.x[i]-window[1]))

        self.x = self.x[__lIndex:__hIndex:stride]
        self.y = self.y[__lIndex:__hIndex:stride]

    def scale(self, factor):
        self.y *= factor

    def shift(self, shift):
        """Shifts the spectra by an specified amount in energy."""
        self.x += shift

    # Not sure if load and save belong here or to a "higher" level component
    def load(self, datafile):
        """Loads json datafile. Includes all metadata."""
        pass

    def save(self, filename):
        """Saves dataset """
        pass

    def export(self, filename, header = None):
        """Exports the dataset as a two column (x,y) text file with header
        optional.

        If the error flag is set to true, a third column with the error will be
        saved.
        """

        savetxt(filename, (self.x, self.y), header = header)

    def plot(self):
        """Plots the data contained in the dataset."""

        pyplot.plot(self.x, self.y, label = self.name)
        if self.unit is "eV":
            pyplot.xlabel("Energy [eV]", fontsize = 18)
        elif self.unit is "cm-1":
            pyplot.xlabel("Wavenumber [cm-1]", fontsize = 18)

        if self.name:
            pyplot.title(self.name, fontsize = 18)

class ReflectivityDataset(Dataset):
    """Reflectivity oriented dataset container."""

    def __init__(self, inputFile = None, unit = "eV", name = None):
        super().__init__(inputFile = inputFile, unit = unit, name= name)
        self.type = "Reflectivity"

    def plot(self):
        super().plot()
        pyplot.ylabel("Reflectivity")



class TransmissionDataset(Dataset):
    """Reflectivity oriented dataset container."""

    def __init__(self, inputFile = None, unit = "eV", name = None):
        super().__init__(inputFile = inputFile, unit = unit, name= name)
        self.type = "Transmission"

class DielectricFunctionDataset(Dataset):

    def __init__(self, x = None, y = None, name = None, inputFile = None, unit = "eV"):
        """ Some documentation. """

        self.type = "Dielectric function"

        if inputFile:
            self.loadRaw(inputFile, unit)

        else:
            self.x = array(x, dtype = float)
            self.y = array(y, dtype = complex)

        self._name = name

    def loadRaw(self, spectraFile, unit = 'eV'):
        """
        Loads the dielectric function values from a textfile.

        unit: One of the units defined in the list energyUnits. It will
        transform it into electronvolts (eV).
        """

        # How to deal with files with a header?
        # This code is very much like the parent one, how can it be better
        # factorized?

        self.x, self._y1, self._y2 = loadtxt(spectraFile, unpack = True)

        self.y = self._y1+1j*self._y2

        if unit is not 'eV':
            self.x /= unitTransform[unit]

    def scale(self):
        print("It makes no sense to scale a dielectric function dataset!\n\
            try another operation")

    def plot(self):
        """Plots the data contained in the dataset."""
        pyplot.plot(self.x, real(self.y), label = self.name)
        pyplot.plot(self.x, imag(self.y), label = self.name)

class EllipsometryDataset(Dataset):
    """Ellipsometry oriented dataset container. Built as a pair of general
    datasets, one for each value."""

    ellipTypes = ("ellipsometric angles", "pseudo dielectrc function", "n\&k")

    def __init__(self, ellipType):
        super().__init__()
        self.type = "Ellipsometry"
        self.ellipType = ellipType

    def loadRaw(self, spectraFile):
        x, y1, y2 = loadtxt(spectraFile, unpack = True)
        self.d = (Dataset(x, y1), Dataset(x, y2))


if __name__ == "__main__":

    #import matplotlib.pyplot as pyplot

    def plotWindow(*datasets):
        """
        Plots the loaded spectra for visual inspection. Takes one or many
        datasets and plots them in the same window.
        """

        pyplot.figure("Loaded spectra")

        for dataset in datasets:

            if dataset.y.dtype is dtype(complex):
                pyplot.plot(dataset.x, real(dataset.y), label = dataset.name)
                pyplot.plot(dataset.x, imag(dataset.y), label = dataset.name)

            else:
                pyplot.plot(dataset.x, dataset.y, label = dataset.name)

        pyplot.legend(loc=0)
        pyplot.show()
