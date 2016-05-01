import numpy as np
from scipy.optimize import minimize
from . import OpticalModel as OpticalModel
from . import Datasets as Datasets
from . import Oscillators as Oscillators
import h5py

import matplotlib.pyplot as pyplot

class OpticalSystem:
           
    def __init__(self):
        """Initialize the OpticalSystem"""

        self.datasets = [] # List containing the imported datasets 
        self.models = [] # List containing the built optical models
        self.logger = ""
    
    def save(self, filename):
        """Save everything to an hdf5 file"""
        f = h5py.File(filename, "w")
        #Specify in the metadata that it contains a system
        f.attrs['type'] = 'optics system'
        
        #Save models
        h5models = f.create_group("models")
        for model in self.models:
            h5model = h5models.create_group(model.name)
            model.savetohdf5(h5model)
                
        #Save datasets
        h5datasets = f.create_group("datasets")
        for i, dataset in enumerate(self.datasets):
            h5dataset = h5datasets.create_group(str(i))
            dataset.savetohdf5(h5dataset)
        f.close()
        
    def load(self, filename):
        """Load everything from an hdf5 file"""
        f = h5py.File(filename, "r")
        assert (f.attrs['type']=='optics system'), "This file does not contain a optics system"
        
        for name, h5model in f['models'].items():
            om = self.createModel(name)
            om.loadfromhdf5(h5model)
                
        #Load datasets
        for i, hd5dataset in f['datasets'].items():
            dset = Datasets.Dataset()
            dset.loadfromhdf5(hd5dataset)
            self.datasets.append(dset)
        
        f.close()
    
    def createModel(self, name = None):
        """Creates an optical model with a given name. Name is optional."""
        if name:
            om = OpticalModel.OpticalModel(name)
            self.models.append(om)
        else:
            om = OpticalModel.OpticalModel()
            self.models.append(om)
        return om
        
    def listModels(self):
        """List the optical models"""
        for o in self.models:
            print(o.name)
        
    def plotModel(self, opticalmodel, window, step = 0.01):
        """Plots a given optical model.
        
        Implementing only dielectric function"""
        p = plt.figure() # check figure extra parameters
        _window = arange(window[0], window[1], step = step)
        p.plot(_window, opticalmodel.dielectric_function(_window))
        
    def addData(self, x = None, y = None, name = None, inputFile = None, dataType = None, unitX = "eV", unitY = "Pure", desc = None, **kwargs):
        self.datasets.append(Datasets.Dataset(x, y, name, inputFile, dataType, unitX, unitY, desc))
        
        return self.datasets[-1]
    
    '''def add_data(self, X, Y, XUnit=None, YUnit=None, YType=None, YPart=None, Priority=0):
        """Add optical data
        
        1st argument: Frequency/Energy/Wavelength axis of the optical
        data used to initialize the OpticalSystem
        
        2nd argument: Units of the first argument. Should be either a
        string among 'eV' (for electronvolts), 'nm' (for nanometers), 
        'um' (for micrometers), 'cm-1' (for centimeters to the minus
        one), or a float for the direct conversion to terahertz
        (terahertz = argument * unit of given axis)
        
        3rd argument: Data to be loaded. It can be: reflectivity,
        dielectric function, conductivity. In the last two cases it can
        be either the full quantity or just the real or imaginary part.
        The full quantity can be either passed as a complex number
        or as a 2D-list or array.
        
        4th argument: Pass conversion to SI unit as a float. Conversions
        will be implemented.
        
        5th argument: In the future, the code will try to identify the 
        type (reflectivity, dielectric function, conductivity) of the
        loaded data. But for now pass the data type as: 'R' for
        reflectivity, 'E' for dielectric constant, 'S' for conductivity
        """
        Message = []
        
        if type(XUnit) == str and XUnit == int(self.__conversionsX.keys()):
            X = np.array(X)*self.__conversionsX[XUnit]
        elif XUnit == None:
            X = np.array(X)
            message = "Assuming X is Frequency in terahertz."
            Message.append(message)
            raise Warning(message)
        elif type(XUnit) == float or type(XUnit) == int :
            X = np.array(X)*XUnit
        else:
            raise AssertionError("I was not able to perform the conversion of the X.")

        if type(YUnit) == str and YUnit in self.__conversionsY.keys():
            Y = np.array(Y)*self.__conversionsY[YUnit]
        elif type(YUnit) == float or type(YUnit) == int:
            Y = np.array(Y)*YUnit
        elif YType == 'DielectricFunction' or YType == 'Reflectivity':
            Y = np.array(Y)
        elif YType == 'Conductivity':
            Y = np.array(Y)
            message = "Assuming Y data is "+YType+" in ohm m-1."
            Message.append(message)
            raise Warning(message)
        else:
            raise AssertionError("I was not able to determine what kind of data Y is. "+
                "I am not saving it.")
        
        fullcomplex = False
        if type(Y[0]) == complex:
            fullcomplex = True
        
        # If the input is a two-dimensional array (and it is not 2d
        # just because of only two entries), then it is understood to
        # be of the type [Y.real, Y.imag] and converted to a single
        # dimensional array of the type [Y.real+iY.imag].
        if len(Y) == 2 and (type(Y[0]) != float or type(Y[0]) != complex):
            Y = Y[0] + 1.0j*Y[1]
            fullcomplex = True
        
        #CREATE DATASET OBJECTS
        if YType == 'DielectricFunction' and fullcomplex:
            #self.__SourceData.append({"Type": 'DielectricFunction', "Part": "Full", 'X': X, 'Y': Y})
        elif YType == 'DielectricFunction' and YPart == None:
            #self.__SourceData.append({'Type': 'DielectricFunction', 'Part': "Real", "X": X, "Y": Y})
            message = "Assuming that the data is the real part of "+\
                "the dielectric function. If not, delete the "+\
                "oscillator and specify YPart=\"Imag\"."
            Message.append(messagge)
            raise Warning(message)
        elif YType == 'DielectricFunction' and YType == "Imag":
            #self.__SourceData.append({'Type': 'DielectricFunction', "Part": "Imag", 'X': X, 'Y': Y})
        
        # Last thing, to be done for each valid entry: set the
        # priority. This will be used when matching boundary values
        #self.__SourceData[-1]['Priority'] = Priority
        
        # If you survived up to now, process the Logger prefixing to
        # the messages the __SourceData current index.
        index = len(self.__SourceData) - 1
        for message in Message:
            self.__Logger.append("SourceData "+str(index).zfill(2)+": "+message)
            
        return True'''
    
    #move the following two to the dataset    
    def reflectivity_extrapolation_lower(self):
        return 0.0
    
    def reflectivity_extrapolation_upper(self):
        return 0.0
    
        
    """
    Methods related to the fits
    """  
    
    @staticmethod
    def __fit_error(params, model, datasets):
        
        e = 0.0
        model.params = params
        for dataset in datasets:
            epsilon = model.dielectric_function(dataset.x)
            processed = dataset.inputToType(epsilon)
            e += np.sum(np.power(np.absolute(processed - dataset.y),2))
        
        #Constraints (should be contained in the model)

        return e
    
    def fit(self, model, datasets=None, verbose=True):
        if datasets==None:
            dsets = self.datasets
        elif isinstance(datasets, Datasets.Dataset):
            dsets = [datasets]
        elif isinstance(datasets[0], Datasets.Dataset):
            dsets = datasets
        elif isinstance(datasets[0], int):
            dsets = []
            for i in datasets:
                dsets.append(self.datasets[i])
        
        parameters = model.params
        print(parameters)
        Result = minimize(self.__fit_error, 
            x0=parameters,
            method="Powell",
            args=(model, dsets), 
            jac=False)
        
        return True if verbose == False else model.show()
