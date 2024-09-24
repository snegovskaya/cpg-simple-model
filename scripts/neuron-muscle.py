import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model/src")
import numpy as np
from src.net import Net 
from src.element import Element
from src.neuron import Neuron 
from src.muscle import Muscle 
from src.Iapp_patterns import I_impulse 
from src.ode_solution import ode_solution 

from matplotlib import pyplot as p

## Задание сети 
# net = Net(2) # Вернуть
net = Net(1) # Тест для одного 
neuron = Neuron(net = net, input = I_impulse) # pars = {"impulseAmpl": 10, "impulseLength": 10, "tStart": 5}
# muscle = Muscle(input = neuron) # Вернуть 

t = np.linspace(0, 100, 100)
result = ode_solution(net, t)


##---- Построение графика, потому что как обычно нихрена не работает ---------
# v, m, n, h, CN, FN = result.T # Вернуть 
v, m, n, h = result.T # Тест для одного 
Iapp_array = [I_impulse(t_meaning) for t_meaning in t]

fig = p.figure() 
p.plot(t, v) 
p.plot(t, m)
p.plot(t, n) 
p.plot(t, h)
# p.plot(t, FN) # Вернуть 
p.plot(t, Iapp_array)
# p.plot(t, [input(tmeaning)*10 for tmeaning in t], label = 'Iapp (10x)') # масштаб x10 
# p.plot(t, v, label = 'v')
# p.plot(t, FN,label = 'FN')
# # p.plot(t, FN,label = 'FN') # FIXME Тестовая строчка, удалить
# p.plot(t, CN*1e-1, label = 'CN (0.1x)')
# p.xlabel('$t, \: \mathrm{мс}$')
# p.legend()
# p.title('Поведение потенциала на нейроне $v$ и мускульной силы $FN$ \n при импульсном внешнем токе $I_{app}(t)$ \n амплитудой %.0f $\mathrm{мкА/см^2}$ (показана $10\mathrm{x}$) и длительностью импульса %.0f $\mathrm{мс}$' % (5, 1)) # \n и скважностью импульсов %.0f 
p.show(block = True) 


print("It works!")