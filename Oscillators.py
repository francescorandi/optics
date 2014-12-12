import numpy as np
import scipy

def lorentz(x, x0, gamma, intensity):
	"""Compute complex lorentzian function.
	
	The function is protected against negative unphysical arguments.	
	"""
	x0 = abs(x0)
	gamma = abs(gamma)
	intensity = abs(intensity)
	lor = intensity * np.divide(gamma * x0, pow(x0,2) - pow(x,2) - 1.0j * x * gamma)
	
	return lor

def tauc_lorentz(x, x0, gamma, gap, intensity):
	"""Compute Tauc-Lorentz. It seems that it it still incomplete.
	
	The function is protected against unphysical values of the args.
	"""
	x0 = abs(x0)
	gamma = abs(gamma)
	gap = abs(gap)
	intensity = abs(intensity)

	if x > gap:
		t = intensity 
			* np.divide(1.0, 2.0 * np.pi * nu) 
			* 2.0 * np.pi * x0 * gamma
			* pow((2.0 * np.pi * (nu - gap)),2) 
			* np.divide(1.0, pow(pow(2.0 * np.pi * nu,2) - pow(2.0 * np.pi * x0,2) 
				+ pow(2.0 * np.pi * nu * gamma, 2),2))
	else:
		t = 0.0
	
	return 1.0j * tauc
	
def gauss(x, x0, gamma, intensity): #gamma come definito nella tesi di Fabio
	"""Compute complex gaussian oscillator. Its imaginary part is
	the Dawson function (satisfying the Kramers Kronig relations).
	
	The function is protected against unphysical values of the args.
	"""

	x0 = abs(x0)
	gamma = abs(gamma)
	intensity = abs(intensity)
	gau = 	intensity 
			* (np.exp( -4.0 * log(2) * pow(x-x0,2) / pow(gamma,2)) 
			- np.exp( -4.0 * log(2) * pow(x+x0,2) / pow(gamma,2)))
	daw = 	intensity * 2.0 / sqrt(np.pi) 
			* ( scipy.special.dawsn( 2.0 * sqrt(log(2.0)) * (x+x0) / gamma) 
			- scipy.special.dawsn( 2.0 * sqrt(log(2.0)) * (x-x0) / gamma))
	
	return daw + 1.0j * gau
	
def drude(x, gamma, intensity):
	"""Compute the Drude oscillator.
	The function is protected against unphysical values of the args.
	"""
	gamma = abs(gamma)
	intensity = abs(intensity)
	
	dru = np.divide(-intensity, ( x * (x + 1.0j * gamma)))
		
	return dru
	
def extended_drude(x, fgamma, intensity):
	"""Compute the extended Drude oscillator.
	
	To be implemented."""
	
	return 0.0
	
def epsilon_infinity(value):
	"""Return a constant value for espilon_infinity"""
	
	return value
	
def pole(x, x0, intensity):
	x0 = abs(x0)
	intensity = abs(intensity)
	
	p = np.divide(intensity, pow(x0,2) - pow(x,2))
	
	return p
	
def model(Nu, Oscillator):
	try:
		iter(Nu)
	except TypeError,e:
		Nu = np.array([Nu])
	
	s1 = np.zeros_like(Nu) + 1.0j* np.zeros_like(Nu)
	if type(Oscillator) != list:
		Oscillator = [Oscillator]
		
	for oscillator in Oscillator:
		tipo = oscillator['type']
		if tipo == "lorentz":
			s1 += lorentz(Nu, x0 = oscillator['position'], 
					gamma = oscillator['width'], 
					intensity = oscillator['intensity'])
		elif tipo == "gauss":
			s1 += gauss(Nu, x0 = oscillator['position'],
					gamma = oscillator['width'], 
					intensity = oscillator['intensity'])
		elif tipo == "drude":
			s1 += drude(Nu, gamma = oscillator['width'], 
					intensity = oscillator['intensity'])
		elif tipo == "extended_drude":
			s1 += extended_drude(Nu, fgamma = oscillator['fgamma'], 
					intensity = oscillator['intensity'])
		elif tipo == "tauc_lorentz":
			s1 += tauc_lorentz(Nu, x0 = oscillator['position'], 
					gamma = oscillator['width'], 
					gap = oscillator['gap'], 
					intensity = oscillator['intensity'])
		elif tipo == "epsilon_infinity":
			s1 += epsilon_infinity(value = oscillator['value'])
		elif tipo == "pole":
			s1 += pole(Nu, x0 = oscillator['position'], intensity = oscillator['intensity'])
		
	return s1
	
	
def params2oscillator(Parameters, Type, Constraint=[{}]):
	"""Converts the minimizer-readable list/array of Parameters
	to the storable and human-readable dictionary Oscillator.
	
	Returns Oscillator.
	"""
	
	# In case teh Constraint list of dictionaries comes empty,
	# populate it of the right amount of empty entries to avoid
	# subsequent problems.
	
	if len(Constraint) == 0 and len(Constraint) != len(Type):
		for i in range(len(Type)):
			Constraint.append({})
	
	# Determine the lengths of the slices of the list Parameters 
	# corresponding to each oscillators from the type of the oscillator.
	
	Length = []
	for tipo in Type:
		if tipo == 'gauss' or tipo == 'lorentz':
			length = 3
		elif tipo == 'drude' or tipo == 'extended_drude' or tipo == 'pole':
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
	
	Oscillator = []
	M = len(SplitParameter)
	for m in range(M):
		if Type[m] == 'gauss' or Type[m] == 'lorentz':
			Oscillator.append({'type': Type[m], 
								'position': SplitParameter[m][0],
								'width': SplitParameter[m][1], 
								'intensity': SplitParameter[m][2], 
								'constraints': Constraint[m]})
		elif Type[m] == 'drude':
			Oscillator.append({'type': Type[m], 
								'width': SplitParameter[m][0], 
								'intensity': SplitParameter[m][1], 
								'constraints': Constraint[m]})
		elif Type[m] == 'extended_drude':
			Oscillator.append({'type': Type[m], 
								'fgamma': SplitParameter[m][0], 
								'intensity': SplitParameter[m][1], 
								'constraints': Constraint[m]})
		elif Type[m] == 'tauc_lorentz':
			Oscillator.append({'type': Type[m], 
								'position': SplitParameter[m][0], 
								'width': SplitParameter[m][1], 
								'gap': SplitParameter[m][2], 
								'intensity': SplitParameter[m][3], 
								'constraints': Constraint[m]})
		elif Type[m] == 'epsilon_infinity':
			Oscillator.append({'type': Type[m], 
								'value': SplitParameter[m][0], 
								'constraints': Constraint[m]})
		elif Type[m] == 'pole':
			Oscillator.append({'type': Type[m],
								'position': SplitParameter[m][0], 
								'intensity': SplitParameter[m][1]})
		
	return Oscillator
	
def oscillator2params(Oscillator):
	"""Converts the human-readable Oscillator dictionary to the
	minimizer-readable Parameters array/list.
	
	Returns Parametes, Type, Constraints.
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
		elif oscillator['type'] == 'pole':
			Type.append(oscillator['type'])
			Parameters.append(oscillator['position'])
			Parameters.append(oscillator['intensity'])
		
			
		try:
			Constraints.append(oscillator['constraints'])
		except:
			Constraints.append('')
	
	return Parameters, Type, Constraints
