from numpy import * 
from matrix import * 

class Element: 

    # Интуитивно — хорошо бы иметь у него поле type 
    # Совершенно обязательно — поле input 
    # Возможно — ссылку на матрицу 
    # Возможно — кол-во диффуров в его модели 
    # Обязательно — порядковый номер

    # Это вызовется перед созданием объекта класса:
    def __new__(cls, *args, **kwargs): 
        print("вызов __new__ для " + str(cls)) 
        #  if matrix для этой серии элементов ещё не создан: 
        # создать matrix
        matrix = kwargs['matrix']
        matrix.refill(1)
        return super().__new__(cls)
    
    # Это вызовется после создания объекта класса:
    def __init__(self, **kwargs):  
        print("вызов __init__ для " + str(self))
    
    # А это хз когда вызывается, но это должен быть сплав первого и второго
    def __call__(self): 
        print("вызов __call__ для " + str(self))
    

matrix = Matrix()
test_element1 = Element(matrix = matrix)
print(matrix.explicit)
test_element2 = Element(matrix = matrix)
print(matrix.explicit)
