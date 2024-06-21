from numpy import *

class Matrix: 
    dim = 2 
    index = 0
    explicit = zeros((dim, dim)) 

    # Проверить, на всякий пожарный, что matrix всего один: 
    # — это если вдруг __new__ Element запустится без скрипта 

    # Клёво было бы, если matrix вызывается без ничего, выдавать matrix.explicit

    def refill(self, input_index): 
        self.explicit[self.index, input_index] = 1 
        self.index +=1
        return self.explicit

 