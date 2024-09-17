import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model/src")
import numpy as np1 
from src.net import Net 
from src.element import Element
from src.neuron import Neuron 
from src.muscle import Muscle 
from src.Iapp_patterns import I_impulse 
from src.ode_solution import ode_system

## Задание сети 
net = Net(2) 
neuron = Neuron(net = net, input = I_impulse, pars = {"impulseAmpl": 10, "impulseLength": 10, "tStart": 5}) 
muscle = Muscle(input = neuron) 

print(ode_system(net))

print("It works!")