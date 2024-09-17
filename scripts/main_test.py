# from numpy import * 
import sys
sys.path.append("/Users/dascha/Job/cpg-simple-model/src")
import numpy as np1 
from src.net import Net 
from src.element import Element
from src.neuron import Neuron

## Приблуды для отображения переменных из пространства имён и пути 
# (см. занятие по модулям на selfedu) 

# import sys
# import pprint

# pprint.pprint(sys.path)
# pprint.pprint(locals())


net = Net(3)
element1 = Neuron(net = net, name = "neuron1") 
element2 = Neuron(input = element1, name = "element2")
element3 = Element(net = net, input = (element1, element2)) # А мог бы быть и None

print(element3.net.elements_list)