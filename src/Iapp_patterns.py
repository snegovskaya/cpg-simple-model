def I_impulse(t: float, impulseAmpl = 5, impulseLength = 5, tStart = 1):
    if t > tStart and t < tStart + impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I 

def I_period_impulse(t: float, impulseAmpl = 5, impulseLength = 5, period = 10, tStart = 1, tFinish = 50): 
    if t > tFinish: 
        I = 0
    elif (t - tStart) % period <= impulseLength:
        I = impulseAmpl
    else:
        I = 0
    return I