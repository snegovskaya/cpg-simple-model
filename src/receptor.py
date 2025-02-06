from src.element import Element 

class Receptor(Element): 
    """
    A spindle model taken from Matthews & Stein (1969). Laplace notation is used.
    """ 
    r = 1 # s^{-1}, instant frequency of receptor's spiking 
    __F = 0
    k = 1 # unitless, coefficient for namely this receptor model 
    phi = 1 # unitless, phase of receptor's spiking 
    A = 1 # mV, amplitude of receptor's spiking 
    u = 0 # mV 
    __I = 0, # mkA
    # input = F(t), Н  
    output = 0 # I(t), мА 


    ## Геттеры и сеттеры: 
    @property 
    def output(self): 
        self.__output = self.I()
        return self.__output 
    

    @property 
    def F(self): 
        return self.__F 
    
    @F.setter #  FIXME: Временный костыль
    def F(self, F_meaning): 
        self.__F = F_meaning


    def __init__(self, **kwargs): 
        super().__init__(**kwargs) # Вызов __init__'а из Element 
        # F = self.input # FIXME: Раскомментировать потом!!!
    
    @ property 
    def I(self): 
        # return self.r() 
        return 2 * self.F # Тестовое значение 
    
    @ property 
    def output(self): 
        self.__output = self.I 
        return self.__output 

    def get_x(self): 
        self.x = self.F 
        return self.x 

    def x_Laplace(self): 
        pass 

    ## r через Лапласа — т.е. r(s): 
    def r(self, s=1): ## FIXME: s откуда и на каком этапе добывается?
        k = self.k 
        x = self.x 
        r = k*x*(s + 10)  
        return r 

    # ## r через x, dx_dt: 
    # def get_r(self): 
    #     print(self.input_node)

    def r_Laplace_inverse(self): 
        k = self.k 
        x = self.x
        dx_dt = 0 ## FIXME 
        r = k*x*(dx_dt + x) 
        return r 

    def get_I(self): 
        pass

    # def model_Laplace(self): # Возвращает модель рецептора в Лапласовской нотации
    #     return k * x * (s + 10) # r(s) = kx(s + 10)
    
    

if __name__ == "main": 
    import numpy as np
    receptor = Receptor(input = np.sin)