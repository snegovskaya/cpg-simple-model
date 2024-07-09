from numpy import * 
from src.element import * 

matrix1 = Matrix(2)
matrix2 = Matrix(3)
test_element1 = Element(matrix = matrix1, input = 0) 
test_element2 = Element(matrix = matrix2, input = 1)
test_element3 = Element(matrix = matrix1, input = 2) # А мог бы быть и None

print(test_element3.matrix.explicit)