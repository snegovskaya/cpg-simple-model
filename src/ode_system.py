from numpy import array, zeros 
from src.net import Net
from src.neuron import Neuron
from src.muscle import Muscle 
from scipy.integrate import odeint


## ------------- Наброски функционала ------------- 

# N_eq = sum(element.eq_num for element in net.elements_list) 
# variables_array = zeros(1, N_eq)
# ode_array = zeros(1, N_eq)  # FIXME: Переименовать, возможно 

class ODE_system(): # FIXME: Пока делаю его без наследования от Net 

    test_var = "I'm ODE_system class"

    def __init__(self): 
        print("Инициализация класса ODE_system")
        # super().__init__(self) # Вот здесь собака зарыта! 
        self.net = Net(1) 
        self.elements_list = self.net.elements_list 
        self.__vars = [] 
        self.__right_part = [] 

    def set_inputs(self): 
        for element in self.elements_list: 
            element.set_input()

    @property # FIXME
    def vars(self): 
        """ 
        Геттер для приватной переменной __vars: 
        - Проходится по всем элементам сети; 
        - Добывает __vars из каждого элемента; 
        - Сводит добытое в итоговый список для всей системы; 
        - Возвращает этот список. 
        """ 
        self.__vars = [] # FIXME Но нам же не надо опустошать массив каждый раз, да?..
        for element in self.elements_list: 
            if element.vars == None: 
                pass # FIXME А может быть так, что в списке переменных ничего нет? 
            else: 
                self.__vars += [*element.vars] 
        return self.__vars 
    
    @vars.setter  
    def vars(self, vars): 
        """ 
        Сеттер для приватной переменной (свойства) __vars: 
        - Раскидывает переданные ему значения vars по всем элементам сети
        """ 
        for element in self.elements_list: 
            if element.model == None: 
                pass # FIXME: обработать исключение 
            else: 
                slice_size = len(element.vars) 
                vars_to_load = vars[0:slice_size] 
                element.vars = vars_to_load # FIXME 
                vars = vars[slice_size:] 

    def right_part(self, *args, **kwargs): # FIXME: аргументы... 
        def right_part_inner(vars, t): 
            self.vars = vars
            result = [] # FIXME 
            for element in self.elements_list: 
                if element.model == None: 
                    print("игнорируется эл-т без диффура...") 
                else: 
                    result.extend(element.model(t))
            return result
        self.__right_part = right_part_inner 
        return self.__right_part
    

    def generate_ode_system(self): # FIXME: аргументы... 
        self.set_matrix(input = input)
        def ode_system(vars, t): 
            self.vars = vars
            result = [] # FIXME 
            for element in self.elements_list: 
                result.extend(element.model(t))
            return result
        self.ode_system = ode_system 
        return self.ode_system 

    def generate_vars_list(self): # FIXME: Дублирование с геттером! 
        self.__vars = [] # FIXME 
        for element in self.elements_list: 
            try: 
                self.__vars.extend(element.vars) # Обработка исключения, если напоролись на рецептор
            except: 
                continue
        return self.__vars

 
    
    

    def solution(self, t): # FIXME: Всё перекурочено! 
        result = odeint(self.right_part(), self.vars, t) # FIXME 
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

if __name__ == "__main__": 
    test_net = Net(1)
    test_ode_system = ODE_system() 
    print("test_ode_system works!")