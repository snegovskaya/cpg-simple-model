# from numpy import * 
import numpy as np1
from src.element import Element
from src.net import Net

## Для чего нужны были штуки ниже, я не помню
# import sys
# import pprint

# pprint.pprint(sys.path)
# pprint.pprint(locals())


net1 = Net(3)
net2 = Net(0)
element1 = Element() 
element2 = Element(net = net2, input = element1, name = "element2")
element3 = Element(net = net1, input = (element1, element2)) # А мог бы быть и None

test_array = np1.zeros((2,2)) # FIXME Удалить потом

print(element3.net)