from numpy import *

def muscle_test():
    print("I'm a Simplified Adapted Model muscle")
    return

class Muscle: 
    # Simplified Adapted Model (see Wilson2013)

    tauc = 0.1 # FIXME units! 
    tau1 = 0.1 # FIXME units! 
    tau2 = 0 # FIXME units! 
    k =  5 # FIXME units! 
    A = 10 # FIXME units! 
    m = 2 # dim-less 

    def __init__(self, CN0, F0, u): # FIXME: В каком формате передавать u? Как название ф-ции?
        """ 
        Parameters:
        CN0 : initial CN(t) meaning 
        F0 : initial F(t) meaning 
        u : input voltage function 
        """

        self.test = 'I\'m class Muscle test' 

        self.CN = CN0 
        self.F = F0 
        self.u = u # 1. FIXME Но это не точно; 2. Зависимость от t сюда вроде как писать не нужно 

    def eq_CN(self, t): 
        """
        Right part of an ODE for CN variable
        FIXME Я пока ХЗ, откуда нужно брать и как сюда внедрять u 
        """
        CN = self.CN 
        tauc = self.tauc 
        u = self.u 

        return - CN / tauc + u(t) 
        # FIXME: вообще, по-хорошему, должно быть u(*args) или что-то типа того

    def x(self):
        """
        Function x(CN)
        """
        CN = self.CN 
        m = self.m 
        k  = self.k 

        return CN ** m / (CN ** m + k ** m)

    def eq_F(self): 
        """
        Right part of an ODE for F variable
        """
        F = self.F 
        tau1 = self.tau1 
        A = self.A 
        x = self.x()
        return - F / tau1 + A * x


    # System of ODEs
    def model(self, t): #
        'Collects ODEs in one system'

        eq_1 = self.eq_CN(t)
        eq_2 = self.eq_F()

        return array([eq_1, eq_2])
    
