import math

def average(*kwargs):
    return sum(kwargs) / len(kwargs)

def power(base, exponent):
    return base ** exponent

def sqrt(number):

    if number < 0:
        raise ValueError("Can not take square root of negative number")

    return number ** 0.5

def log(number, base=10):

    if number <= 0 or base <= 0:
        raise ValueError("Can not take log of non-positive number or base")


    return math.log(number, base)