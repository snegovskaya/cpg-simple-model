from src.neuron import *
from src.muscle import * 

# В самом начале нужно ввести количество эл-тов и огранизовать для них матрицу 

# Возможно, сеть лучше сразу оформлять как класс

"""Если был вызван init, то
    Узнать, что это за звено; 
    Найти в матрице последний безымянный элемент (или нулевую строчку) и прописать там ребро 
    В массив системы дописать соответствующее кол-во модели 
    В массив vars дописать соответствующее количество переменных
"""
connectivity_matrix = zeros((2, 2))
print(connectivity_matrix)

# Функция для добавления матрицы: 

def refill_matrix(element, matrix = connectivity_matrix): 
    # # указатель на последний ряд матрицы должен стоять там, где его оставили
    # matrix[last, element.input] = 1; 

    return

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