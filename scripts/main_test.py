from src.muscle import *
from src.neuron import *

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 100, 100)
CN0 = 1
F0 = 0
vars0 = (CN0, F0) 

def Iimpulse(t: float, impulseAmpl = 50, impulseLength = 5, tStart = 1):
  if t > tStart and t < tStart + impulseLength:
    I = impulseAmpl
  else:
    I = 0
  return I 

input = Iimpulse

test_muscle = Muscle(CN0, F0, input=Iimpulse, t=t[0])
# Таким образом имеем, что test_muscle.CN = CN0, test_muscle.F = F0 
   
test_result = integrate.odeint(lambda *args: delegate(test_muscle, *args,), vars0, t)
print(test_result) 
CN, FN = test_result.T 

fig = p.figure()
p.plot(t, FN)
p.show(block = True)
