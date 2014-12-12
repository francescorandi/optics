import numpy as np
import Oscillators

class OpticalModel:
	"""Class to store and handle the oscillator model of the dielectric
	function.
	"""	
	Oscillator = [{}]
	
	def add(self, oscillator):
		"""Add an oscillator to the model.
	
		Parameters:
		oscillator --	should a type be defined? However, there cannot
						be a fully standard set of keys, because there
						are different kinds of functions.
	
		Perform basic checks on the passed oscillator and append it to
		the class attribute.
	
		Returns -- index of the appended oscillator	
		"""
		if ('type' in oscillator.keys()):
			self.Oscillator.append(oscillator)
			index = len(Oscillator)-1
		
			return index
		else:
			raise AssertionError("Please pass a valid oscillator.")
		
	def delete(self, index):
		if index < len(self.Oscillator):
			self.Oscillator.pop(index)
		else:
			raise AssertionError("Index out of range.")
		
		return index
		
	def clear(self):
		self.Oscillator = [{}]
		
	def save(self, filename):
		f = open(filename, 'w')
		json.dump(Oscillator, f)
		f.close()
		
		return True
		
	def get(self, index=None):
		if index = None:
			return self.Oscillator
		else:
			return self.Oscillator[index]
	
	def build_from_parameters(self, Parameter, Type, Constraint):
		self.clear()
		self.Oscillator = self.__params2oscillator(Parameter, Type, Constraint)
		
		return True
	
	def get_parameters(self):
		return self.__oscillator2params(self.Oscillator)		
			
	def dielectric_function(self, Nu, Oscillator):
		"""Calculates the dielectric function from a given
		Oscillator list.
		
		Parameters:
		Nu --			Scalar or list or numpy ndarray of the
						frequency axis to calculate epsilon on.
		Oscillator --	As usual.
		
		Returns:
		eps --			The calculated dielectric function.
						Scalar if the passed Nu was a scalar.
						Numpy ndarray if Nu was a list or ndarray.
		"""
		
		scalarinput = False
		try:
			iter(Nu)
		except TypeError,e:
			Nu = np.array([Nu])
			scalarinput = True
	
		eps = np.zeros_like(Nu) + 1.0j* np.zeros_like(Nu)
		if type(Oscillator) != list:
			Oscillator = [Oscillator]
		
		for oscillator in Oscillator:
			tipo = oscillator['type']
			if tipo == "lorentz":
				eps += lorentz(Nu, x0 = oscillator['position'], 
						gamma = oscillator['width'], 
						intensity = oscillator['intensity'])
			elif tipo == "gauss":
				eps += gauss(Nu, x0 = oscillator['position'],
						gamma = oscillator['width'], 
						intensity = oscillator['intensity'])
			elif tipo == "drude":
				eps += drude(Nu, gamma = oscillator['width'], 
						intensity = oscillator['intensity'])
			elif tipo == "extended_drude":
				eps += extended_drude(Nu, fgamma = oscillator['fgamma'], 
						intensity = oscillator['intensity'])
			elif tipo == "tauc_lorentz":
				eps += tauc_lorentz(Nu, x0 = oscillator['position'], 
						gamma = oscillator['width'], 
						gap = oscillator['gap'], 
						intensity = oscillator['intensity'])
			elif tipo == "epsilon_infinity":
				eps += epsilon_infinity(value = oscillator['value'])
		
		return eps if scalarinput = False else eps[0]
	
	@staticmethod
	def __params2oscillator(Parameter, Type, Constraint):
		"""Converts the minimizer-readable list/array of Parameters
		to the storable and human-readable dictionary Oscillator.
		
		Parameters:
		Parameters -- 	List of minimizer-edible parameters built by
						__oscillator2params().
		Type --			List of error function-edible types built by
						__oscillator2params().
		Constraint --	List of error function-edible constraints
						built by __oscillator2params().
						
		Returns: 
		Oscillator -- 	As usual.
		"""
	
		# In case the Constraint list of dictionaries comes empty,
		# populate it of the right amount of empty entries to avoid
		# subsequent problems.
		# However, this won't happen here in the object.
	
		if len(Constraint) == 0 and len(Constraint) != len(Type):
			for i in range(len(Type)):
				Constraint.append({})
	
		# Determine the lengths of the slices of the list Parameters 
		# corresponding to each oscillators from the type of the oscillator.
	
		Length = []
		for tipo in Type:
			if tipo == 'gauss' or tipo == 'lorentz':
				length = 3
			elif tipo == 'drude' or tipo == 'extended_drude':
				length = 2
			elif tipo == 'tauc_lorentz':
				length = 4
			elif tipo == 'epsilon_infinity':
				length = 1
			Length.append(length)
	
		#Split the list Parameters into slices corresponding to single oscillators.
	
		SplitParameter = []
		position = 0
		for length in Length:
			splitparameter = []
			for i in range(length):
				splitparameter.append(Parameters[position+i])
			SplitParameter.append(splitparameter)
			position += i + 1
	
		# Build the human readable Oscillators list of dictionaries.
	
		Oscillatore = []
		M = len(SplitParameter)
		for m in range(M):
			if Type[m] == 'gauss' or Type[m] == 'lorentz':
				Oscillatore.append({'type': Type[m], 
									'position': SplitParameter[m][0],
									'width': SplitParameter[m][1], 
									'intensity': SplitParameter[m][2], 
									'constraints': Constraint[m]})
			elif Type[m] == 'drude':
				Oscillatore.append({'type': Type[m], 
									'width': SplitParameter[m][0], 
									'intensity': SplitParameter[m][1], 
									'constraints': Constraint[m]})
			elif Type[m] == 'extended_drude':
				Oscillatore.append({'type': Type[m], 
									'fgamma': SplitParameter[m][0], 
									'intensity': SplitParameter[m][1], 
									'constraints': Constraint[m]})
			elif Type[m] == 'tauc_lorentz':
				Oscillatore.append({'type': Type[m], 
									'position': SplitParameter[m][0], 
									'width': SplitParameter[m][1], 
									'gap': SplitParameter[m][2], 
									'intensity': SplitParameter[m][3], 
									'constraints': Constraint[m]})
			elif Type[m] == 'epsilon_infinity':
				Oscillatore.append({'type': Type[m], 
									'value': SplitParameter[m][0], 
									'constraints': Constraint[m]})
		
		return Oscillatore
	
	@staticmethod
	def __oscillator2params(Oscillator):
		"""Converts the human-readable Oscillator dictionary to the
		minimizer-readable Parameters array/list.
		
		Parameters:
		Oscillator -- A general one, not the object attribute.
	
		Returns:
		Parametes --	List to be passed to the minimizer for the fit.
		Type -- 		List of types of the original Oscillator. It 
						is needed (also by the error function) to 
						reconstruct it from the Parameters list.
		Constraints --	List of the constraints of the original 
						Oscillator. It is needed by the error function.	
		"""

		Parameters = []
		Type = []
		Constraints = []
		for oscillator in Oscillator:
			if oscillator['type'] == 'gauss' or oscillator['type'] == 'lorentz':
				Type.append(oscillator['type'])
				Parameters.append(oscillator['position'])
				Parameters.append(oscillator['width'])
				Parameters.append(oscillator['intensity'])
			elif oscillator['type'] == 'drude':
				Type.append(oscillator['type'])
				Parameters.append(oscillator['width'])
				Parameters.append(oscillator['intensity'])
			elif oscillator['type'] == 'tauc_lorentz':
				Type.append(oscillator['type'])
				Parameters.append(oscillator['position'])
				Parameters.append(oscillator['width'])
				Parameters.append(oscillator['gap'])
				Parameters.append(oscillator['intensity'])
			elif oscillator['type'] == 'epsilon_infinity':
				Type.append(oscillator['type'])
				Parameters.append(oscillator['value'])
		
			
			try:
				Constraints.append(oscillator['constraints'])
			except:
				Constraints.append('')
	
		return Parameters, Type, Constraints
