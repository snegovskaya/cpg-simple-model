from src.neuron import *
from src.muscle import *

def delegate (obj, vars, t):
    if isinstance(obj, Neuron): 
        delegate_Neuron(obj, vars, t)
    elif isinstance(obj, Muscle): 
        delegate_Neuron(obj, vars, t)