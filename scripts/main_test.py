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

CN0 = 0
F0 = 0
vars0_muscle = (CN0, F0) 

def Iimpulse(t: float, impulseAmpl = 5, impulseLength = 5, tStart = 1):
    if t > tStart and t < tStart + impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I 



def Iperiod_impulse(t: float, impulseAmpl = 5, impulseLength = 5, period = 10, tStart = 1, tFinish = 50): 
    if t > tFinish: 
        I = 0
    elif (t - tStart) % period <= impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I 

input = Iimpulse 

test_neuron = Neuron(v0, m0, n0, h0, input=input, t=t[0])

# test_result = integrate.odeint(lambda *args: delegate_neuron(test_neuron, *args,), vars0_neuron, t) 
# v,m,n,h = test_result.T 

test_muscle = Muscle(CN0, F0, input = test_neuron.v - v0) # t=t[0] 
# Вот тут бы уточнить, чо по единицам измерения
# test_muscle.tauc *= 1e3 
# test_muscle.tau1 *= 1e3
# test_muscle.tau2 *= 1e3
# Таким образом имеем, что test_muscle.CN = CN0, test_muscle.F = F0 

# test_muscle = Muscle(CN0, F0, input = test_neuron.v - v0, t=t[0])
   
# test_result = integrate.odeint(lambda *args: delegate_muscle(test_muscle, *args,), vars0_muscle, t)
# CN, FN = test_result.T 
  

# Полностью собранная схема
def delegate_circuit(neuron, muscle, vars, t): 
    vars_neuron = vars[0:4]
    vars_muscle = vars[4:]
    model_neuron = delegate_Neuron(neuron, vars_neuron, t)
    model_muscle = delegate_Muscle(muscle, vars_muscle, t, input = neuron.v - v0) 
    return concatenate([model_neuron, model_muscle]) 

vars0 = vars0_neuron + vars0_muscle

test_result = integrate.odeint(lambda *args: delegate_circuit(test_neuron, test_muscle, *args,), vars0, t)
v,m,n,h, CN, FN = test_result.T 

# Строю кривую нейрона отдельно

neuron_vars = integrate.odeint(lambda *args: delegate_Neuron(test_neuron, *args,), vars0_neuron, t) 
v,m,n,h = neuron_vars.T 

# # График v(t) для нейрона
# fig = p.figure()
# p.plot(t, [Iimpulse(tmeaning) for tmeaning in t], label = 'Iapp')
# p.plot(t, v, label = 'v')
# p.xlabel('$t, \: \mathrm{мс}$')
# p.legend()
# p.title('v(t) при импульсном внешнем токе $I_{app}(t)$ \n амплитудой %.2f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$) и длительностями импульса от %.1f до %.1f $\mathrm{мс}$' % (5, 1, 5))
# p.show(block = True)


# # тест интегрирования одного уравнения CN при импульсном токе 
# def delegate_CN(muscle, CN, uinput, t):
#     muscle.CN = CN 
#     print('CN= ',CN) # Убрать потом
#     if muscle.upars.get('t') != None:
#         muscle.upars['t'] = t
#         muscle.u = uinput(**muscle.upars) 
#     else:
#         muscle.u = uinput
#         print('muscle.u = ', muscle.u) # Убрать потом
#     return muscle.eq_CN() 


# def getvt(tarray=t, varray=v, **kwargs): # Вот этот набросок надо доработать 
#     tmeaning = kwargs['t']
#     return varray[where(tarray==tmeaning)[0]] 


# test_muscle = Muscle(CN0, F0, input = getvt, t=t[0]) # Заменила импульс тока на функцию доступа к независимому v
# def instead_of_lambda(*args):
#     return delegate_CN(test_muscle, *args) 
# test_result = integrate.odeint(instead_of_lambda, CN0, t) 
# # test_result = integrate.odeint(lambda *args: delegate_CN(test_muscle, *args,), CN0, t) 
# CN = test_result.T[0]  


# # Попытка в сборку чисто с CN

# def delegate_circuit(neuron, muscle, vars, t):
#     print('t = ', t) # Убрать потом 
#     vars_neuron = vars[0:4]
#     CN = vars[4:]
#     model_neuron = delegate_Neuron(neuron, vars_neuron, t)
#     model_CN = delegate_CN(muscle, CN, neuron.v - v0, t) 
#     return concatenate([model_neuron, model_CN]) 

# vars0 = vars0_neuron + (CN0,)



# test_result = integrate.odeint(lambda *args: delegate_circuit(test_neuron, test_muscle, *args,), vars0, t)
# v, m, n, h, CN = test_result.T



# Самый главный график
fig = p.figure()
p.plot(t, [Iimpulse(tmeaning)*10 for tmeaning in t], label = 'Iapp') # масштаб x10 
p.plot(t, v, label = 'v')
p.plot(t, FN*1e2,label = 'FN')
# p.plot(t, FN,label = 'FN') # FIXME Тестовая строчка, удалить
p.plot(t, CN, label = 'CN')
p.xlabel('$t, \: \mathrm{мс}$')
p.legend()
p.title('Поведение потенциала на нейроне $v$ и мускульной силы $FN$ (x1000) \n при импульсном внешнем токе $I_{app}(t)$ \n амплитудой %.2f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$) и длительностями импульса от %.1f до %.1f $\mathrm{мс}$' % (5, 1, 5))
p.show(block = True) 

# # График CN
# fig = p.figure()
# p.plot(t, [Iimpulse(tmeaning) for tmeaning in t], label = 'Iapp')
# p.plot(t, v, label = 'v')
# p.plot(t, CN, label = 'CN')
# p.xlabel('$t, \: \mathrm{мс}$')
# p.legend()
# p.title('CN при импульсном внешнем токе $I_{app}(t)$ \n амплитудой %.2f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$) и длительностями импульса от %.1f до %.1f $\mathrm{мс}$' % (5, 1, 5))
# p.show(block = True)