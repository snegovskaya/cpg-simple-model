import numpy as np
from src.net import Net

class Element: 
    __name = None # уникальное имя элемента
    __net = None # ссылка на матрицу (сеть) 
    __index = None # порядковый номер в матрице (сети)
    __type = None # тип элемента (нейрон, мышца, рецептор) (пока без понятия, нужно или нет)
    __eq_num = 0 # число уравнений в модели
    __input = None # входной сигнал $ FIXME Аchtung: что делать, если входных сигналов несколько (дендриты)? 
    # __input давать в виде кортежа со ссылками на «входные» элементы
    __output = None # выходной сигнал

    ## Геттеры и сеттеры:
    
    @property
    def name(self): 
        return self.__name 
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def net(self): 
        return self.__net 
    
    @net.setter
    def net(self, net): 
        self.__net = net 

    @property
    def index(self): 
        return self.__index 
    
    @index.setter
    def index(self, index): 
        self.__net = index 

    @property
    def input(self): 
        return self.__input 
    
    @input.setter
    def input(self, input):
        self.__input = input

    # Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        print("Вызов __new__ для " + str(cls)) 
        # Тут нужно такое: если в глобальном пространстве имён существует объект класса Net, то при каждом вызове new ссылку на него передавать по умолчанию 
        if not isinstance(cls.__net, Net):
            print("Ссылка на сеть для данного объекта класса Element отсутствует")
            # И теперь осталось по-нормальному создать сеть
            cls.__net = Net(1) # FIXME: Тут создаётся сеть размерности 1 (но это если до того вообще никакой сети не было) Вопрос: как её потом расширять при необходимости?
        return super().__new__(cls)
    
    # Это вызовется после создания объекта класса:
    def __init__(self, **kwargs):  
        print("вызов __init__ для " + f"{self}") 
        try: 
            self.name = kwargs['name'] 
        except KeyError: 
            print("текущий элемент безымянный")
        try: 
            self.__input = kwargs['input'] # Просто передать кортеж 
        except KeyError: 
            print("Для этого элемента нет input'a") 
        self.__net.add_element(self, input = self.__input) # FIXME% Тут будут исключения! 
        self.__index = self.__net.current_index 

    def __str__(self): 
        if self.__name is None: 
            return super().__str__()
        else: 
            return self.__name     
    
    def __del__(self): 
        pass # FIXME Прописать, что там должно происходить 

