from src.neuron import *
from src.muscle import muscle_test 

neuron_test()
muscle_test()
print("I'm main")

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate


vrest = -63.0540942 # По книге vrest = -65.0
mrest = 0.06 # По книге mrest = 0.05
nrest = 0.00 # По книге nrest = 0.00
hrest = 0.54 # По книге hrest = 0.62
X0 = array([vrest,mrest,nrest,hrest])
t = linspace(0, 500, 100000) # Временная шкала
#tauInput = 500
Iapp = 4

X =  integrate.odeint(dX_dt, X0, t, args=(Iapp,)) # args=(Iapp, tauInput)
v, m, n, h = X.T 

fig = p.figure()
p.plot(t, v)
p.show(block=True)