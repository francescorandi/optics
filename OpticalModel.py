import numpy as np
import matplotlib.pyplot as pyplot

import json

from Oscillators import *

OscillatorsList = ("Drude", "Lorentz", "Gauss")

class OpticalModel:
    """Class to store and handle the oscillator model of the dielectric
    function.
    """
    
    def __init__(self, name):
        """Optical model built from a collection of oscillators."""
        
        self.name = name
        self.oscillators = []
    
    def __str__(self):
        pass
    
    def show(self):
        """Prints the collection of oscillators composing the model."""
        print("Index\t Oscillator name")
        print("========================")
        for index, oscillator in enumerate(self.oscillators):
            print("\t".join([str(index), oscillator.Name]))
    
    def add(self, *oscillators):
        """Add an oscillator to the model.
        
        Parameters:
        oscillators: a collection of oscillator objects
        
        Returns -- index list of the appended oscillators
        """
        
        # I don't see the need to return the index
        _index = []
        
        for oscillator in oscillators:
            self.oscillators.append(oscillator)
            _index.append(len(self.oscillators)-1)
            
        return _index

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