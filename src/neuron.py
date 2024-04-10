def neuron_test():
    print("I'm a HH neuron")
    return

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

class Neuron: 
    # Standart Hodgkin-Huxley model with the parameters got from https://neuronaldynamics.epfl.ch/

    gNa = 40 # FIXME: units! 
    gK = 35 # FIXME: units! 
    gL = 0.3 # FIXME: units! 
    ENa = 55 # FIXME: units! 
    EK = -77 # FIXME: units! 
    EL = -65 # FIXME: units! 
    C = 1 # FIXME: units! 


    def __init__(self, v0, m0, n0, h0, **kwargs): 
        """ 
        Args: 
            v0 (float): initial v meaning 
            m0 (float): initial m meaning 
            n0 (float): initial n meaning 
            h0 (float): initial h meaning
        """
        self.v = v0 
        self.m = m0 
        self.n = n0 
        self.h = h0 

        self.IappFunc = kwargs.pop('input')
        self.IappPars = kwargs
  
  
    def eq_v(self): 
        """
        Returns: 
           callable OR float: right part of an ODE for v variable
        """
        gNa = self.gNa 
        gK = self.gK 
        gL = self.gL 
        ENa = self.ENa 
        EK = self.EK 
        EL = self.EL 
        C = self.C 

        v = self.v 
        m = self.m 
        n = self.n 
        h = self.h 

        IappFunc = self.IappFunc 
        IappPars = self.IappPars
    
        if callable(IappFunc):
            return (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + IappFunc(**IappPars)) * 1/C
        else:
            return (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + IappFunc) * 1/C 


    def __eq_x(self, x, ax, bx): 
        """
        Returns: 
            ?
        """
        # return Cx * exp(-(ax + bx) * t) + ax/(ax + bx) Это ж решение с v в качестве параметра! Мне-то нужно исходное уравнение!
        return ax * (1 - x) - bx * x 
  
  
    def am(self): 
        """
        Returns: 
           float: $alpha_m$ parameter for given v meaning
        """
        v = self.v 
        # return 0.1 * (v + 25) * 1/(exp((v + 25)/10) - 1) # По HodgkinHuxley1952
        return 0.182 * (v + 35) * 1/(1 - exp(-(v + 35)/9)) 
  
    def bm(self): 
        """
        Returns: 
           float: $beta_m$ parameter for given v meaning
        """
        v = self.v 
        # return 4 * exp(v/18) # По HodgkinHuxley1952
        return -0.124 * (v + 35) * 1/(1 - exp((v + 35)/9))

    def an(self): 
        """
        Returns: 
           float: $alpha_n$ parameter for given v meaning
        """
        v = self.v 
        # return 0.01 * (v + 10) * 1/(exp((v + 10)/10) - 1) # По HodgkinHuxley1952
        return 0.02 * (v - 25) * 1/(1 - exp(-(v - 25)/9)) 
  
    def bn(self): 
        """
        Returns: 
           float: $beta_n$ parameter for given v meaning
        """
        v = self.v 
        # return 0.125 * exp(v/80) # По HodgkinHuxley1952
        return -0.002 * (v - 25) * 1/(1 - exp(v - 25)/9) 

    def ah(self): 
        """
        Returns: 
           float: $alpha_h$ parameter for given v meaning
        """
        v = self.v
        # return 0.07 * exp(v/20) # По HodgkinHuxley1952
        return 0.25 * exp(-(v + 90)/12) 

    def bh(self): 
        """
        Returns: 
           float: $beta_h$ parameter for given v meaning
        """
        v = self.v
        # return 1/(exp((v + 30)/10) + 1) # По HodgkinHuxley1952
        return 0.25 * exp((v + 62)/6) / exp((v + 90)/12)
  

    def eq_m(self): 
        """
        Returns: 
           callable OR float: right part of an ODE for m variable
        """
        v = self.v 
        m = self.m 
        am = self.am() 
        bm = self.bm() 
        return self.__eq_x(m, am, bm) 
  
    def eq_n(self): 
        """
        Returns: 
           callable OR float: right part of an ODE for n variable
        """
        v = self.v 
        n = self.n 
        an = self.an() 
        bn = self.bn() 
        return self.__eq_x(n, an, bn) 
  
    def eq_h(self): 
        """
        Returns: 
           callable OR float: right part of an ODE for h variable
        """
        v = self.v 
        h = self.h 
        ah = self.ah() 
        bh = self.bh() 
        return self.__eq_x(h, ah, bh) 


    def model(self): 
        """
        Returns: 
           array: [self.eq_v, self.eq_m, self.eq_n, self.eq_h]
        """
        eq_1 = self.eq_v() 
        eq_2 = self.eq_m() 
        eq_3 = self.eq_n() 
        eq_4 = self.eq_h() 
        return array([eq_1, eq_2, eq_3, eq_4])

def delegate_neuron(obj, vars, t): 
    obj.v = vars[0] 
    obj.m = vars[1] 
    obj.n = vars[2] 
    obj.h = vars[3] 
    if obj.IappPars.get('t') != None: 
        obj.IappPars['t'] = t 
    return obj.model()

