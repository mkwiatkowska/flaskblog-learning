"""
TODO: review

    * uncomment all function calls

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
# print(hyp)


# chapter 6.4, boolean functions
def is_between(x, y, z):
    if(x <= y <= z):
        return True
    else:
        return False

ans = is_between(2, 5, 4)
# print(ans)


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
# for each in lista:
#     try:
#         print(is_palindrome(each))
#     except ValueError as err:
#         print('wyjebalo ci to {:s}'.format(str(err)))
#     else:
#         print(':3')
#     finally:
#         print('przeiterowalem bez bolu')


def is_power(a, b):
    if (a % b == 0):
        if (((a / b) % b) == 0):
            return True
        else:
            return "trochę tak, ale nie"
    else:
        return False


# print(is_power(1024, 2))


# func print_n from 5.8 but done using iteration instead of recursion
def print_n(s, n):
    while (n > 0):
        print(s)
        n -= 1


# print_n("test", 4)


def func_type():
    while True:
        line = input('> ')
        if (line == 'done'):
            break
        print(line)


# func_type()

# ex 7.3
def approximation_one_by_pie():
    final_series = series()
    one_by_pie = (2 * math.sqrt(2))/(9801) * (final_series)
    print(one_by_pie)


def series():
    series = 0.0
    k = 0
    while (True):
        serie_step = ((math.factorial(4 * k)) * (1103 + 26390 * k)) / \
                (math.pow(math.factorial(k), 4) * math.pow(396, 4*k))
        if (serie_step < math.pow(10, -15)):
            return series
        series += serie_step
        k += 1


approximation_one_by_pie()
print(1 / math.pi)


# printing string backwards
def print_back(word):
    index = len(word) - 1
    while (index >= 0):
        print(word[index])
        index -= 1


print_back('katarzis')


# ex 10.1
def nested_sum(t):
    sum = 0
    for i in t:
        for j in i:
            sum += j
    return sum


listka = [[1, 1], [2], [2, 5]]
print(nested_sum(listka))


# ex. 10.2
def cumsum(t):
    wynikowa = []
    accu = 0
    for i in t:
        accu += i 
        wynikowa.append(accu)
    return wynikowa


testowa = [1, 3, 6, 6, 7]
print(cumsum(testowa))


# ex. 10.3
def middle(t):
    if (len(t) > 2):
        return middle(t[1:-1])
    return t


tet1 = [1, 2, 3]
tet2 = [1, 2, 3, 5]

print(middle(tet1))
print(middle(tet2))


# ex 10.5
def is_sorted(t):
    cur_max_val = t[0]
    for i in range(1, len(t)):
        if not(cur_max_val < t[i]):
            return False
        else:
            cur_max_val = t[i]
    return True        


tet3 = [4, 3, 8]


print(is_sorted(tet3))
print(is_sorted(tet1))


s = 'abc'
t = [0, 1, 2]

z = zip(s, t)
for charr, digit in z:
    print(charr, digit)


def most_frequency(s):
    d = dict()
    for letter in s:
        if letter not in d:
            d[letter] = 1
        else:
            d[letter] += 1
    return d


def histogram(txt):
    d = most_frequency(txt)
    for keys, values in reversed(sorted(d.items(), key=lambda kv: kv[1])):
        print(values, keys)

txt = 'To nie ma tak, że jest dobrze, albo że nie dobrze.'

histogram(txt)


# finally CLASSES
class Point2D:
    """Represents a point in 2D space."""
    x = 0.0
    y = 0.0


blank = Point2D()
print(blank)
blank.x = 1.0
blank.y = 4.0
print(blank.x)


def dist_b_p(p1, p2):
    return math.sqrt(math.pow((p2.x - p1.x), 2) + math.pow((p2.y - p1.y), 2))


po2 = Point2D()


print(dist_b_p(blank, po2))


class Rect:
    w = 0.0
    h = 0.0
    corner = Point2D()


box = Rect()
box.w = 100.0
box.h = 200.0
box.corner.x = 1.0
box.corner.y = 5.0


class Time:
    h = 0
    m = 0 
    s = 0


def print_time(t):
    print('{:n}:{:n}:{:n}'.format(t.h, t.m, t.s))

tajm = Time()
tajm.h = 21
tajm.m = 37
tajm.s = 0

print_time(tajm)


word = 'kakadu'
print(len(set(word)), len(word)) 



def uses_only(word, available):
    return set(word) <= set(available)

print(uses_only('zuza','abc'))