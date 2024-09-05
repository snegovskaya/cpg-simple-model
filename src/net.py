from typing import Any # FIXME Что ето и откуда ето взялось?
import numpy as np 

# Забубённое «Зато типа по-правильному»: 
class MetaSingleton(type): # Метакласс для переопределения метода __call__ при вызове класса Net
    __instance = None 
    def __call__(cls, *args, **kwargs): 
        if cls.__instance == None: 
            cls.__instance = super().__call__(*args, **kwargs) 
            # type.__call__(cls, base, attrs)
            # type(cls, Metasingleton, (dim, __current_index, ...)) 
        return cls.__instance

class Net(metaclass = MetaSingleton): 
    __dim = 0 # размерность = кол-во эл-тов системы 
    __current_index = None # указатель текущего эл-та FIXME Возможно, стоит сделать его -1
    # __instance = None # атрибут, показывающий, что экземпляр матрицы уже существует (singleton) 
    __initialized = False # индикатор того, что объект класса инициализирован FIXME Ето костыль, призванный помочь жопе
    __matrix = list(list()) # явный вид матрицы (2D-массив) # FIXME Возможно, надо переделать
    
    
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
    def matrix(self): 
        return self.__matrix 
    
    @matrix.setter # А нужен ли?
    def matrix(self, matrix): 
        self.__matrix = matrix 

    ## В качестве альтернативы — переопределение метода __call__ для класса

    # def __new__(cls, *args, **kwargs): 
    #     if cls.__instance is None: # Паттерн Singletone
    #         cls.__instance = super().__new__(cls) 
    #     return cls.__instance 

    ## Ниже — собсна сабж, трэш и угар: 

    # def __call__(cls, *args, **kwargs): 
    #     if cls.__instance == None: 
    #         cls.__instance = cls.__new__(cls, *args, **kwargs) 
    #         cls.__init__(cls.__instance, *args, **kwargs) 
    #         return cls.___instance 


## Костыльное решение через __initialized:
    # def __init__(self, *args): # Проблемное местечко, может потребоваться FIXME 
    #     if self.__initialized == True: # FIXME Юзаю костыль
    #         pass
    #     elif args == (): # FIXME надо думать 
    #         self.__dim = 0 
    #         self.__initialized = True 
    #     else: 
    #         self.__dim = args[0] 
    #         self.__matrix = np.zeros((self.__dim, self.__dim)) # Если размерность сети известна заранее, то переделать список в массив 
    #         self.__initialized = True 
    #     self.__current_index = None  
    #     print(self.__matrix) # FIXME: убрать потом 

## Решение для той мудроты с метаклассами: 
    def __init__(self, *args): 
        self.__dim = args[0] 
        self.__matrix = np.zeros((self.__dim, self.__dim))
        self.__current_index = None # FIXME: вангую какую-нибудь херотень в граничных случаях
        print(self.__matrix) # FIXME: убрать потом 

    def __del__(self): 
        self.__class__.__instance = None # FIXME: возможно, это норм, но не факт

    def __str__(self): 
        return f"{self.__matrix}" 
    
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
    def add_element(self, element, **kwargs): # Добавление нового элемента 
        try:
            input = kwargs['input']
        except KeyError: 
            print("На input ничего не поступало")
        
        self.__next__() 

        def get_input_indices(input): 
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
        input_indices = get_input_indices(input) # FIXME см. ниже: привела к единому виду
        try: 
            for input_index in input_indices: # FIXME: нужна проверка, что input_indices — это tuple!
                # или сделать программу с вариативным поведением для одного или для нескольких input'ов
                self.__matrix[self.__current_index][input_index] = 1 
        except TypeError: 
            if input_indices in (0, int):
                print("input сейчас — это одна чиселка")
                input_index = input_indices
                self.__matrix[self.__current_index][input_index] = 1
            else: 
                pass
        return self.__matrix
    
    # Функции ниже скорее относятся к модулю net:


    