#from src.neuron import neuron_test
from src.muscle import *

# neuron_test()
muscle_test()
print("I'm main")

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 100, 1000)
C_N0 = 1 # Чему, ёлы-палы, может быть равен C_N?
F0 = 0
X0 = array([C_N0, F0])

X =  integrate.odeint(dX_dt, X0, t) 

#%%
fig = p.figure()
p.plot(t, np.sin(t))
p.plot(t, X.T[1]*5000) # Achtung! Тут надо транспонировать!
p.show(block=True)