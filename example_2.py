# RUN FROM OUTSIDE THE PACKAGE FOLDER <---------- <--------

import optics
import matplotlib.pyplot as plt
import numpy as np

#Create optical system environment
oenv = optics.system()

#Load data from file and plot it
ds = oenv.addData(inputFile='optics/R-gold', dataType='R', unitX='nm', name='gold', dtype=np.cfloat)
ds.scale(0.9) #error in the data
plt.plot(ds.x,ds.y)
plt.show()

#The x axis of the dataset is converted to eV upon loading.
#The function dataset.xto(unitX) allows to retrieve the x axis of the dataset in
#units different from eV.
plt.plot(ds.xto('nm'), ds.y)
plt.show()

#Create a model
om = oenv.createModel()

#Add the oscillators
drude = optics.oscillators.Drude(10,0.1)
om.add(drude)
lor = optics.oscillators.Lorentz(1,1.5,2)
om.add(lor)

#Modify the oscillators' parameters: now they are properties and the abs()
#is taken at assignment
drude.width = 0.07
drude.amplitude = 20
lor.amplitude = 1
lor.width = 1.5
lor.position = 3

#Plot the refractive index produced by the model
#The optical relations are now contained in the relations module, which also
#contains the functions that convert the energy axis between the various units
energy = np.arange(0.01,6,0.01)
plt.plot(energy, optics.relations.refractive_index(om.dielectric_function(energy)))
plt.ylim(0,3)
plt.show()

#Compare the dataset and the model. dataset.inputToType() converts the
#dielectric function to the data type of the dataset by automatically picking
# the right function, e.g., o.relations.reflectivity()
plt.plot(ds.x,ds.y)
plt.plot(ds.x,ds.inputToType(om.dielectric_function(ds.x)))
plt.show()

oenv.save('system.h5')
