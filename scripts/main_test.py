from src.muscle import *
from src.neuron import *

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 100, 100) 


v0 = -63.0540942 
m0 = 0.06 
n0 = 0.00 
h0 = 0.54
vars0_neuron = (v0, m0, n0, h0)

CN0 = 1
F0 = 0
vars0_muscle = (CN0, F0) 

def Iimpulse(t: float, impulseAmpl = 50, impulseLength = 5, tStart = 1):
  if t > tStart and t < tStart + impulseLength:
    I = impulseAmpl
  else:
    I = 0
  return I 

input = Iimpulse 

test_muscle = Muscle(CN0, F0, input=Iimpulse, t=t[0])
# Таким образом имеем, что test_muscle.CN = CN0, test_muscle.F = F0 
   
test_result = integrate.odeint(lambda *args: delegate_muscle(test_muscle, *args,), vars0_muscle, t)
print(test_result) 
CN, FN = test_result.T 

test_neuron = Neuron(v0, m0, n0, h0, input=Iimpulse, t=t[0])

test_result = integrate.odeint(lambda *args: delegate_neuron(test_neuron, *args,), vars0_neuron, t) 
v,m,n,h = test_result.T 

fig = p.figure()
# p.plot(t, [Iimpulse(tmeaning) for tmeaning in t])
# p.plot(t, FN)
p.plot(t, v)
p.show(block = True) 

