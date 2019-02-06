"""
TODO: review

    * 

"""

import math


# chapter 6.2, incremental development exercise
def hypotenuse(a, b):
    asquared = a**2
    bsquared = math.pow(b, 2)
    csquared = asquared + bsquared
    c_square_root = math.sqrt(csquared)
    return c_square_root

hyp = hypotenuse(3, 4)
print(hyp)


# chapter 6.4, boolean functions
def is_between(x, y, z):
    if(x <= y <= z):
        return True
    else:
        return False

ans = is_between(2, 5, 4)
print(ans)


# recursive palindrome checker
def is_palindrome(word):
    if (len(word) == 0):
        raise ValueError("ochujałeś?")
    if (ret_first(word) == ret_last(word)):
        if (len(ret_middle(word)) > 1):
            return is_palindrome(ret_middle(word))
        else:
            return True
    else:
        return False


def ret_first(word):
    return word[0]


def ret_last(word):
    return word[-1]


def ret_middle(word):
    return word[1:-1]


lista = ["krok", "ara", "onomatopeja", "abba", ""]

# szybki czit szit do trajkeczowania
for each in lista:
    try:
        print(is_palindrome(each))
    except ValueError as err:
        print('wyjebalo ci to {:s}'.format(str(err)))
    else:
        print(':3')
    finally:
        print('przeiterowalem bez bolu')


def is_power(a, b):
    if (a % b == 0):
        if (((a / b) % b) == 0):
            return True
        else:
            return "trochę tak, ale nie"
    else:
        return False


print(is_power(1024, 2))


