from numpy import * 
from src.matrix import * 

class Element: 

    matrix = None # ссылка на матрицу 
    index = None # порядковый номер в матрице 
    type = None # тип элемента (нейрон, мышца, рецептор) 
    eq_num = 0 # число уравнений в модели
    input = None # входной сигнал
    
    # Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        print("Вызов __new__ для " + str(cls)) 
        if cls.matrix == None: 
            print("Матрица связности для класса Element ещё не создана") 
        # создать matrix
        cls.matrix = kwargs['matrix']
        cls.matrix.refill(kwargs['input'])
        return super().__new__(cls)
    
    # Это вызовется после создания объекта класса:
    def __init__(self, **kwargs):  
        print("вызов __init__ для " + str(self)) 
        self.input = kwargs['input']
    
    # А это хз когда вызывается, но это должен быть сплав первого и второго
    def __call__(self): 
        print("вызов __call__ для " + str(self))
    
