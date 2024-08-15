from typing import Any # FIXME Что ето и откуда ето взялось?
import numpy as np

class Net: 
    __dim = 0 # размерность = кол-во эл-тов системы 
    __current_index = None # указатель текущего эл-та FIXME Возможно, стоит сделать его -1
    __instance = None # атрибут, показывающий, что экземпляр матрицы уже существует (singleton) 
    __initialized = False # индикатор того, что объект класса инициализирован FIXME Ето костыль, призванный помочь жопе
    __matrix = list(list()) # явный вид матрицы (2D-массив) # FIXME Возможно, надо переделать
    
    
    ## В качестве альтернативы — переопределение метода __call__ для класса

    def __new__(cls, *args, **kwargs): 
        if cls.__instance is None: # Паттерн Singletone
            cls.__instance = super().__new__(cls) 
        return cls.__instance 

    ## Ниже — собсна сабж, трэш и угар: 

    # def __call__(cls, *args, **kwargs): 
    #     if cls.__instance == None: 
    #         cls.__instance = cls.__new__(cls, *args, **kwargs) 
    #         cls.__init__(cls.__instance, *args, **kwargs) 
    #         return cls.___instance 

    def __init__(self, *args): # Проблемное местечко, может потребоваться FIXME 
        if self.__initialized == True: # FIXME Юзаю костыль
            pass
        elif args == (): # FIXME надо думать 
            self.__dim = 0 
            self.__initialized = True 
        else: 
            self.__dim = args[0] 
            self.__matrix = np.zeros((self.__dim, self.__dim)) # Если размерность сети известна заранее, то переделать список в массив 
            self.__initialized = True 
        self.__current_index = None  
        print(self.__matrix) # FIXME: убрать потом 

    def __del__(self): 
        self.__class__.__instance = None # FIXME: возможно, это норм, но не факт

    def __str__(self): 
        return f"{self.__matrix}" 
    
    def add(self): 
        if self.__current_index < self.__dim:
            pass # FIXME 
        self.__сurrent_index += 1 
        # А дальше — куча всякой фигни 


    # Всякие стрёмные недореализованные функции: 
    
    def __iter__(self): # Для итерирования по матрице
        pass 

    def refill(self, input_index): # Добавление нового элемента
        self.__matrix[self.__current_index, input_index] = 1 
        self.__current_index +=1 #FIXME: Не лучше ли наоборот? 
        return self.__matrix
    
    # Функции ниже скорее относятся к модулю net:

    def get_element(self, index): 
        pass

    