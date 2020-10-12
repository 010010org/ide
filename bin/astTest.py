import ast
import json

list = [1, 2, 3]
list2 = [4, 5, 6]
list+=list2
print(list)


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
