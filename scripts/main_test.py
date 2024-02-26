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
t = linspace(0, 100, 1000) # Временная шкала
Iapp = 4

X =  integrate.odeint(muscle.dX_dt, X0, t) 
C_N, F = X.T
Y =  integrate.odeint(neuron.dX_dt, Y0, t, args=(Iapp,)) # args=(Iapp, tauInput)
v, m, n, h = Y.T 
def u(t):
    return  abs(sin(t*2))

fig1 = p.figure()
p.plot(t, v)
p.show(block=True)

fig2 = p.figure()
p.plot(t, u(t), label = '$u, \: \mathrm{мВ}$')
p.plot(t, F*500, label = '$F (x500), \: \mathrm{?}$')
p.legend()
p.xlabel('$t, \: \mathrm{мс}$')
p.ylabel('$u, \: F$')
p.ylim([-1, 1])
p.title('Мышечная сила и входное напряжение, зависимость от времени')
p.show(block=True)