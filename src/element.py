import numpy as np
from src.net import Net

class Element: 
    __name = None # уникальное имя элемента
    __net = None # ссылка на матрицу (сеть) 
    __index = None # порядковый номер в матрице (сети)
    __type = None # тип элемента (нейрон, мышца, рецептор) (пока без понятия, нужно или нет)
    __eq_num = 0 # число уравнений в модели 
    __vars = None
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
    def input(self, *args, **kwargs): 
        if isinstance(self.input_node, (Element)):
            element =  self.input_node
            if element.output is None: 
                self.__input = 0 
            else: 
                self.__input = element.output 
        elif callable(self.input_node): 
            input_func = self.input_node
            self.__input = input_func
        # FIXME: Должна ли здесь быть обработка? Опасное место.
        return self.__input 
    
    # @input.setter
    # def input(self, input):
    #     self.__input = self.__input_proceeding(input) # FIXME: Говна налепила!
 
    
    @property
    def output(self): 
        return self.__output  # без сеттера. Ещё вопрос, нужно ли оно. 
    
    # @output.setter # FIXME: Зайчаток сеттера для output'а
    # def out
    
    @property # FIXME
    def vars(self): 
        print("Задай vars, сцуко!") 

    @vars.setter 
    def vars(self, vars): 
        print("Нету у тебя vars, сцуко!")

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
    def __init__(self, *args, **kwargs):  # FIXME: Не знаю, насколько тут нужны *args
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
        self.net.add_element(self, input = input)# FIXME Из-за чехарды с наследованием заменила self.__net на self.net 
        self.index = self.net.current_index # То же самое (см. выше)
        self.input_node = input # FIXME: Временная тестовая строчка
        self.__primary_input_proceed(input)

    ## Я хз, лучше ли писать функцию по обработке input до или после __init__'а, 
    ## Но в любом случае, вот фукция по обработке __input__'а: 

   # Экспериментальная функция на замену старой      
    def __primary_input_proceed(self, input): 
        if isinstance (input, tuple): 
            self.__multiple_input_proceeding(input) # = __primary_input_proceed(input) 
        else: 
            self.__single_input_proceeding(input) 
    
    def __multiple_input_proceeding(self, input): # FIXME Костыль! 
            input_proceeded = list((0,)* len(input)) 
            for source in input:
                input_proceeded[input.index(source)] = self.__single_input_proceeding(source)
            return sum(input_proceeded) # Achtung! Выполняю втупую суммирование входных сигналов

    def __single_input_proceeding(self,input): # Функция обработки сигнала из одного источника
        if isinstance(input, (Element)):  
            # Нужно будет различать input как элемент и как число 
            self.__input = input # Вводим поле input'а как элемента 
            # Выковыривание из этого элемента числа: 
            element = input 
            ## Потом раскомментить и доработать
            def input_value_getter(): 
                if element.output is None: 
                    input_value = 0 
                else: 
                    input_value = element.output 
                return input_value  
            # def input_value(self):
            #     return self.__input.output 
            # input_value = property(input_value_getter) 
            # self.__input_value = input_value 
            # self.__input_value.fget = self.__input_value_getter 
            # self.__input_value = self.input_value_getter 
            # input как функция 
        ## Потом раскомментить и доработать: 
        elif callable(input): 
            input_func = input
            def input_value_getter(): 
                input_value = input_func
                return input_value 
        else: 
            def input_value_getter(): 
                return input 
        return input_value_getter
            # def input_value(self, *args, **kwargs):
            #     return self.__input(*args, **kwargs)
        # self.input_value = input_value_getter(self)
          
            
    def __input_proceeding(self, input): 
        def single_input_proceeding(input): # Функция обработки сигнала из одного источника
            if isinstance(input, (Element)): 
                if input.output is None: 
                    return 0 
                else: 
                    return input.output # FIXME: Здесь проблема!
            else:  
                if callable(input): 
                    print("Achtung: input — это функция!") # В рамках класса element такой input обрабатывается через жопу
                    try: 
                        print(self.t) 
                    except AttributeError: 
                        print("Параметр t не был передан")
                    try:
                        print(self.pars) # FIXME: Найти эти параметры!
                    except AttributeError: 
                        print("Доп. параметров для функции input не существует")
                elif input is None: 
                    return 0 
                return input # FIXME: Дописать обработку всякой хрени, если input не является float'ом или функцией  
        
        def multiple_input_proceeding(input): # FIXME 
            input_proceeded = list((0,)* len(input)) 
            for source in input:
                input_proceeded[input.index(source)] = single_input_proceeding(source)
            return sum(input_proceeded) # Achtung! Выполняю втупую суммирование входных сигналов
        
        if isinstance (input, tuple): 
            return multiple_input_proceeding(input) 
        else: 
            return single_input_proceeding(input)

    def __str__(self): 
        if self.__name is None: 
            return super().__str__()
        else: 
            return self.__name     
    
    def __del__(self): 
        pass # FIXME Прописать, что там должно происходить 

