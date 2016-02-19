from OpticalModel import OpticalModel
from Oscillators import Lorentz, Gauss

import numpy as np

# Creating Optical model
om = OpticalModel('Two Oscillator Example')

# Creating a Lorentz oscillator
l = Lorentz.Lorentz(1, 0.4, 2)
print(l)

om.add(l) # Adding Lorentz to the model
om.show()

# Creating and adding a Gaussian
g = Gauss.Gauss(1, 0.6, 6)
print(g)
om.add(g)
om.show()

# Establishing the energy window of interest
energies = np.arange(0.01,8,0.005)

# Plotting the dielectric function
om.plot(energies)
