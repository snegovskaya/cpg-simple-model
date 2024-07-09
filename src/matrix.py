from numpy import *

class Matrix: 
    dim = 2 
    index = 0
    explicit = zeros((dim, dim))  
    __instance = None # атрибут, показывающий, что экземпляр матрицы уже существует 
    
    # Проверить, на всякий пожарный, что matrix всего один: 
    # — это если вдруг __new__ Element запустится без скрипта 

    def __new__(cls, *args, **kwargs): 
        if cls.instance is None: 
            cls.instance.__ = super().__new__(cls) 
        return cls.__instance 
    

    def __del__(self): 
        Matrix.__instance = None 
        


    # Клёво было бы, если matrix вызывается без ничего, выдавать matrix.explicit

    def refill(self, input_index): 
        self.explicit[self.index, input_index] = 1 
        self.index +=1
        return self.explicit

 