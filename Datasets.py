# -*- coding: utf-8 -*-
"""
Dataset class.
"""

from numpy import array, loadtxt, savetxt
from scipy.constants import physical_constants

class Dataset(object):
    """Base class for datasets. Generic type."""
    
    energyUnits = ('eV', 'cm-1') #List of energy units
    
    def __init__(self, x = None, y = None, name = None):
        self.type = "Generic"
        self.x = array(x)
        self.y = array(y)
        self.name = name
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
        
    def __repr__(self):
        return str(self.x), str(self.y)
        
    def loadRaw(self, spectraFile):
        self.x, self.y = loadtxt(spectraFile, unpack = True)
        self.x = array(self.x)
        self.y = array(self.y)
        
    def load(self, datafile):
        """Loads json datafile. Includes all metadata."""
        pass
    
    def save(self, filename):
        """Saves dataset """
        pass
    
    def export(self, filename, header = None):
        """Exports the dataset as a two column (x,y) text file with header 
        optional.
        """
        
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