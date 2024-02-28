from numpy import * 

def muscle_test():
    print("I'm a Simplified Adapted Model muscle")
    return

# ===== Nessessary technical feature ======
import weakref 

class WeakMethod: # Та самая приблуда для обхода циклических ссылок
    """
    Объектами класса (лучше бы назвать этот класс WeakAttribute, конечно)
    должны стать те стрёмные атрибуты CN и F, которые я 
    из своего изначального класса Muscle собираюсь вытащить
    """
    def __init__(self, attribute, instance):
        self.attribute = attribute 
        self.instance_ref = weakref.ref(instance) 

        # self.__wrapped__ # Есть в образце, но у меня  пока не прописан 

    def __call__(self):
        instance = self.instance_ref
        return self.attribute(instance)

    # def __repr__(self):
    #     # Тоже зачем-то нужен, но у меня тоже пока не прописан 
# =======================================   
    
# И теперь должно быть что-то типа того: 
class Muscle: 
    def __init__(self, CN0):
        self.CN = # FIXME
    
    def eq_CN(self, )
        

# То есть хотим так:
muscle_test = Muscle(CN)

print(muscle_test.eq_CN(muscle_test.CN))
# Короче, пока см. ниже


# =============================
# Пример со stackoverflow: 
def foo1(self, b):
    return self.a*b

class FooBar1(object):
    def __init__(self, func, a):
        self.a=a
        self.func=func

# Now, if you try the following:
foobar1 = FooBar1(foo1,4)
foobar1.func(3) # = foo1(self, 3)
# You'll get the following error:
# TypeError: foo0() missing 1 required positional argument: 'b' 
# т.е. типа 3 - это self

import weakref

class WeakMethod:
    def __init__(self, func, instance): 
        """ т.е. объект этого класса — это хреновина, которая связывает 
        слабую ссылку на объект исходного класса с функцией, которую использует класс. 
        Ещё раз: объект класса по слабой ссылке и функция для объекта этого класса
        """
        self.func = func
        self.instance_ref = weakref.ref(instance)

        self.__wrapped__ = func  # this makes things like `inspect.signature` work
        # Я ХЗ, что это

    def __call__(self, *args, **kwargs):
        instance = self.instance_ref()
        return self.func(instance, *args, **kwargs)
    """ 
    Т.е. объект этого класса — это автоматический вызов нужной нам функции 
    от объекта исходного класса? 
    """ 

    """ 
    В чём тогда твоя проблема, Карл? 
    В том, что вызвать функцию исходного класса от самого класса ты не можешь, 
    а вызвать эту же функцию от слабой ссылки на класс ты можешь? 
    """

    def __repr__(self):
        cls_name = type(self).__name__
        return '{}({!r}, {!r})'.format(cls_name, self.func, self.instance_ref()) 
    # На это тоже пока забьём


class FooBar(object):
    def __init__(self, func, a):
        self.a = a
        self.func = WeakMethod(func, self) 
        """ 
        То есть в переводе на русский, когда мы в этом (исходном) классе 
        вызываем (дёргаем) функцию как атрибут, 
        мы на самом деле вызываем её с аргументом – слабой ссылкой на сам класс 
        (элементом класса). 
        И эта чёртова магия должна сработать просто из-за волшебных слов «слабая ссылка»? 
        Что за хрень?!
        """ 

f = FooBar(foo1, 7) 
print(f.func(3))  # 21 
""" = WeakMethod(foo1, f)(3) = foo1(weakref.ref(f), 3)) = 
= weakref.ref(f).a * 3 = 7 * 3 = 21 
Ну вот да, основной вопрос — зачем нужна вся эта хренотень со слабыми ссылками?
"""

# =====================================



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


    def model(self, CN, F, t): 
        """
        Collects ODEs in one system
        """
        # Эту функцию пока фиксируем и от неё отталкиваемся

        eq_1 = self.eq_CN(CN, t)
        eq_2 = self.eq_F(F, t)

        return array([eq_1, eq_2])
    
