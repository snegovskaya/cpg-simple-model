from src.muscle import *
from src.neuron import *

from numpy import *
from matplotlib import pyplot as p
from scipy import integrate

t = linspace(0, 100, 100)
CN0 = 1
F0 = 0

u = 1

test_muscle = Muscle(CN0, F0, u)
# Таким образом имеем, что test_muscle.CN = CN0, test_muscle.F = F0 
test_result = integrate.odeint(test_muscle.model, test_muscle.CN, test_muscle.F, t)
# Дальше просто причесать результат и в продакшн