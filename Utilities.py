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

<<<<<<< HEAD
=======

def vectElementDiv(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
            result = []
            for dimension in zip(vect1, vect2):
                if (dimension[1] == 0):
                    print("division by 0")
                    return None
                result.append(dimension[0]/dimension[1])
            return result
    else:
        print("cannot divide elementwise different size vectors")
        return None

>>>>>>> master
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

<<<<<<< HEAD
=======

def scalarDiv(vect, scalar, integer=False):
    if scalar != 0:
        result = []
        for dimension in vect:
            if (integer == True):
                result.append(dimension // scalar)
            else:
                result.append(dimension / scalar)
        return result
    else:
        print("division by 0 is undefined")
        return None
      
>>>>>>> master
class vector():
    def __init__(initData):
        pass

#end utilities  

