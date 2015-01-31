import numpy as np
from scipy import integrate

def real2imag(Nu, Y, iNuEval=None):
	"""Compute the imaginary part g of a causal function of the form
	f + ig given its real part f.
	
	iNuEval must be the array of indexes of Nu where to calculate KK.
	"""
	
	if iNuEval==None:
		iNuEval = np.arange(Nu)
	
	L = len(iNuEval)
	NuEval = np.zeros(L)
	Result = np.zeros(L)
	for i in range(L):
		j = iNuEval[i]
		nuEval = Nu[j]
		
		Integrand = np.divide(Y-Y[j],np.power(Nu,2)-np.power(nuEval,2))
		
		result = integrate.simps(Integrand,X=Nu)
		
		NuEval[i] = nuEval
		Result[i] = -2.0 * nuEval / np.pi * result
	
	return NuEval, Result
	
def imag2real(Nu, Y, iNuEval=None):
	"""Compute the real part f of a causal function of the form
	f + ig given its real part g.
	
	iNuEval must be the array of indexes of Nu where to calculate KK.
	"""
	
	if iNuEval==None:
		iNuEval = np.arange(Nu)
	
	L = len(iNuEval)
	NuEval = np.zeros(L)
	Result = np.zeros(L)
	for i in range(L):
		j = iNuEval[i]
		nuEval = Nu[j]
		
		Integrand = 0.0#np.divide(Y-Y[j],np.power(Nu,2)-np.power(nuEval,2))
		
		result = integrate.simps(Integrand,X=Nu)
		
		NuEval[i] = nuEval
		Result[i] = -2.0 * nuEval / np.pi * result
	
	return NuEval, Result

def mod2phase(Nu, Y, iNuEval=None, Extrapolation="FreeCharges", ExtrapolationParams=None):
	"""Compute the imaginary part g of a causal function of the form
	log(f) + ig, i.e. f*exp(ig), given f. High frequency
	extrapolations are done above the last 
	
	iNuEval must be the array of indexes of Nu where to calculate KK.
	"""
	
	if iNuEval==None:
		iNuEval = np.arange(Nu)
		
	L = len(iNuEval)
	NuEval = np.zeros(L)
	Result = np.zeros(L)
	
	nuLast = Nu[-1]
	yLast = Y[-1]
	
	if Extrapolation=="FreeCharges":
		#No intermediate region
		ExtrapolationParams = {'nub': nuLast, 's': 0.0, 'N': 10}
	
	if Extrapolation=="Full":
		#With intermediate region
		ExtrapolationParams = {'nub': nuLast*2.0, 's': 2.0, 'N': 10}

	for i in range(L):
		j = iNuEval[i]
		nuEval = Nu[j]
		
		Integrand = np.divide(np.log(Y/Y[j]),np.power(nuEval,2)-np.power(Nu,2))
		
		result = integrate.simps(Integrand,X=Nu)
		resultExtrap = mod2phase_extrapolation_high(nuEval, nuLast, Y[j], yLast, ExtrapolationParams)
		
		NuEval[i] = nuEval
		Result[i] = nuEval / np.pi * result * resultExtrap
	
	return NuEval, Result
	
def mod2phase_extrapolation_high(nu, nua, Rnu, Rnua, ExtrapolationParams):
	"""High energy contributions. See Wooten's book, Appendix G."""
	
	nub = ExtrapolationParams['nub']
	s = ExtrapolationParams['s']
	N = ExtrapolationParams['N']
	
	result = 0.0
	nnua = nu/nua
	nnub = nu/nub
	fourms = 4.0 - s
	for n in np.arange(N):
		result += (s * pow(nnua,2*n+1) + fourms * pow(nnub, 2*n+1)) / pow(2*n + 1, 2)
	result *= np.pi
	result += 1.0/2.0*np.pi*np.log(Rnua/Rnu)*log( (1.0 - nu/nua) / (1.0 + nu/nua) )
	
	return result
