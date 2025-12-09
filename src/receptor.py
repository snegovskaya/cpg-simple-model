import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model") # для запуска __main__
from src.element import Element # from src.element import Element # Но вообще с этим надо что-то делать
from src.neuron import Neuron 
from math import sin, pi # Для отладки

class Receptor(Neuron): 
    """
    A spindle model taken from Matthews & Stein (1969). Laplace notation is used.
    """ 
    r = 1 # s^{-1}, instant frequency of receptor's spiking 
    __F = 0
    k = 1 # unitless, coefficient for namely this receptor model 
    phi = 1 # unitless, phase of receptor's spiking 
    A = 1 # mV, amplitude of receptor's spiking 
    u = 0 # mV 
    __I = 0, # mkA
    # input = F(t), Н  
    output = 0 # I(t), мА 


    ## Геттеры и сеттеры: 
    @property 
    def output(self): 
        """ 
        Организует выход с рецептора — быстрый ток I (который I_fast).
        """ 
        self.__output = self.I 
        print("I на рецепторе: ", self.__output)
        return self.__output 
    
    @output.setter #FIXME 
    def output(self, output): 
        """ 
        Должен принимать на вход, вообще говоря, медленный ток I_slow.
        """ 
        self.__output = output

    @property 
    def F(self): 
        """
        Интерпретирует поданное на вход в self.input как силу F.
        """
        self.__F = self.input() # Проверить, в каком виде, так-то, input 
        print("F на рецепторе: ", self.__F)
        return self.__F 
    
    @F.setter #  FIXME: Временный костыль 
    def F(self, F_meaning): 
        """
        Пока что как будто максимум, что имеет смысл делать в этом сеттере — это проверять self.input на адекватность.
        """
        self.__F = F_meaning


    def __init__(self, **kwargs): 
        super().__init__(**kwargs) # Вызов __init__'а из Neuron. FIXME: Какие поля нужно доо/переопределять?  
        self.F = self.input
    
    @property 
    def I(self): 
        """
        FIXME: Вот тут нужна схема преобразований! Потому я хз, быстрый это ток или медленный.
        """
        # return self.r() 
        return sin(self.F + pi) # Тестовое значение 

    def get_x(self): 
        """
        FIXME: Я хз, что это за параметр, и почему он запихнут в это же property. 
        Кстати: а декоратор же работает только над def I(self)?
        """
        self.x = self.F 
        return self.x 

    def x_Laplace(self): 
        pass 

    ## r через Лапласа — т.е. r(s): 
    def r(self, s=1): ## FIXME: s откуда и на каком этапе добывается?
        k = self.k 
        x = self.x 
        r = k*x*(s + 10)  
        return r 

    # ## r через x, dx_dt: 
    # def get_r(self): 
    #     print(self.input_node)

    def r_Laplace_inverse(self): 
        k = self.k 
        x = self.x
        dx_dt = 0 ## FIXME 
        r = k*x*(dx_dt + x) 
        return r 

    def get_I(self): 
        pass

    # def model_Laplace(self): # Возвращает модель рецептора в Лапласовской нотации
    #     return k * x * (s + 10) # r(s) = kx(s + 10)
    
    

if __name__ == '__main__': 
    t = 50 # ms # Но вообще linspace с последующим интегрированием
    F_period = 100 # ms
    import numpy as np
    receptor = Receptor(input = np.sin(2*pi*t/F_period))