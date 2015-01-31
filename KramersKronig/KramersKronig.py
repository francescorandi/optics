import numpy as np
from scipy import integrate

def real2imag(f, axis, a, b):
	"""Compute the imaginary part g of a causal function of the form
	f + ig given its real part f.
	
	Arguments:
	f: callable real part (hint, use interp1d)
	axis: where g will be calculated
	a: lower integration limit
	b: upper integration limit
	
	Returns g as numpy ndarray calculated on axis.
	"""
	I = len(axis)
	g = np.zeros(I)
	
	for i in range(I):
		nu0 = axis[i]		
		result, error = integrate.quad(real2imag_integrand, a=a, b=b,
										args=(nu0, f), epsrel = 1.0e-5)
		g[i] += nu0*result
	
	g *= -2.0 / np.pi
	
	return g
	
def real2imag_integrand(nu, nu0, f):
	y = (f(nu) - f(nu0))/(pow(nu,2) - pow(nu0,2))
	
	return y
	
# Still missing imag2real. To be coded.

def mod2phase(f, axis, a, b):
	"""Compute the imaginary part g of a causal function of the form
	log(f) + ig given f.
	
	Arguments:
	f: callable real part (hint, use interp1d)
	axis: where g will be calculated
	a: lower integration limit
	b: upper integration limit
	
	Returns g as numpy ndarray calculated on axis.
	"""
	
	I = len(axis)
	g = np.zeros(I)
	
	for i in range(I):
		nu0 = axis[i]
		result, error = integrate.quad(mod2phase_integrand, a=a, b=b,
										args=(nu0, f), epsrel=1.0e-5)
		g[i] += nu0*result
		
	g /= np.pi
	
def mod2phase_integrand(nu, nu0, f):
	y = np.log(f(nu) / f(nu0)) / (pow(nu0,2) - pow(nu,2))
	
	return y
	
def mod2phase_high_energy_simple(nu, nua, nub, Rnu, Rnua, s, N=10):
	"""High energy contributions. See Wooten's book, Appendix G."""
	y = 0.0
	nnua = nu/nua
	nnub = nu/nub
	fourms = 4.0 - s
	for n in np.arange(N):
		y += (s * pow(nnua,2*n+1) + fourms * pow(nnub, 2*n+1)) / pow(2*n + 1, 2)
	y *= np.pi
	y += 1.0/2.0*np.pi*np.log(Rnua/Rnu)*log( (1.0 - nu/nua) / (1.0 + nu/nua) )
