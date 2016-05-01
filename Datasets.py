# -*- coding: utf-8 -*-
"""
Dataset class.
"""

from numpy import array, loadtxt, savetxt, imag, real, dtype, cfloat
from scipy.constants import physical_constants
from . import relations
import warnings #To be removed?
import h5py
                 
_availableDataTypes = [
    "reflectivity",
    "transmittivity",
    "dielectric function",
    "conductivity",
    "ellipsometric angles",
    "pseudo dielectric function",
    "n k",
]

_relationsToEpsilon = {
    "reflectivity": "reflectivity",
    "transmittivity": "",
    "dielectric function": "identity",
    "conductivity": "conductivity",
    "ellipsometric angles": "",
    "pseudo dielectric function": "",
    "n k": "refractive_index",
}

_availableDataTypesVariants = {
    "reflectivity": 0,
    "R": 0,
    "transmittivity": 1,
    "transmission": 1,
    "dielectric function": 3,
    "dielectricfunction": 3,
    "epsilon": 3,
    "conductivity": 4,
    "sigma": 4,
    "ellipsometric angles": 5,
    "pseudo dielectric function": 6,
    "n k": 7
}

def availableTypes():
    message = "The available dataTypes available are: "
    for element in _availableDataTypes:
        message += element+", "
    print(message)    

class Dataset(object):
    """Base class for datasets. Generic type."""

    def __init__(self, x = None, y = None, name = None, inputFile = None, dataType = None, unitX = "eV", unitY = "Pure", desc = '', **kwargs):
        """ Write some documentation. """
        
        if unitX not in relations.availableEnergyUnits:
            raise relations.NotImplemented("Conversion from "+unitX+" to eV not implemented. \
                Please pass x as either of the following: "+[u for u in relations.availableEnergyUnits])     

        self.type = dataType
        self.unitX = unitX
        self.unitY = unitY
        self.name = name
        
        if inputFile:
            self.loadData(inputFile, unitX = unitX, **kwargs)
        else:
            self.x = array(x, dtype = float)
            self.y = array(y, dtype = cfloat)
            
        if x is not None: self.convertX()

        self.description = desc

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
    def type(self):
        return self._type
        
    @type.setter
    def type(self, dataType):
        if dataType in _availableDataTypesVariants:
            self._type = _availableDataTypes[_availableDataTypesVariants[dataType]]
        else:
            warnings.warn("The specified dataType is not allowed.")            

    def __repr__(self):
        #Find a better representation
        return str(self.x), str(self.y)

    def __str__(self):
        return str(self.type) + ' dataset.\n' + str(self._name)

    def loadData(self, spectraFile, unitX = 'eV', **kwargs):
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
        self.unitX = unitX
        
        if self.unitX is not 'eV':
            self.convertX()
        
    def convertX(self):
        """Converts the x axis to eV at init/loading."""
        if self.unitX is not 'eV':
            try:
                self.x = relations.xtoeV(self.x, self.unitX)
                self.unitX = 'eV'
            except relations.NotImplemented:
                print("Conversion from "+self.unitX+" to eV not implemented.")
                
    def xto(self, unitX):
        """Returns the x axis in the specified units."""
        
        return relations.eVtox(self.x, unitX)
        
    def inputToType(self, data):
        """Function to convert external data calculated on self.x to the data type of this dataset."""
        converted = getattr(relations, _relationsToEpsilon[self.type])(data)
        
        return converted
        

    '''def clone(self, subset = None, scale = None, shift = None, name = None):
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

        return __clone'''

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
    def loadfromjson(self, datafile):
        """Loads json datafile. Includes all metadata."""
        pass

    def loadfromhdf5(self, hdf5):
        """
        Load dataset from hdf5 file. Can be used directly or called
        from a higher level function (e.g. system.load()).
        
        hdf5 can either be the filename or an hdf5 group
        """
        if isinstance(hdf5, str):
            hdf5 = h5py.File(hdf5, "r")
        
        self.x = hdf5['x'][:]
        if hdf5.attrs['dtype'] == 'complex':
            self.y = hdf5['y.real'][:] + 1.0j*hdf5['y.imag'][:]
        if hdf5.attrs['dtype'] == 'real':
            self.y = hdf5['y'][:]
        
        self.name = hdf5.attrs['name']
        self.type = hdf5.attrs['type']
        self.unitX = hdf5.attrs['unitX']
        self.unitY = hdf5.attrs['unitY']
        self.description = hdf5.attrs['description']
        
    
    def savetohdf5(self, hdf5):
        """
        Saves dataset to hdf5 file. Can be used directly or called
        from a higher level function (e.g. system.save()).
        
        hdf5 can either be the filename or an hdf5 group
        """
        if isinstance(hdf5, str):
            hdf5 = h5py.File(hdf5, "w")
        
        hdf5.create_dataset("x", data=self.x)
        
        if isinstance(self.y, cfloat) or isinstance(self.y[0], cfloat):
            hdf5.create_dataset("y.real", data=self.y.real)
            hdf5.create_dataset("y.imag", data=self.y.imag)
            hdf5.attrs['dtype'] = 'complex'
        else:
            hdf5.create_dataset("y", data=self.y)
            hdf5.attrs['dtype'] = 'real'
        hdf5.attrs['name'] = self.name
        hdf5.attrs['type'] = self.type
        hdf5.attrs['unitX'] = self.unitX
        hdf5.attrs['unitY'] = self.unitY
        hdf5.attrs['description'] = (self.description if self.description else '')

    def savetotxt(self, filename, header = None):
        """Exports the dataset as a two column (x,y) text file with header
        optional.

        If the error flag is set to true, a third column with the error will be
        saved.
        """

        savetxt(filename, (self.x, self.y), header = header)
