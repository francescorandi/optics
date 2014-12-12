import numpy as np
import scipy
import json
import KramersKronig as kk
import Oscillators
import OpticalModel

class OpticalSystem:
	
	__Oscillator = OpticalModel()
	__GuessOscillator = OpticalModel()
	__FittedOscillator = OpticalModel()
	
	__SourceData = [{}]
	
	__Frequency = []
	__Epsilon = []
	
	__Logger = [""]
	
	# Conversion of units. Everything stored in terahertz and SI.
	# The conversion is SI = value * key
	# The choice of terahertz instead of hertz helps the minimizers used in the 
	# fitting procedures avoiding huge numbers for the usual frequency ranges.
	__conversionsX = {'eV': 241.79893, 'nm': 299792.458, 'um': 299.792458, 'cm-1': 0.02998}
	__conversionsY = {'default' = 1.0}
	
	def __init__(self):
		"""Initialize the OpticalSystem"""
	
	def add_data(self, X, Y, XUnit=None, YUnit=None, YType=None, YPart=None, Priority=0):
		#for every new entry, the reflectivity must be calculated from all the old ones,
		#appended to the new entry and everything must be transformed back to epsilon
		
		#add_data saves also the entry in a variable just keeping them together
		#once all are added, if there is at least one reflectivity without
		#the phase, all the sigmas and epsilons are used to calculate the reflectivity,
		#everything is put together and then kramers kroniged to epsilon
		
		
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
		
		if type(XUnit) == str and XUnit == in self.__conversionsX.keys():
			X = np.array(X)*self.__conversionsX[XUnit]
		elif type(XUnit) != str :
			X = np.array(X)*XUnit
		elif XUnit == None:
			X = np.array(X)
			message = "Assuming X is Frequency in terahertz."
			Message.append(message)
			raise Warning(message)
		else:
			raise AssertionError("I was not able to perform the conversion of the X.")

		if type(YUnit) == str and YUnit in self.__conversionsY.keys():
			Y = np.array(Y)*self.__conversionsY[YUnit]
		elif type(YUnit) != str :
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
		
		[sY, sX] = zip(*sorted(zip(X, Y)))
		X = np.array(sX)
		Y = np.array(sY)
		
		if YType == 'DielectricFunction' and fullcomplex:
			self.__SourceData.append({"Type": 'DielectricFunction', "Part": "Full", 'X': X, 'Y': Y})
		elif YType == 'DielectricFunction' and YType == None:
			self.__SourceData.append({'Type': 'DielectricFunction', 'Part': "Real", "X": X, "Y": Y})
			message = "Assuming that the data is the real part of "+
				"the dielectric function. If not, delete the "+
				"oscillator and specify YPart=\"Imag\"."
			Message.append(messagge)
			raise Warning(message)
		elif YType == 'DielectricFunction' and YType == "Imag":
			self.__SourceData.append({'Type': 'DielectricFunction', "Part": "Imag", 'X': X, 'Y': Y})
		
		# Last thing, to be done for each valid entry: set the
		# priority. This will be used when matching boundary values
		self.__SourceData[-1]['Priority'] = Priority
		
		# If you survived up to now, process the Logger prefixing to
		# the messages the __SourceData current index.
		index = len(self.__SourceData) - 1
		for message in Message:
			self.__Logger.append("SourceData "+str(index).zfill(2)+": "+message)
			
		return True
	
	def build_optical_properties(self):
		#add_data saves also the entry in a variable just keeping them together
		#once all are added, if there is at least one reflectivity without
		#the phase, all the sigmas and epsilons are used to calculate the reflectivity,
		#everything is put together and then kramers kroniged to epsilon
		
		# There is one final array of epsilon data to be stored and the interpolated
		# when called.
		
		# When this function is called, compute the lower and upper bound for which
		# the reflectivity is done, to be able then to call the extrapolation functions
		# for the kramers kronig. Maybe also intervals in between to data sets..
		
		# Check whether they are all full (Re+iIm) dielectric functions.
		# In case they are, easy go.
		allepsilon = True
		allfull = True
		for data in self.__SourceData:
			allepsilon = (data['Type']=='DielectricFunction')
			allfull = (data['Part']=='Full')
		if allepsilon: self.__Logger.append("I discovered that all the source data sets"+
			" are dielectric functions.") 
		if allepsilon and not allfull: self.__Logger.append("However, not all the "+
			"real and imaginary parts of the dielectric functions were given.") 
		
		# If they are all dielectric functions
		if allepsilon:
			if not allfull:
				# What to implement? KK on the single data sets?
				# Once KKed, save it to the same __SourceData element,
				# but find a way of lowering the priority of the KKed
				# for the  matching.
				raise NotImplementedError("I should perform the kramers "+
					"kronig to get the full complex numbers.")
					
			Frequency = np.zeros(0)
			Epsilon = np.zeros(0)
			# Should be implemented: matching of boundary values. LOL.
			# The best thing will be to implement a function that does this on
			# homogeneous data. Use Priority in __SourceData to take decisions.
			# This function should maybe also deform the data to preserve
			# analyticity at the matching points.
			# When reflectivity and epsilon have to be matched
			# then take epsilon at the boundary, calculate the would be R(epsilon)
			# and then match.
			for data in self.__SourceData:
				np.concatenate(Frequency,data['X'])
				np.concatenate(Epsilon,data['Y'])
			[sEpsilon, sFrequency] = zip(*sorted(zip(Frequency, Epsilon)))
			self.__Frequency = np.array(sFrequency)
			self.__Epsilon = np.array(sEpsilon)
			
			self.__Logger.append("I successfully built the unified set.")
			
			return True
		
		# Check whether they all are either dielectric functions or
		# conductivities.
		allepsorsigma = True
		for data in self.__SourceData:
			if (data['Type']=='DielectricFunction') or (data['Type']=='Conductivity'):
				allepsorsigma = 
		self.__Logger.append("I discovered that all the source data sets"+
				" are dielectric functions.") 
		
		
		return True
		
	def reflectivity_extrapolation_lower(self):
		return 0.0
	
	def reflectivity_extrapolation_upper(self):
		return 0.0
	
	def save(self, filename):
		"""Dump everything into a json file so that the object can be
		rebuilt without the processing
		"""
		
	def load(self, filename):
		"""Load everything from a json file"""
	
	def epsilon(self):
		"""This is the main interpolator of the stored epsilon"""
		
		return 0.0
	
	# These could be moved to a module containing optical relations,
	# including more complicated things.
	def get_reflectivity(self, axis):
		N = sqrt(self.epsilon(axis))
		r = (N - 1.0)/(N + 1.0)
		R = pow(abs(r),2)
		
		return R
	
	def get_epsilon(self, axis):
		return self.epsilon(axis)
		
	def get_epsilon_real(self, axis):
		return self.epsilon(axis).real
	
	def get_epsilon_imag(self, axis):
		return self.epsilon(axis).imag
		
	def get_sigma(self, axis):
		# Calculate it everytime, there's no need to contain 
		# computational effort that much.
		return 0.0
		
	def get_sigma_real(self, axis):
		# Calculate it everytime, there's no need to contain 
		# computational effort that much.
		return 0.0
	
	def get_sigma_imag(self, axis):
		# Calculate it everytime, there's no need to contain 
		# computational effort that much.
		return 0.0
		
	# Methods related to the fit of the dielectric function or 
	# of the reflectivity
	
	def set_guess_oscillator(self, Oscillator):
		try:
			iter(Oscillator)
		else:
			Oscillator = np.array(Oscillator)
		
		self.GuessOscillator.clear()
		for oscillator in Oscillator:
			self.GuessOscillator.add_oscillator(oscillator)
		
		return True
	
	def add_guess_oscillator(self, Oscillator):
		try:
			iter(Oscillator)
		else:
			Oscillator = np.array(Oscillator)
		
		for oscillator in Oscillator:
			self.GuessOscillator.add_oscillator(oscillator)
		
		return True
		
	def get_guess_oscillator(self, index=None):
		if index = None:
			return self.GuessOscillator
		else:
			return self.GuessOscillator[index]
	
	def get_fitted_oscillator(self, index=None):
		if index = None:
			return self.FitterOscillator		
		else:
			return self.FittedOscillator[index]
		
	def fit_is_ok(self):
		"""If the fit was ok, deepcopy the FittedOscillator	to 
		Oscillator.
		"""
		self.Oscillator = self.FittedOscillator[:]
		return True	
	
	@staticmethod
	def __fit_error(Parameters, Type, Constraints, data, axis,
			finalfunction=self.get_epsilon):
				  
		osc = OpticalModel.__params2oscillator(Parameters, Type, Constraints)
		eps = OpticalModel.__dielectricfunction(axis,Oscillator)
		processed = finalfunction(eps)
		
		e = 0.0
		e += sum(pow(abs(processed - data),2))
		#Implement constraints here

		return e
	
	def fit_do(self, axis=None, tobefitted='DielectricFuction', verbose=False):
		if tobefitted = 'DielectricFunction':
			ftransform = self.get_epsilon
		elif tobefitted = 'Refelctivity':
			ftransform = self.get_reflectivity
		
		if axis == None:
			axis = self.__Frequency
			
		Parametri, Tipi, Constraints = GuessModel.get_parameters()
		Risultato = optimize.minimize(self.__fit_error, 
			method="Powell", 
			x0=Parametri, 
			args=(Tipi, Constraints, ftransform(), axis), 
			jac=False)
		self.FittedOscillator = OpticalModel.__params2oscillator(
			Risultato['x'], Tipi, Constraints)
		
		return True if verbose = False else self.FittedOscillator 
