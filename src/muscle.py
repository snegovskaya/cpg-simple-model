import numpy as np

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

    def __init__(self, t, CN0, F0):
        """ 
        Parameters:
        t : array of time points at those muscle response is observed 
        CN0 : array of CN(t) meanings in zero approximation 
        F0 : array of F(t) meanings in zero approximation 
        """
        self.test = 'I\'m class Muscle test' 

        self.t = t
        self.CN = CN0 
        self.F = F0 

    def eq_CN(self, u): 
        """
        ODE for CN variable
        FIXME Я пока ХЗ, откуда нужно брать и как сюда внедрять u 
        """
        CN = self.CN 
        tauc = self.tauc 
        t = self.t 

        return - CN / tauc + u(t) 

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
        ODE for F variable
        """
        F = self.F 
        tau1 = self.tau1 
        A = self.A 
        x = self.x()
        return - F / tau1 + A * x


    # System of ODEs
    def dX_dt(X, t): # Возможно, лучше заменить на model
        'FIXME: Добавить нормальное описание '

        #Constants
        tauc = 0.1 #c
        tau1 = 0.1 
        k = 5
        A = 10 
        m = 2

        CN = X[0]
        F = X[1] 

        # по u ещё ни черта не понятно
        def u(t):
            return abs(np.sin(t * 2))

        eq_1 = - CN/tauc + u(t)

        def x(t):
            return CN**m/(CN**m + k**m)
        
        eq_2 = - F/tau1 + A*x(t)

        return np.array([eq_1, eq_2])
    
