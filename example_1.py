import numpy as np

import Oscillators as osc
from OpticalModel import OpticalModel

# Creating Optical model
om = OpticalModel('Two Oscillator Example')

# Creating a Lorentz oscillator
l = osc.Lorentz(1, 0.3, 2)
print(l)

# Adding Lorentz to the model
om.add(l)
om.show()

# Creating and adding a Gaussian
g = osc.Gauss(1, 0.8, 5)
print(g)
om.add(g)

# Printing a list of the oscillators in the model
om.show()

# Establishing the energy window of interest
energies = np.arange(0.01, 8, 0.005)

# Spectral weight

print("Gauss SW: ", g.spectralWeight)
print("Lorentz SW: ", l.spectralWeight)

print("Model SW: ", om.spectralWeight())
print("Partial SW (0 -- 4): ", om.spectralWeight([0, 4]))

# Plotting the dielectric function
om.plot(energies)
