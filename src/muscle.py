from numpy import array 
from src.element import Element

class Muscle(Element): 
    # Simplified Adapted Model (see Wilson2013 Eqs. 5–7)

    tauc = 0.02 * 1e3 #  s --> ms # FIXME Нахимичила с единицами измерения!!
    tau1 = 0.05 * 1e3 # s --> ms # FIXME -//-
    # tau2 = 50 # ms # Он тут не фигурирует
    k =  0.5 # FIXME -//- 
    A = 2.5 # хз --> N * ms 
    m = 2 # unitless 

    ## Геттеры и сеттеры: 
    @property 
    def eq_num(self): 
        return self.__eq_num 
    
    @eq_num.setter 
    def eq_num(self, eq_num): 
        self.__eq_num = eq_num 

    @property # FIXME
    def vars(self): 
        self.__vars = self.CN, self.F 
        return self.__vars 

    @vars.setter 
    def vars(self, vars): 
        self.CN, self.F = vars
        self.__vars = vars 

    @property # Это пока без геттера и сеттера
    def u(self): 
        return self.input 
    
    # @u.setter
    # def u(self, u): 


    def __init__(self, CN0 = 0, F0 = 0, **kwargs): # FIXME: В каком формате передавать u? Как название ф-ции?
        """ 
        Args: 
            CN0 (float): Initial CN(t) meaning 
            F0 (float): Initial F(t) meaning  
            **kwargs (dict): 
                kwargs.input (float OR callable): Input voltage meaning OR function 
                kwargs.pop('input'): Arbitrary args to pass the 'input' function 
        """ 

        super().__init__(self, **kwargs) # Вызов __init__'а из Element 

        self.eq_num = 2 
        self.CN = CN0 
        self.F = F0 
        self.vars = self.CN, self.F 
        # self.u = self.input # Вернуть как было! 
        # self.u = self.input
        self.upars = kwargs # 1. FIXME Но это не точно; 2. Зависимость от t сюда вроде как писать не нужно 

    def eq_CN(self): 
        """
        Returns: 
            callable OR float: Right part of an ODE for CN variable 
        """
        CN = self.CN 
        tauc = self.tauc 
        u = self.u
        print("u = ", u)
        upars = self.upars

        if callable(u):
            return - CN / tauc + u(**upars) # Это должно быть u - u_rest 
        else: 
            print('eq_CN = ', - CN / tauc + u) # Убрать потом
            return - CN / tauc + u # FIXME Ерунда с константой!!
        # FIXME: вообще, по-хорошему, должно быть u(*args) или что-то типа того


    def x(self):
        """ 
        Returns: 
            callable OR float: Function x(CN)
        """
        CN = self.CN 
        m = self.m 
        k  = self.k 

        return CN ** m / (CN ** m + k ** m)


    def eq_F(self): 
        """ 
        Returns: 
        callable OR float: Right part of an ODE for F variable
        """
        F = self.F 
        tau1 = self.tau1 
        A = self.A 
        x = self.x()
        return - F / tau1 + A * x


    def model(self, *args): # FIXME
        """
        Collects ODEs in one system 

        Returns: 
            array: 
                [self.eq_CN, self.eq_F]
        """
        eq_1 = self.eq_CN()
        eq_2 = self.eq_F()

        return array([eq_1, eq_2])

def delegate_Muscle(obj, vars, t, **kwargs): # Нужно ли сюда именно впихивать t? 
    obj.CN = vars[0] 
    # print(obj.CN) # Убрать потом
    obj.F = vars[1] 
    obj.u = kwargs.pop('input') # Леплю говно
    if  obj.upars.get('t') != None: 
        obj.upars['t'] = t # Химичим с t 
        # FIXME Что-то там было про переписать upars[t]
    return obj.model()
    
