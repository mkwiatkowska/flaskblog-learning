import math


# chapter 6.2, incremental development exercise
def hypotenuse(a, b):
    asquared = a**2
    bsquared = math.pow(b, 2)
    csquared = asquared + bsquared
    c_square_root = math.sqrt(csquared)
    return c_square_root

print(hypotenuse(3, 4))
