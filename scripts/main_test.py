from src import muscle 
from src import neuron

neuron.neuron_test()
muscle.muscle_test()
print("I'm main")

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 100, 1000)
C_N0 = 1 # Чему, ёлы-палы, может быть равен C_N?
F0 = 0
X0 = array([C_N0, F0])
vrest = -63.0540942 # По книге vrest = -65.0
mrest = 0.06 # По книге mrest = 0.05
nrest = 0.00 # По книге nrest = 0.00
hrest = 0.54 # По книге hrest = 0.62
Y0 = array([vrest,mrest,nrest,hrest])
t = linspace(0, 500, 100000) # Временная шкала
Iapp = 4

X =  integrate.odeint(muscle.dX_dt, X0, t) 
C_N, F = X.T
Y =  integrate.odeint(neuron.dX_dt, X0, t, args=(Iapp,)) # args=(Iapp, tauInput)
v, m, n, h = Y.T 

fig1 = p.figure()
p.plot(t, v)
p.show(block=True)

fig2 = p.figure()
p.plot(t, sin(t))
p.plot(t, C_N*5000)
p.show(block=True)