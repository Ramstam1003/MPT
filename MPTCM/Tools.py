import numpy as np
import pyunit_prime as pp
import random


def Cutting(x: int, dt, s):
    # x is the input ; dt:basic datatype ;s byte len of dt
    # this function can cut x in a series number in the format of dt,and put them in a list to return
    result = []
    z = dt(1 * pow(2, s) - 1)  # 255 when dt==uint8
    while x != 0:
        t = dt(np.bitwise_and(z, x))
        result.append(t)
        x = dt(np.right_shift(x, s))
    return result


def GenerateIPHash(w, range1=51, range2=100):
    # generate pairwise independent hash function,using the prime number
    # ax + b mod p, a,b,p are all prime numbers,p nears w,a in [range1+1,range2], b in [1,range1]
    # return a hash-function and it`s consequence range
    a = random.randint(range1 + 1, range2)
    b = random.randint(1, range1)
    pl = pp.prime_range(w - 20, w + 20)
    p = pl[int(len(pl) / 2)]

    def hash_func(x):
        return (a * x + b) % p

    return hash_func, p
