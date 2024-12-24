import numpy as np 
# from src.receptor import Receptor # FIXME: только для отладки!

## Метакласс для переопределения метода __call__ при вызове класса Net 
class MetaSingleton(type): 
    __instance = None 
    def __call__(cls, *args, **kwargs): 
        if cls.__instance is None: 
            cls.__instance = super().__call__(*args, **kwargs)  
        return cls.__instance

class Net(metaclass = MetaSingleton): 
    __dim = 0 # размерность = кол-во эл-тов системы 
    __current_index = None # указатель текущего эл-та FIXME Возможно, стоит сделать его -1 
    __elements_list = list() # список со ссылками на элементы сети
    __matrix = list(list()) # явный вид матрицы (2D-массив) 
    # FIXME: Вписать сюда vars и ode_system!

## Решение для той мудроты с метаклассами: 
    def __init__(self, *args): 
        self.dim = args[0] # FIXME поменяла на геттер
        self.elements_list = [None] * self.dim # FIXME поменяла на геттер
        self.__matrix = np.zeros((self.__dim, self.__dim))
        self.__current_index = None # FIXME: вангую какую-нибудь херотень в граничных случаях
        print(self.__matrix) # FIXME: убрать потом 

    def __del__(self): 
        self.__class__.__instance = None # FIXME: возможно, это норм, но не факт

    def __str__(self): 
        return f"{self.__matrix}"

    ## Геттеры и сеттеры: 
    @property
    def dim(self): 
        return self.__dim 
    
    @dim.setter 
    def dim(self, dim): 
        self.__dim = dim 

    @property
    def current_index(self): 
        return self.__current_index 
    
    @current_index.setter 
    def current_index(self, current_index): 
        self.__current_index = current_index 

    @property 
    def elements_list(self): 
        return self.__elements_list 
    
    @elements_list.setter 
    def elements_list(self, elements_list): 
        self.__elements_list = elements_list
    
    @property
    def matrix(self): 
        return self.__matrix 
    
    @matrix.setter # А нужен ли?
    def matrix(self, matrix): 
        self.__matrix = matrix  
    
        # А дальше — куча всякой фигни 


    ## Всякие стрёмные недореализованные функции: 
    
    def __iter__(self): # Для итерирования по матрице 
        pass 

    def __next__(self): # Получение следующего элемента; в итоге будет юзаться какой-то из этих двух методов
        if self.__current_index == 0 or isinstance(self.__current_index, int): 
            if self.__current_index < self.__dim: 
                self.__current_index += 1 
            else:
                print("АШЫПКА! Вывалились за границы сети!") 
        else:
            self.__current_index = 0 # FIXME: тут могут быть подводные камни 
            print(self.current_index) 
        return self.__current_index

    ## Добавление нового элемента 
    # FIXME: Тут щас творится полная жопа! 

    def __add_element_in_list(self, element): 
        self.elements_list[self.current_index] = element # Тут тоже заменяю приватный атрибут на его геттер
        return self.elements_list 
    
    def __add_element_in_matrix(self, element): # Добавление нового элемента 
        # try:
        #     input = kwargs['input']
        # except KeyError: 
        #     print("На input ничего не поступало") 


        def get_input_indices(input): #FIXME: Где-то здесь проблема с inputом: он сейчас передаётся как число!
            try:
                if isinstance(input, tuple):
                    return tuple(map(input.index, input)) 
                else: 
                    return input.index
            except AttributeError: 
                return None
        
        # for input_index in input.index: 
            # <Везде проставить единички>
        
        # Аыаыаы, пошёл крепкий алкоголь...
        input_indices = get_input_indices(element.input_node) # FIXME см. ниже: привела к единому виду
        try: 
            for input_index in input_indices: # FIXME: нужна проверка, что input_indices — это tuple!
                # или сделать программу с вариативным поведением для одного или для нескольких input'ов
                self.matrix[self.current_index][input_index] = 1 # Приватный параметр на геттер
        except TypeError: 
            if type(input_indices) is int: # FIXME!!! 
                print("input сейчас — это одна чиселка")
                input_index = input_indices
                self.matrix[self.current_index][input_index] = 1
            else: 
                pass
        return self.matrix 
    
    def add_element(self, element): 
        self.__next__()
        self.__add_element_in_list(element)

    # Чтобы исправить задание матрицы # FIXME: Полностью переписать!
    def set_matix(self): 
        self.__current_index = None 
        for element in self.__elements_list: 
            self.__next__()
            self.__add_element_in_matrix(element)
    
    



    