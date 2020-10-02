import ast
import json

print(dir(ast.cmpop))
for element in ast.cmpop._attributes:
    print(element)


def plusPlus(x):
    i = 1
    while x & i:
        x = x ^ i
        i = i << 1
    return x ^ i


#print(plusPlus(2))


def plus(x, y):
    while x & y:
        x ^= y
        y = (x & y) << 1
    return x ^ y


#print(plus(2, 3))
