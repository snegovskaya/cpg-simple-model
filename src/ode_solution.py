from numpy import array, zeros 
from src.net import Net
from src.neuron import Neuron
from src.muscle import Muscle 
from scipy.integrate import odeint


## ------------- Наброски функционала ------------- 

# N_eq = sum(element.eq_num for element in net.elements_list) 
# variables_array = zeros(1, N_eq)
# ode_array = zeros(1, N_eq)  # FIXME: Переименовать, возможно 

class ODE_system(Net): ## ACHTUNG!! Завела для системы диффуров отдельный класс!!

    @property # FIXME 
    def vars(self): 
        self.__vars = [] # FIXME Но нам же не надо опустошать массив каждый раз, да?..
        for element in self.elements_list: 
            if element.vars == None: 
                pass # FIXME А может быть так, что в списке переменных ничего нет? 
            else: 
                self.__vars += [*element.vars] 
        return self.__vars 
    
    @vars.setter # FIXME: прописать, что он делает, — а то я уже забыла 
    def vars(self, vars): 
        from src.receptor import Receptor # FIXME: только для отладки!
        for element in self.elements_list: 
            if not isinstance(element, Receptor):
                slice_size = len(element.vars) 
                vars_to_load = vars[0:slice_size] 
                element.vars = vars_to_load # FIXME 
                vars = vars[slice_size:] 

    @property # FIXME: криво написано, с кривыми названиями 
    def ode_system(self, vars, t): 
        self.vars = vars
        result = [] # FIXME 
        for element in self.elements_list: 
            if element.model == None:
                print("I_rec = ",element.output)
            else: 
                result.extend(element.model(t))
        self.__ode_system = result 
        return self.__ode_system 
    

    def generate_vars_list(self): # FIXME: Дублирование с геттером! 
        self.__vars = [] # FIXME 
        for element in self.elements_list: 
            try: 
                self.__vars.extend(element.vars) # Обработка исключения, если напоролись на рецептор
            except: 
                continue
        return self.__vars

    def generate_ode_system(self): # FIXME: аргументы... 
        from src.receptor import Receptor # FIXME: только для отладки!
        def ode_system(vars, t): 
            self.vars = vars
            result = [] # FIXME 
            for element in self.elements_list: 
                if isinstance(element, Receptor): # FIXME: Отладочное условие!
                    print("I_rec = ",element.output)
                else: 
                    result.extend(element.model(t))
            return result
        self.ode_system = ode_system 
        return self.ode_system 
    


def ode_solution(net, t): 
    net.vars = net.generate_vars_list() # FIXME: Костыли сраные!
    net.ode_system = net.generate_ode_system()
    result = odeint(net.ode_system, net.vars, t) # Добавить поля в класс
    return result


def delegate_Muscle(obj, vars, t, **kwargs): # Нужно ли сюда именно впихивать t? 
    obj.CN = vars[0] 
    # print(obj.CN) # Убрать потом
    obj.F = vars[1] 
    obj.u = kwargs.pop('input') # Леплю говно
    if  obj.upars.get('t') != None: 
        obj.upars['t'] = t # Химичим с t 
        # FIXME Что-то там было про переписать upars[t]
    return obj.model()

def delegate_Neuron(obj, vars, t): 
    obj.v = vars[0] 
    print('v = ', obj.v) # Убрать потом 
    obj.m = vars[1] 
    obj.n = vars[2] 
    obj.h = vars[3] 
    if obj.IappPars.get('t') != None: 
        obj.IappPars['t'] = t 
    return obj.model()


def delegate (obj, vars, t):
    if isinstance(obj, Neuron): 
        delegate_Neuron(obj, vars, t)
    elif isinstance(obj, Muscle): 
        delegate_Neuron(obj, vars, t)


'''Вопрос: что мы хотим интегрировать? 
Это должен быть какой-то такой вид: 
integrate.odeint(circuit_ODE, vars, t)
?

Если да, то тогда надо сразу забивать под неё матрицу
'''