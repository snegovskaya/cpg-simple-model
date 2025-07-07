import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model")
from src.neuron import Neuron 
from src.net import Net 
from src.ode_system import ODE_system 
from src.Iapp_patterns import I_const

import numpy as np 
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


def get_v_freq(v, T): # FIXME: скопипастить Фурью из nemusrec'a 
    '''
    Фурье-обработка массива значений v;
    Дополнительно требуется время симуляции Т 
    !FIXME: лучше массив t, с заранее известным разбиением
    и, возможно, кол-во точек N. 
    На выходе хорошо бы, чтобы давал положение локальных максимумов для частот
    '''
    # Попытка в Фурью:  
    print("Общее время симуляции T = ", T) 
    
    N = len(v) # FIXME: для масcива (array) может выдать ошибку
    print("Число точек N = ", N) 

    t = np.linspace(0, T, N) 
    dt = np.diff(t)[0] # ms, шаг симуляции

    print("Шаг симуляции dt = ", dt) 

    freq = fftfreq(N) 
    '''Должен выдать N точек:
    [0, 1, ..., N/2-1, -N/2, ..., -1] / N, если N чётное; 
    [0, 1, ..., N/2,   -N/2, ..., -1] / N, если N нечётное.
    ''' 
    v_freq = fft(v) # Выдаст N неупорядоченных точек (комплексных чисел!) 

    # В нуле получается какой-то странный выброс, поэтому:
    freq = np.delete(freq, 0)
    freq = np.delete(v_freq, 0)

    # plt.plot(freq[1:N//2], np.abs(v_freq[1:N//2])) 
    # # p.xlim(left = 1)
    # plt.show(block = True) 

    return v_freq




def get_v(Iapp_meaning, T, N): # FIXME: банально пофиксить
    '''
    Должен для переданного эл-та класса Neuron, 
    входного тока Iapp 
    и заданных параметров симуляции 
    выдать массив v. 
    Требует импортирования класса Neuron 
    и модуля, который занимается интегрированием. 
    ''' 
    #Iapp = I_const(Amplitude=Iapp) # Да, это очень тупо, зато понятно 
    Iapp = Iapp_meaning
    neuron = Neuron(input = Iapp) 
    neuron.net.set_matrix()
    ode_system = ODE_system() 
    t = np.linspace(0, T, N) 
    result = ode_system.solution(t) # FIXME: выдаёт одномерный массив 
    del ode_system.net # FIXME: Долбанутая ручная чистка сети
    del neuron.net
    v, m, n, h = result.T 
    return v


def freq_from_Iapp(T, N, Iapp_probes = np.linspace(0, 10, 10)): 
    '''
    Подаётся нейрон и набор константных Iapp; 
    На выходе хотим видеть для каждого Iapp доминирующую частоту; 
    Хотя полезнее сразу делать фиттинг функции и выдавать коэф-ты
    '''
    dominant_frequencies = []
    v_array = [] 
    v_freq_array = []

    for Iapp in Iapp_probes: #FIXME: банально пофиксить 
        t = np.linspace(0, T, N) 
        v = get_v(Iapp, T, N) 
        v_freq = get_v_freq(v, T)
        dominant_frequencies.append(np.argmax(v_freq)) 
    

    plot = plt.pyplot(Iapp_probes, dominant_frequencies) 
    return dominant_frequencies
    # fit(plot, <certain_dependence>)


def Iapp_from_freq(depenence): # FIXME: конкретизировать черновик
    '''
    Для практического использования на выходе хотим видеть формулу пересчёта
    из частоты в Iapp — скорее всего функцию.
    '''
    return reverse(dependence) 

if __name__ == "__main__": 
    Iapp = 1.0 # мкА
    T = 500 # мс
    N = 500 # точек 
    t = np.linspace(0, T, N) # FIXME: Надо шото сделать с дублированием здесь и в функции
    # v = get_v(Iapp, T, N) 
    # plt.plot(t, v)
    # v_freq = get_v_freq(v, T) 
    freq_from_Iapp(T, N) 
    Iapp_from_freq()