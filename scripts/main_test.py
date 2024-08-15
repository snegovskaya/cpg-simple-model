# from numpy import * 
import numpy as np1
from src.element import Element
from src.net import Net
import sys
import pprint

pprint.pprint(sys.path)
pprint.pprint(locals())

matrix1 = Net(3)
matrix2 = Net(0)
test_element1 = Element(input = 0) 
test_element2 = Element(matrix = matrix2, input = 1)
test_element3 = Element(matrix = matrix1, input = 2) # А мог бы быть и None

test_array = np1.zeros((2,2)) # FIXME Удалить потом

print(test_element3.__net)