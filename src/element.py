import numpy as np
from src.net import Net

class Element: 
    __name = None # уникальное имя элемента
    __net = None # ссылка на матрицу (сеть) 
    __index = None # порядковый номер в матрице (сети)
    __type = None # тип элемента (нейрон, мышца, рецептор) (пока без понятия, нужно или нет)
    __eq_num = 0 # число уравнений в модели 
    model = None # FIXME: Возможно, имеет смысл перевести её в приват и добавить геттеры / сеттеры 
    __vars = None
    __input = None # входной сигнал $ FIXME Аchtung: что делать, если входных сигналов несколько (дендриты)? 
    input_nodes = None # входные элементы в графе 
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
        if isinstance(self.input_nodes, (Element)):
            element =  self.input_nodes
            if element.output is None: 
                self.__input = 0 
            else: 
                self.__input = element.output 
        elif callable(self.input_nodes): 
            input_func = self.input_nodes
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

    ## Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        # Тут нужно такое: если в глобальном пространстве имён существует объект класса Net, то при каждом вызове new ссылку на него передавать по умолчанию 
        if not isinstance(cls.net, Net): # FIXME: В kwargs'ах-то net был!
            print("Ссылка на сеть для данного объекта класса Element отсутствует")
            # И теперь осталось по-нормальному создать сеть 
            cls.net = Net(1) # FIXME: Тут создаётся сеть размерности 1 (но это если до того вообще никакой сети не было) Вопрос: как её потом расширять при необходимости?
        return super().__new__(cls)
    
    ## Это вызовется после создания объекта класса:
    def __init__(self, *args, **kwargs):  # FIXME: Не знаю, насколько тут нужны *args 
        """ 
        kwargs - словарь, содержащий след. поля: 

        name – опционально; 
        input – в произвольном формате FIXME: это важно!
        """
        if 'name' in kwargs: 
            self.name = kwargs['name'] 
        else: 
            print("Текущий элемент безымянный")
        if 'input' in kwargs: 
            # FIXME: сделать предобработку input'a, чтобы input_nodes был массивом 
            self.input_nodes = self.primary_input_proceeding(kwargs['input']) # Видимо, без input_nodes пока не обойтись, и их с собственно input нужно разделять
        else: # FIXME: Надо поднять какую-нибудь ошибку 
            print("Для этого элемента нет input'a") 
            self.input_nodes = None 
        self.net.add_element(self) 
        self.index = self.net.current_index 
        # self.__primary_input_proceed(self.input_nodes) # FIXME: на рецепторе чего-то возвращает None 

    def primary_input_proceeding(self, input): 
        """ 
        Приведение входного сигнала, заданного в произвольной форме, 
        к единому формату списка 
        """ 
        if isinstance (input, tuple) or isinstance(input, list): 
            return list(input)
        else: 
            return list(input) 
        
    def input_proceeding(self, *args, **kwargs): 
        """ 
        Преобразование, делающее из информации о входных элементах итоговых входной сигнал
        """ 
        input_values = [] 
        for node in self.input_nodes: 
            if node is int: 
                pass 
            elif callable(node): 
                input_values.append(node(*args, **kwargs)) 
            elif isinstance(node, Element): 
                input_values.append(node.output) 
            return sum(input_values)

    def get_input_indices(self): 
        """ 
        Функция нужна, чтобы из всего, что загружается в input, 
        отидентифицировать непосредственно элементы
        """ 
        result = []
        for input_node in self.input_nodes: 
            if isinstance(input_node, Element): 
                result.append(input_node.index)
        return result 
    
    # @property  
    def input(self, *args, **kwargs): 
        """ 
        Очень сложный геттер для input'а, который должен срабатывать хрен знает когда
        """ 
        from src.neuron import Neuron # FIXME: убрать потом!
        # Давай так: оно должно возвращать функцию, которую если вызвать от t, то она сработает
        # Сейчас это полная копия input_proceeding
        input_values = [] 
        for node in self.input_nodes: 
            if (isinstance(node, int)) or (isinstance(node, float)):
                input_values.append(node)
            elif callable(node): 
                input_values.append(node(*args, **kwargs)) # FIXME
            elif isinstance(node, Element): 
                input_values.append(node.output) 
        if isinstance(self, Neuron):
            print("input_values: ", input_values)
        self.__input = sum(input_values) 

        return self.__input
#-------------------- ниже — неактуальные версии --------------------

    ## Я хз, лучше ли писать функцию по обработке input до или после __init__'а, 
    ## Но в любом случае, вот фукция по обработке __input__'а:  
        
    # Для kwargs['input'] --> element.input_nodes      
    def primary_input_proceeding(self, input): 
        ''' 
        На данный момент эта функция используется 
        для приведения input'а элемента в произвольной форме 
        к списку element.input_nodes
        ''' 
        if isinstance (input, list): 
            return input
        elif isinstance(input, tuple): 
            return list(input)
        else: 
            return [input]
        
    # Обработка input'а V.3: # FIXME: я запуталась, на каком месте распаковывать input_nodes и передавать дальше по ссылке или по значению? 
    def set_input(self): 
        for input_nodes in self.input_nodess: 
            print("input_nodes'ов много") 
        if isinstance(input_nodes, Element): 
            self.__input = input_nodes.output 
    # Или забить на начальные значения input'а и работать с ним только через сеттер?..
  
    
    def __multiple_input_proceeding(self, input): # FIXME Костыль! 
            input_proceeded = list((0,)* len(input)) 
            for source in input:
                input_proceeded[input.index(source)] = self.__single_input_proceeding(source)
            return sum(input_proceeded) # Achtung! Выполняю втупую суммирование входных сигналов

    def __single_input_proceeding(self, input): # Функция обработки сигнала из одного источника
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
          
    ## Устаревшая версия        
    # def input_proceeding(self, input): 
    #     def single_input_proceeding(input): # Функция обработки сигнала из одного источника
    #         if isinstance(input, (Element)): 
    #             if input.output is None: 
    #                 return 0 
    #             else: 
    #                 return input.output # FIXME: Здесь проблема!
    #         else:  
    #             if callable(input): 
    #                 print("Achtung: input — это функция!") # В рамках класса element такой input обрабатывается через жопу
    #                 try: 
    #                     print(self.t) 
    #                 except AttributeError: 
    #                     print("Параметр t не был передан")
    #                 try:
    #                     print(self.pars) # FIXME: Найти эти параметры!
    #                 except AttributeError: 
    #                     print("Доп. параметров для функции input не существует")
    #             elif input is None: 
    #                 return 0 
    #             return input # FIXME: Дописать обработку всякой хрени, если input не является float'ом или функцией  
        
    #     def multiple_input_proceeding(input): # FIXME 
    #         input_proceeded = list((0,)* len(input)) 
    #         for source in input:
    #             input_proceeded[input.index(source)] = single_input_proceeding(source)
    #         return sum(input_proceeded) # Achtung! Выполняю втупую суммирование входных сигналов
        
    #     if isinstance (input, tuple): 
    #         return multiple_input_proceeding(input) 
    #     else: 
    #         return single_input_proceeding(input)

    def __str__(self): 
        if self.__name is None: 
            return super().__str__()
        else: 
            return self.__name     
    
    def __del__(self): 
        pass # FIXME Прописать, что там должно происходить 

