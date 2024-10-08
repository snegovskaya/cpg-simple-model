from numpy import array, zeros 
from src.net import Net
from src.neuron import Neuron
from src.muscle import Muscle 
from scipy.integrate import odeint


## ------------- Наброски функционала ------------- 

# N_eq = sum(element.eq_num for element in net.elements_list) 
# variables_array = zeros(1, N_eq)
# ode_array = zeros(1, N_eq)  # FIXME: Переименовать, возможно

def ode_system(net): 
    N_eq = sum(element.eq_num for element in net.elements_list) # FIXME: Здесь эти строчки пускать или где?
    variables_array = []
    ode_array = [] # FIXME: Так массив или список? И аппендить или заменять?
    for element in net.elements_list: 
        ode_array.append(element.model()) # FIXME: тут имеет смысл ставить либо везде ode_system, либо model
    return ode_array 
##-------------------------------------------------

def ode_solution(net, t): 
    net.ode_system()
    result = odeint(net.ode_system, net.initial_values, t) # Добавить поля в класс
    return result


def delegate_Muscle(obj, vars, t, **kwargs): # Нужно ли сюда именно впихивать t? 
    obj.CN = vars[0] 
    # print(obj.CN) # Убрать потом
    obj.F = vars[1] 
    obj.u = kwargs.pop('input') # Леплю говно
    if  obj.upars.get('t') != None: 
        obj.upars['t'] = t # Химичим с t 
        # FIXME Что-то там было про переписать upars[t]
    return obj.model()

def delegate_Neuron(obj, vars, t): 
    obj.v = vars[0] 
    print('v = ', obj.v) # Убрать потом 
    obj.m = vars[1] 
    obj.n = vars[2] 
    obj.h = vars[3] 
    if obj.IappPars.get('t') != None: 
        obj.IappPars['t'] = t 
    return obj.model()


def delegate (obj, vars, t):
    if isinstance(obj, Neuron): 
        delegate_Neuron(obj, vars, t)
    elif isinstance(obj, Muscle): 
        delegate_Neuron(obj, vars, t)


'''Вопрос: что мы хотим интегрировать? 
Это должен быть какой-то такой вид: 
integrate.odeint(circuit_ODE, vars, t)
?

Если да, то тогда надо сразу забивать под неё матрицу
'''