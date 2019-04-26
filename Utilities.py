import sys
import sdl2
import sdl2.ext

#utilities
signOf = lambda a: (a > 0) - (a < 0)

vectSameLength = lambda a, b: len(a) == len(b)

def vectAdd(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
        result = []
        for dimension in zip(vect1, vect2):
            result.append(dimension[0] + dimension[1])

        return result
    print("cannot add different size vectors")
    return None

def vectSub(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
        result = []
        for dimension in zip(vect1, vect2):
            result.append(dimension[0] - dimension[1])

        return result
    print("cannot subtract different size vectors")
    return None

def vectElementMult(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
            result = []
            for dimension in zip(vect1, vect2):
                result.append(dimension[0] * dimension[1])
            return result
    else:
        print("cannot multiply elementwise different size vectors")
        return None

def vectAbs(vect):
    result = []
    for dimension in vect:
        result.append(abs(dimension))
    return result

def scalarAdd(vect, scalar):
    result = []
    for dimension in vect:
        result.append(dimension + scalar)
    return result

def scalarProduct(vect, scalar):
    result = []
    for dimension in vect:
        result.append(dimension * scalar)
    return result

class vector():
    def __init__(initData):
        pass

#end utilities  

