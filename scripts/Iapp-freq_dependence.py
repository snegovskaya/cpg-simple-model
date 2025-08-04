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

    freq = fftfreq(N, dt) 
    '''Должен выдать N точек:
    [0, 1, ..., N/2-1, -N/2, ..., -1] / N, если N чётное; 
    [0, 1, ..., N/2,   -N/2, ..., -1] / N, если N нечётное.
    ''' 
    v_freq = fft(v) # Выдаст N неупорядоченных точек (комплексных чисел!) 

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
    # del ode_system.net # FIXME: Долбанутая ручная чистка сети
    # del neuron.net
    v, m, n, h = result.T 
    return v


def freq_from_Iapp(T, N, Iapp_probes = np.linspace(0, 5, 50)): 
    '''
    Подаётся нейрон и набор константных Iapp; 
    На выходе хотим видеть для каждого Iapp доминирующую частоту; 
    Хотя полезнее сразу делать фиттинг функции и выдавать коэф-ты
    '''
    dominant_frequencies = [] # FIXME: переделать из списка в массив с заранее выделенной памятью
    v_array = [] 
    v_freq_array = []

    for Iapp in Iapp_probes: #FIXME: банально пофиксить 
        t = np.linspace(0, T, N)
        dt = np.diff(t)[0] # ms, шаг симуляции 
        v = get_v(Iapp, T, N) 
        # plt.plot(t, v)
        # plt.show(block = True)
        v_freq = get_v_freq(v, T) # FIXME А есть ли именно соответствующий метод для массива?
        v_freq = np.abs(v_freq[1:N//2]) # Предобработка под задачу поиска макс. частоты
        freq = fftfreq(N, dt)
        freq = freq[1:N//2] # Предобработка под задачу поиска макс. частоты
        # plt.plot(freq[1:N//2], np.abs(v_freq[1:N//2])) # Старая версия, без предобработки 
        # plt.plot(freq, v_freq)
        # plt.show(block = True)
        # dominant_frequencies.append(freq[np.argmax(np.abs(v_freq))]) # Старая версия, без предобработки 
        dominant_frequencies.append(freq[np.argmax(v_freq)])
         

    plot = plt.plot(Iapp_probes, dominant_frequencies)
    plt.title("Зависимость частоты спайкинга $(мс^-1)$ на нейроне ХХ \
        \n от постоянного внешнего тока $I_{app}$ \
        \n в диапазоне от %.0f до %.0f мкА на 50 точках" %(Iapp_probes[0], Iapp_probes[-1])) 
    plt.xlabel('$Iapp, \: \mathrm{мкА}$') 
    plt.ylabel('$частота, \: \mathrm{мс}^{-1}$') 
    plt.show(block = True)
    
    return dominant_frequencies
    # fit(plot, <certain_dependence>)


def Iapp_from_freq(depenence): # FIXME: конкретизировать черновик
    '''
    Для практического использования на выходе хотим видеть формулу пересчёта
    из частоты в Iapp — скорее всего функцию.
    '''
    return reverse(dependence) 

if __name__ == "__main__": 
    T = 500 # мс
    N = 100 # точек 
    Iapp1 = 1.15 
    Iapp2 = 1.25 
    # t = np.linspace(0, T, N) # FIXME: Надо шото сделать с дублированием здесь и в функции
    # v1 = get_v(Iapp1, T, N) 
    # v2 = get_v(Iapp2, T, N)
    # plt.plot(t, v1)
    # plt.plot(t, v2) 
    # plt.show(block = True)
    # ===
    # v = get_v(Iapp1, T, N) 
    # plt.plot(t, v)
    # v_freq = get_v_freq(v, T)
    # v1_freq = get_v_freq(v1, T)
    # v2_freq = get_v_freq(v2, T) # Вот это вот всё делалось для двух значений 
    Iapp_min = 0 #мкА # Было 1 мкА
    Iapp_max = 10 #мкА # Было 1.3 мкА
    Iapp_n_points = 20 
    Iapp_probes = np.linspace(Iapp_min, Iapp_max, Iapp_n_points)
    freq_from_Iapp(T, N, Iapp_probes) 
    # Iapp_from_freq()