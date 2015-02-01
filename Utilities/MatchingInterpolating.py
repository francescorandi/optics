import numpy as np
from scipy.interpolate import interp1d

def chooseMatchingPoint():
	#still to figure out what exactly to implement here
	return 0.0

def matchValue(Y1, Y2, operation='scale', value='average', weigth=0.5):
	if value == 'average':
		y0 = Y1[-1] * confidence + Y2[0] * (1.0 - confidence)
		
	if operation == 'scale': 
		Y1 *= y0 / Y1[-1]
		Y2 *= y0 / Y2[0]
	
	if operation == 'shift':
		Y1 += y0 - Y1[-1]
		Y2 += y0 - Y2[0]
	
	return np.append(Y1,Y2), len(Y1)-1
	
def matchDerivatives(X, Y, i0, n):
	#check i0+-1!! 
	Xp = np.append(X[i0-2*n:i0-n],X[i0+n:i0+2*n])
	Yp = np.append(Y1[i0-2*n:i0-n],Y2[i0+n:i0+2*n])
	
	f = interp1d(Xp,Yp,n)
	Y[i0-n:i0+n] = f(X[i0-n:i0+n])
	
	return Y
	
def interpolate(X1, X2, Y1, Y2, Xnew, n):
	#Should there more deep checks on ordering of X1 and X2?
	if X1[-1] < X2[0]:
		Xa = X1
		Xb = X2
		Ya = Y1
		Yb = Y2
	elif X[0] > X2[-1]:
		Xa = X2
		Xb = X1
		Ya = Y2
		Yb = Y1
	
	Xp = np.append(Xa,Xb)
	Yp = np.append(Ya,Yb)
	
	f = interp1d(Xp, Yp, n)
	Ynew = f(Xnew)
	
	return np.append(X1,[X2,Xnew]), np.append(Y1,[Ynew,Y2])
