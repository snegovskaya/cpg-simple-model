def muscle_test():
    print("I'm a Simplified Adapted Model muscle")
    return

def dX_dt(X, t):
    C_N = X[0]
    F = X[1]

    tau_c = 1 
    tau_1 = 1 
    k = 1 
    A = 1 
    m = 1 

    # по u ещё ни черта не понятно
    def u(t):
        return sin(t)

    eq_1 = - C_N/tau_c + u(t)

    def x(t):
        return C_N**m/(C_N**m + k**m)
    
    eq_2 = -F/tau_1 + A*x

    return array([eq_1, eq_2])
    
