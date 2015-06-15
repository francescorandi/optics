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

	PI2 = np.pi*2
	
	if x > gap:
		t = intensity * np.divide(1.0, PI2 * nu) * PI2 * x0 * gamma	* pow((PI2 * (nu - gap)),2) * np.divide(1.0, pow(pow(PI2 * nu,2) - pow(PI2 * x0,2) + pow(PI2 * nu * gamma, 2),2))
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
