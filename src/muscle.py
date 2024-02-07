import numpy as np

def muscle_test():
    print("I'm a Simplified Adapted Model muscle")
    return

#Simplified Adapted Model (see Wilson2013)

# ODEs
def dX_dt(X, t): # Возможно, лучше заменить на model
    'FIXME: Добавить нормальное описание '

    #Constants
    tau_c = 0.1 
    tau_1 = 0.1 
    k = 5
    A = 10 
    m = 2

    C_N = X[0]
    F = X[1] 

    # по u ещё ни черта не понятно
    def u(t):
        return np.sin(t)

    eq_1 = - C_N/tau_c + u(t)

    def x(t):
        return C_N**m/(C_N**m + k**m)
    
    eq_2 = -F/tau_1 + A*x(t)

    return np.array([eq_1, eq_2])
    
