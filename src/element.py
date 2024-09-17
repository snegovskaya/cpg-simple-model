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
        self.__index = index 

    @property
    def input(self): 
        return self.__input 
    
    @input.setter
    def input(self, input):
        self.__input = input 
    
    @property
    def output(self): 
        return self.__output  # без сеттера. Ещё вопрос, нужно ли оно.

    # Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        print("Вызов __new__ для " + str(cls)) 
        # Тут нужно такое: если в глобальном пространстве имён существует объект класса Net, то при каждом вызове new ссылку на него передавать по умолчанию 
        if not isinstance(cls.net, Net): # FIXME: В kwargs'ах-то net был!
            print("Ссылка на сеть для данного объекта класса Element отсутствует")
            # И теперь осталось по-нормальному создать сеть
            cls.net = Net(1) # FIXME: Тут создаётся сеть размерности 1 (но это если до того вообще никакой сети не было) Вопрос: как её потом расширять при необходимости?
        return super().__new__(cls)
    
    # Это вызовется после создания объекта класса:
    def __init__(self, **kwargs):  
        print("вызов __init__ для " + f"{self}") 
        try: 
            self.name = kwargs['name'] 
        except KeyError: 
            print("текущий элемент безымянный")
        try: 
            input = kwargs['input'] # FIXME: Здесь рано загонять значение в self.__input 
        except KeyError: 
            print("Для этого элемента нет input'a") 
            input = None 
        self.net.add_element(self, input = input)# Из-за чехарды с наследованием заменила self.__net на self.net 
        self.index = self.net.current_index # То же самое (см. выше)
        self.input = self.__input_proceeding(input) # FIXME: Обработку input'а на уровне диффуров вывести сюда

    ## Я хз, лучше ли писать функцию по обработке input до или после __init__'а, 
    ## Но в любом случае, вот фукция по обработке __input__'а: 
        
    def __input_proceeding(self, input): 

        def single_input_proceeding(input): # Функция обработки сигнала из одного источника
            if isinstance(input, (Element)): 
                if input.output is None: 
                    return 0 
                else: 
                    return input.output 
            else: 
                if input is None: 
                    return 0
                return input # FIXME: Дописать обработку всякой хрени, если input не является float'ом или функцией  
        
        def complex_input_proceeding(input): # FIXME 
            input_proceeded = list((0,)* len(input)) 
            for source in input:
                input_proceeded[input.index(source)] = single_input_proceeding(source)
            return sum(input_proceeded) # Achtung! Выполняю втупую суммирование входных сигналов
        
        if not isinstance (input, tuple): 
            return single_input_proceeding(input) 
        else: 
            return complex_input_proceeding(input)

    def __str__(self): 
        if self.__name is None: 
            return super().__str__()
        else: 
            return self.__name     
    
    def __del__(self): 
        pass # FIXME Прописать, что там должно происходить 

