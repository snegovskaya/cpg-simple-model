## Скрипт для сети из одного нейрона, одной мышцы и одного рецептора
import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model")
import numpy as np
from src.net import Net 
from src.neuron import Neuron 
from src.muscle import Muscle 
from src.receptor import Receptor
from src.Iapp_patterns import I_impulse, I_period_impulse 
from src.ode_system import ODE_system  

from matplotlib import pyplot as p 
from math import sin, pi

## Задание сети 
net = Net(3) # FIXME: динамическое расширение сети 
neuron = Neuron(net = net, input = [I_period_impulse]) # pars = {"impulseAmpl": 10, "impulseLength": 10, "tStart": 5}
muscle = Muscle(input = neuron) 
receptor = Receptor(input = muscle)
neuron.input_nodes.append(receptor) 
net.set_matix()

## Решение модели
t = np.linspace(0, 500, 500) 
ode_system = ODE_system()
result = ode_system.solution(t)


##---- Построение графика, потому что как обычно нихрена не работает ---------
v, m, n, h, CN, F = result.T # Вернуть 
# v, m, n, h = result.T # Тест для одного 
Iapp_array = [I_period_impulse(t_meaning) for t_meaning in t] 

def get_I_receptor(F_array): # Костыль, чтобы чекнуть рецептор 
    I_receptor = [] 
    for F_meaning in F_array: 
        # receptor.F = F_meaning 
        # print(F_meaning, " ", receptor.F)
        # I_receptor.append(receptor.I) 
        I_receptor.append(sin(F_meaning + pi))
    return I_receptor 

I_receptor = get_I_receptor(F) 


fig = p.figure() 
# p.plot(t, v) 
# p.plot(t, [magnitude*1e2 for magnitude in m], label = "m (x10^2)")
# p.plot(t, [magnitude*1e3 for magnitude in n], label = "n (x10^3)") 
# p.plot(t, [magnitude*1e2 for magnitude in h], label = "h (x10^3)")
p.plot(t, [magnitude*1e1 for magnitude in Iapp_array], label = "Iapp (x10^2)")
# p.plot(t, [input(tmeaning)*10 for tmeaning in t], label = 'Iapp (10x)') # масштаб x10 
p.plot(t, v, label = 'v')
p.plot(t, [magnitude*1 for magnitude in F],label = 'F') 
p.plot(t, I_receptor, label = "I_receptor") 
# # p.plot(t, FN,label = 'FN') # FIXME Тестовая строчка, удалить
# p.plot(t, CN*1e-1, label = 'CN (0.1x)')
# p.xlabel('$t, \: \mathrm{мс}$')
p.legend()
p.title("Потенциал на нейроне $v$ и мускульная сила $FN$ \
    \n при импульсном внешнем токе $I_{app}(t)$ \
    \n (без рецептора)")
# и зависимостью тока $I$ на рецепторе от $FN$ как $I = sin(FN + \pi)$") 
# амплитудой %.0f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$), \n\
# длительностью импульса %.0f $\mathrm{мс}$ и скважностью импульсов %.0f $\mathrm{мс}$ % (5, 1, 10) 

# \n и скважностью импульсов %.0f $\mathrm{мс}$
p.show(block = True) 
 # 

# print("It works!")