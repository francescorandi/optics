from OpticalModel import OpticalModel
import Oscillators as osc
import numpy as np

# Creating Optical model
om = OpticalModel('Two Oscillator Example')

# Creating a Lorentz oscillator
l = osc.Lorentz(1, 0.4, 2)
print(l)

om.add(l) # Adding Lorentz to the model
om.show()

# Creating and adding a Gaussian
g = osc.Gauss(1, 0.6, 6)
print(g)
om.add(g)
om.show()
