from src.muscle import *
from src.neuron import *

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 25, 1000) 

v0 = -63.0540942 
m0 = 0.06 
n0 = 0.00 
h0 = 0.54
vars0_neuron = (v0, m0, n0, h0)

CN0 = 0
F0 = 0
vars0_muscle = (CN0, F0) 

def Iimpulse(t: float, impulseAmpl = 5, impulseLength = 5, tStart = 1):
    if t > tStart and t < tStart + impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I 


def Iperiod_impulse(t: float, impulseAmpl = 5, impulseLength = 5, period = 10, tStart = 1):
    if (t - tStart) % period <= impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I 

input = Iperiod_impulse 

test_neuron = Neuron(v0, m0, n0, h0, input=input, t=t[0])

# test_result = integrate.odeint(lambda *args: delegate_neuron(test_neuron, *args,), vars0_neuron, t) 
# v,m,n,h = test_result.T 

test_muscle = Muscle(CN0, F0, input = test_neuron.v - v0) # t=t[0] 
test_muscle.tauc *= 1e3 
test_muscle.tau1 *= 1e3
test_muscle.tau2 *= 1e3
# Таким образом имеем, что test_muscle.CN = CN0, test_muscle.F = F0 

# test_muscle = Muscle(CN0, F0, input = test_neuron.v - v0, t=t[0])
   
# test_result = integrate.odeint(lambda *args: delegate_muscle(test_muscle, *args,), vars0_muscle, t)
# CN, FN = test_result.T 
  

def delegate_circuit(neuron, muscle, vars, t): 
    vars_neuron = vars[0:4]
    vars_muscle = vars[4:]
    model_neuron = delegate_Neuron(neuron, vars_neuron, t)
    model_muscle = delegate_Muscle(muscle, vars_muscle, t, input = neuron.v - v0) 
    return concatenate([model_neuron, model_muscle]) 

vars0 = vars0_neuron + vars0_muscle

test_result = integrate.odeint(lambda *args: delegate_circuit(test_neuron, test_muscle, *args,), vars0, t)
v,m,n,h, CN, FN = test_result.T 
print(CN)


# def delegate_CN(muscle, v, t): # тест интегрирования одного уравнения CN при импульсном токе 
#     muscle.u = v
#     if muscle.upars.get('t') != None:
#         muscle.upars['t'] = t
#     return muscle.eq_CN()


# test_muscle = Muscle(CN0, F0, input = Iimpulse, t=t[0]) 

# test_result = integrate.odeint(lambda *args: delegate_CN(test_muscle, *args,), CN0, t) 
# print(test_result.T)
# CN = test_result.T[0]  

print('at ')

fig = p.figure()
p.plot(t, [Iperiod_impulse(tmeaning) for tmeaning in t], label = 'Iapp')
p.plot(t, v, label = 'v')
p.plot(t, 1e2*FN,label = 'FN (x100)')
# p.plot(t, FN,label = 'FN') # FIXME Тестовая строчка, удалить
p.plot(t, CN*1e1, label = 'CN (x10)')
p.xlabel('$t, \: \mathrm{мс}$')
p.legend()
p.title('Поведение потенциала на нейроне $v$ и мускульной силы $FN$ (x1000) \n при импульсном внешнем токе $I_{app}(t)$ \n амплитудой %.2f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$) и длительностями импульса от %.1f до %.1f $\mathrm{мс}$' % (5, 1, 5))
p.show(block = True) 

fig_testMuscle = p.figure()
p.plot(t * 10, CN, label = 'CN')
p.plot(t, v, label = 'v')
p.xlabel('$t, \: \mathrm{с}$')
p.show(block = True)