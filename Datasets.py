# -*- coding: utf-8 -*-
"""
Dataset class.
"""

from numpy import array, loadtxt, savetxt
from scipy.constants import physical_constants

energyUnits = ('eV', 'cm-1', 'THz') #List of energy units available

__wavelength = 'electron volt-inverse meter relationship'
__herz = 'electron volt-hertz relationship'

unitTransform = {'cm-1': physical_constants[__wavelength][0]/100,
                 'THz': physical_constants[__herz][0]/10**12,
                 'eV': 1}

class Dataset(object):
    """Base class for datasets. Generic type."""    
    
    def __init__(self, x = None, y = None, name = None):
        self.type = "Generic"
        self.x = array(x, dtype = float)
        self.y = array(y, dtype = float)
        self._name = name
    
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
        
    def __repr__(self):
        #Find a better representation

        return str(self.x), str(self.y)
        
    def __str__(self):
        return self.type+ ' dataset.\n'+ str(self._name)
        
    def loadRaw(self, spectraFile, error = False, unit = 'eV'):
        """
        Loads the data from a textfile.
        
        If there is an error column, use the flag 'error = True'
        
        unit: One of the units defined in the list energyUnits. It will 
        transform it into eV.
        """
        
        if error:
            self.x, self.y, self.y_err = loadtxt(spectraFile, unpack = True)
            self.y_err = array(self.y_err, dtype = float)
            
        else:
            self.x, self.y = loadtxt(spectraFile, unpack = True)
            
        self.x = array(self.x, dtype = float)
        self.y = array(self.y, dtype = float)
        
        if unit is not 'eV':
            self.y /= unitTransform[unit]
        
    def clone(self, subset = None, scale = None, shift = None):
        """Clones/duplicates the dataset."""
        
        #Would it be better to use deepcopy implementing a __deepcopy__ method?
        __clone = Dataset(self.x, self.y)
        
        if scale:
            __clone.scale(scale)
            
        if shift:
            __clone.shift(shift)
            
        if subset:
            __clone.subset(*subset)
        
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
        self.x -= shift
    
    # Not sure if load and save belong here or to a "higher" level component
    def load(self, datafile):
        """Loads json datafile. Includes all metadata."""
        pass
    
    def save(self, filename):
        """Saves dataset """
        pass
    
    def export(self, filename, error = False, header = None):
        """Exports the dataset as a two column (x,y) text file with header 
        optional.
        
        If the error flag is set to true, a third column with the error will be
        saved.
        """
        
        # How to deal with the case of the flag on but no error array?
        # 1) Error array set to 0, this can be a) permanently, b) at the time of
        # export
        # 2) Not write a third column and neglect the flag by ussing an 'and'
        # operator in the if statement ingluding teh existence of y_err
        
        if error:
            savetxt(filename, (self.x, self.y, self.y_err), header = header)
            
        else:
            savetxt(filename, (self.x, self.y), header = header)   
            
class ReflectivityDataset(Dataset):
    """Reflectivity oriented dataset container."""
    
    def __init__(self):
        super().__init__()
        self.type = "Reflectivity"
        
    def loadRaw(self, spectraFile):
        super().loadRaw(spectraFile)
        
class TransmissionDataset(Dataset):
    """Reflectivity oriented dataset container."""

    def __init__(self):
        super().__init__()
        self.type = "Transmission"
        
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
    
    import matplotlib.pyplot as pyplot

    
    def plotWindow(*datasets):
        """
        Plots the loaded spectra for visual inspection. Takes one or many 
        datasets and plots them in the same window.
        """
        
        pyplot.figure("Loaded spectra")
        
        for dataset in datasets:
            pyplot.plot(dataset.x, dataset.y, label = dataset.name)
        
        pyplot.legend(loc=0)
        pyplot.show()