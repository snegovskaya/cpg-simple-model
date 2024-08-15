import numpy as np
from .net import Net

class Element: 

    __net = None # ссылка на матрицу 
    __index = None # порядковый номер в матрице 
    __type = None # тип элемента (нейрон, мышца, рецептор) 
    __eq_num = 0 # число уравнений в модели
    __input = None # входной сигнал $ FIXME Аchtung: что делать, если входных сигналов несколько (дендриты)?
    __output = None # выходной сигнал
    
    # Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        print("Вызов __new__ для " + str(cls)) 
        if cls.__net == None: # FIXME Не совсем верное условие: эта переменная пока не знает о том, появилась ли внешняя сеть
            print("Матрица связности для класса Element ещё не создана") 
            cls.__net = Net(1) # FIXME: Вот тут у нас конкретное старое говно
        # создать matrix
        # cls.matrix.iter() # FIXME Обязательно сначала реализовать итерирование по матрице
        cls.__net.refill(kwargs['input'])
        return super().__new__(cls)
    
    # Это вызовется после создания объекта класса:
    def __init__(self, **kwargs):  
        print("вызов __init__ для " + str(self)) 
        self.__input = kwargs['input'] 
    
    def __del__(self): 
        pass # FIXME Прописать, что там должно происходить 

    
