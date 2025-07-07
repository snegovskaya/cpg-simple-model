from numpy import exp, array
from src.element import Element # from element import Element 

class Neuron(Element): 
    """
    # Standart Hodgkin-Huxley model with the parameters got from https://neuronaldynamics.epfl.ch/ (NeuronalDynamics) book 
     and original HodgkinHuxley1952 article 

    Attributes: 
        gNa (float): [mS / cm^2] — Na+ channel conductance 
        gK (float): [mS / cm^2] — K+ channel conductance 
        gL (float): [mS / cm^2] — leak conductance 
        ENa (float): [mV] — Na+ channel displacement from resting potential 
        EK (float): [mV] — K+ channel displacement from resting potential 
        EL (float): [mV] — leak channel displacement from resting potential 
        C (float): [mkF / cm^2] — membrane capacity 
    """
    gNa = 40 
    gK = 35 
    gL = 0.3 
    ENa = 55  
    EK = -77 
    EL = -65 
    C = 1 
    
    ## И чтоб я помнила, откуда взялись эти начальные значения...
    v0 = -63.0540942 
    m0 = 0.06 
    n0 = 0.00 
    h0 = 0.54 

    ## Геттеры и сеттеры: 
    @property
    def output(self): # АЫАЫАЫ, FIXME!!! 
        self.__output = self.v - self.v0
        return self.__output 
    
    @output.setter # А нужно ли? 
    def output(self, output): 
        self.__output = output 

    @property 
    def eq_num(self): 
        return self.__eq_num 
    
    @eq_num.setter 
    def eq_num(self, eq_num): 
        self.__eq_num = eq_num 

    @property # FIXME
    def vars(self): 
        self.__vars = self.v, self.m, self.n, self.h 
        return self.__vars 

    @vars.setter 
    def vars(self, vars): 
        self.v, self.m, self.n, self.h = vars
        self.__vars = vars

    def __init__(self, v0 = -63.0540942, m0 = 0.06, n0 = 0.00, h0 = 0.54, **kwargs): 
        """ 
        Args: 
            v0 (float): [mv] — initial v meaning 
            m0 (float): [unitless in range [0,1]] — initial m meaning
            n0 (float): [unitless in range [0,1]] — initial n meaning
            h0 (float): [unitless in range [0,1]] — initial h meaning 
            **kwargs: keyword arguments for a neuron input  
                'input' (callable / float): obligatory v fuction or meaning input
        """

        super().__init__(**kwargs) # Вызов __init__'а из Element 

        self.eq_num = 4 

        self.v = v0 
        self.m = m0 
        self.n = n0 
        self.h = h0 
        self.vars = (v0, m0, n0, h0) # FIXME

        print("v = ", self.v) 
        print("m = ", self.m)
        print("n = ", self.n)
        print("h = ", self.h)
        print("vars = ", vars)# FIXME: Это взялось из ниоткуда — надо встроить его в общую канву

        self.output = self.v - self.v0 # FIXME 
        
        # FIXME: Исправить и раскомментировать!!!
        self.IappFunc = self.input # FIXME: тестово корректирую: добавила скобочки 
        # Хорошо бы проверку на callable выполнить именно здесь: 

        if callable(self.IappFunc): 
            print("Тута править нада!") 
        try: 
            self.IappPars = kwargs["pars"] # FIXME: Добыть параметры для функции! 
        except KeyError: 
            print("Либо задайте параметры _строго_ с ключевым словом \"pars\", либо идите лесом!")
            self.IappPars = {}

  
    def eq_v(self, *args, **kwargs): 
        """
        Returns: 
           callable / float: right part of an ODE for v variable, t-dependent or indepentent
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

        ## Обработка input'a с element'а: 
        
        t = args[0] # Жоский костыль пошёл 
        print("t = ", t) # Убрать потом 
    
        if callable(IappFunc): # Жоский FIXME!
            if __name__ ==  "src.neuron":
                print ('Iapp = ', IappFunc(t, **IappPars)) # Убрать потом 
            dv_dt = (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + IappFunc(t, **IappPars)) * 1/C
        else:
            dv_dt = (-(gNa * m**3*h*(v - ENa) + gK* n**4*(v - EK) + gL*(v - EL)) + IappFunc) * 1/C  
        print("dv_dt = ", dv_dt)
        return dv_dt

    def __eq_x(self, x, ax, bx): 
        """
        Returns: 
            callable: function template of m, n, h for inner usage
        """
        # return Cx * exp(-(ax + bx) * t) + ax/(ax + bx) Это ж решение с v в качестве параметра! Мне-то нужно исходное уравнение!
        dx_dt = ax * (1 - x) - bx * x 
        return dx_dt 
  
  
    def am(self): 
        """
        Returns: 
           float: $alpha_m$ parameter for given v meaning
        """
        v = self.v 
        # return 0.1 * (v + 25) * 1/(exp((v + 25)/10) - 1) # По HodgkinHuxley1952
        am = 0.182 * (v + 35) * 1/(1 - exp(-(v + 35)/9)) 
        return am
  
    def bm(self): 
        """
        Returns: 
           float: $beta_m$ parameter for given v meaning
        """
        v = self.v 
        # return 4 * exp(v/18) # По HodgkinHuxley1952
        bm = -0.124 * (v + 35) * 1/(1 - exp((v + 35)/9)) 
        return bm 

    def an(self): 
        """
        Returns: 
           float: $alpha_n$ parameter for given v meaning
        """
        v = self.v 
        # return 0.01 * (v + 10) * 1/(exp((v + 10)/10) - 1) # По HodgkinHuxley1952
        an = 0.02 * (v - 25) * 1/(1 - exp(-(v - 25)/9)) 
        return an 
  
    def bn(self): 
        """
        Returns: 
           float: $beta_n$ parameter for given v meaning
        """
        v = self.v 
        # return 0.125 * exp(v/80) # По HodgkinHuxley1952 
        bn = -0.002 * (v - 25) * 1/(1 - exp(v - 25)/9) 
        return bn 

    def ah(self): 
        """
        Returns: 
           float: $alpha_h$ parameter for given v meaning
        """
        v = self.v
        # return 0.07 * exp(v/20) # По HodgkinHuxley1952 
        ah =  0.25 * exp(-(v + 90)/12) 
        return ah 

    def bh(self): 
        """
        Returns: 
           float: $beta_h$ parameter for given v meaning
        """
        v = self.v
        # return 1/(exp((v + 30)/10) + 1) # По HodgkinHuxley1952 
        bh = 0.25 * exp((v + 62)/6) / exp((v + 90)/12) 
        return bh 
  

    def eq_m(self): 
        """
        Returns: 
           callable / float: right part of an ODE for m variable
        """
        m = self.m 
        am = self.am() 
        bm = self.bm() 
        dm_dt = self.__eq_x(m, am, bm) 
        print("dm_dt = ", dm_dt) 
        return dm_dt 
  
    def eq_n(self): 
        """
        Returns: 
           callable / float: right part of an ODE for n variable
        """
        n = self.n 
        an = self.an() 
        bn = self.bn() 
        dn_dt = self.__eq_x(n, an, bn) 
        print("dn_dt = ", dn_dt) 
        return dn_dt 
  
    def eq_h(self): 
        """
        Returns: 
           callable / float: right part of an ODE for h variable
        """
        h = self.h 
        ah = self.ah() 
        bh = self.bh() 
        dh_dt = self.__eq_x(h, ah, bh) 
        print("dh_dt = ", dh_dt)
        return dh_dt 


    def model(self, args): # FIXME: аргументы...
        """
        Returns: 
           array: [self.eq_v, self.eq_m, self.eq_n, self.eq_h]
        """ 
        eq_1 = self.eq_v(args) 
        eq_2 = self.eq_m() 
        eq_3 = self.eq_n() 
        eq_4 = self.eq_h() 
        return array([eq_1, eq_2, eq_3, eq_4])

# def delegate_Neuron(obj, vars, t): 
#     obj.v = vars[0] 
#     print('v = ', obj.v) # Убрать потом 
#     obj.m = vars[1] 
#     obj.n = vars[2] 
#     obj.h = vars[3] 
#     if obj.IappPars.get('t') != None: 
#         obj.IappPars['t'] = t 
#     return obj.model()
