from src.neuron import Neuron 
from src.net import Net 
from src.ode_system import ODE_system


def get_v_freq(v): # FIXME: скопипастить Фурью из nemusrec'a 
    '''
    Фурье-обработка массива значений v;
    Дополнительно требуется время симуляции Т 
    и, возможно, кол-во точек N. 
    На выходе хорошо бы, чтобы давал положение локальных максимумов для частот
    '''
    pass 

def get_v(neuron, Iapp, t): # FIXME: банально пофиксить
    '''
    Должен для переданного эл-та класса Neuron, 
    входного тока Iapp 
    и заданных параметров симуляции 
    выдать массив v. 
    Требует импортирования класса Neuron 
    и модуля, который занимается интегрированием.
    '''
    neuron = Neuron(input = I_const(*args, **kwargs)) 
    neuron.net.set_matrix() 
    ode_system = ODE_system()
    result = ode_system.solution(t)
    v, m, n, h, CN, F = result.T 
    return v


def freq_from_Iapp(): 
    '''
    Подаётся нейрон и набор константных Iapp; 
    На выходе хотим видеть для каждого Iapp доминирующую частоту; 
    Хотя полезнее сразу делать фиттинг функции и выдавать коэф-ты
    '''
    for Iapp in Iapp_probes: #FIXME: банально пофиксить 
        i = Iapp_probes.index(Iapp)
        v_meanings[i] = get_v() 
        v_maxes[i] = max(v_meanings[i]) 

    plot = p.pyplot(Iapp_probes, v_maxes) 
    return plot
    # fit(plot, <certain_dependence>)


def Iapp_from_freq(depenence): # FIXME: конкретизировать черновик
    '''
    Для практического использования на выходе хотим видеть формулу пересчёта
    из частоты в Iapp — скорее всего функцию.
    '''
    return reverse(dependence)