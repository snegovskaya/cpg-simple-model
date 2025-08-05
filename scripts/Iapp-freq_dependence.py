import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model")
from src.neuron import Neuron 
from src.net import Net 
from src.ode_system import ODE_system 
from src.Iapp_patterns import I_const

import numpy as np 
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq 
from scipy.optimize import curve_fit


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

        # plt.plot(t, v) # Отладочный график для малого кол-ва Iapp
        # plt.title("Картина спайков при Iapp = %.2f мкА" %(Iapp))
        # plt.show(block = True)

        v_freq = get_v_freq(v, T) # FIXME А есть ли именно соответствующий метод для массива?
        v_freq = np.abs(v_freq[1:N//2]) # Предобработка под задачу поиска макс. частоты
        freq = fftfreq(N, dt)
        freq = freq[1:N//2] # Предобработка под задачу поиска макс. частоты
        # plt.plot(freq[1:N//2], np.abs(v_freq[1:N//2])) # Старая версия, без предобработки 

        # plt.plot(freq, v_freq) # Отладочный график для малого кол-ва Iapp
        # plt.title("Фурье-разложение картины спайков при Iapp = %.2f мкА" %(Iapp))
        # plt.show(block = True) 

        # dominant_frequencies.append(freq[np.argmax(np.abs(v_freq))]) # Старая версия, без предобработки 
        dominant_frequencies.append(freq[np.argmax(v_freq)])
         

    plot = plt.plot(Iapp_probes, dominant_frequencies)
    plt.title("Зависимость частоты спайкинга $(мс^-1)$ на нейроне ХХ \
        \n от постоянного внешнего тока $I_{app}$ \
        \n в диапазоне от %.2f до %.2f мкА на %i знач-ях $I_{app}$" %(Iapp_probes[0], Iapp_probes[-1], len(Iapp_probes))) 
    plt.xlabel('$Iapp, \: \mathrm{мкА}$') 
    plt.ylabel('$частота, \: \mathrm{мс}^{-1}$') 
    plt.show(block = True)
    
    return dominant_frequencies
    # fit(plot, <certain_dependence>)


def Iapp_from_freq(Iapp_probes, dominant_frequencies): # FIXME: конкретизировать черновик
    '''
    Для практического использования на выходе хотим видеть формулу пересчёта
    из частоты в Iapp — скорее всего функцию.
    ''' 
    plt.plot(dominant_frequencies, Iapp_probes)
    plt.title("Зависимость входного тока на нейроне \
              \n от выходной частоты спайкинга данного нейрона")
    return # reverse(dependence) 

if __name__ == "__main__": 
    T = 500 # мс
    N = 1000 # точек 
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
    Iapp_min = 0.38 #мкА # Было 1 мкА
    Iapp_max = 2.88 #мкА # Было 1.3 мкА
    Iapp_n_points = 10 
    Iapp_probes = np.linspace(Iapp_min, Iapp_max, Iapp_n_points)
    dominant_frequencies = freq_from_Iapp(T, N, Iapp_probes) 
    Iapp_from_freq(Iapp_probes, dominant_frequencies) 

    def fitting_func(x, a0, a1, a2, a3, a4): 
        return a0 * x**4 + a1 * x**3 + a2 * x**2 + a3 * x + a4
    
    pars, pars_cov = curve_fit(fitting_func, Iapp_probes, dominant_frequencies) 
    fitting_freqs = list(map(lambda x: fitting_func(x, *pars), Iapp_probes)) # FIXME: Почему не работает array от map'а?
    plt.plot(Iapp_probes, dominant_frequencies, label = 'фактическая зависимость') 
    plt.plot(Iapp_probes, fitting_freqs, label = 'фиттинг')
    plt.xlabel('$частота, \: \mathrm{мс}^{-1}$')
    plt.ylabel('$Iapp, \: \mathrm{мкА}$') 
    plt.title("Фиттирование зависимости входного тока на нейроне \
              \n от его выходной частоты спайкинга") 
    plt.legend()
    plt.show(block = True) 
    print("Значения пар-ров кривой фиттинга, \
        \n многочлена 4 порядка: \
        \n a0 = %.2E; \n a1 = %.2E; \n a2 = %.2E; \n a3 = %.2E; \n a4 = %.2E" \
        %(pars[0], pars[1], pars[2], pars[3], pars[4])) 

'''
a0 = -9.24E-03; 
 a1 = 6.13E-02; 
 a2 = -1.32E-01; 
 a3 = 1.26E-01; 
 a4 = -2.44E-02
''' 

