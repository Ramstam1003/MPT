import numpy as np
import pyunit_prime as pp
import random


def Cutting(x: int, dt: np.dtype, s):
    # x input dt:basic datatype s byte len of dt
    conse = []
    z = dt(1 * pow(2, s) - 1)  # 255
    while x != 0:
        t = dt(np.bitwise_and(z, x))
        conse.append(t)
        x = dt(np.right_shift(x, s))
    return conse


def GenerateIPHash(w, range1=51,range2=100):
    # generate pairwise independent hash function,using the prime number
    # ax + b mod p, a,b,p are all prime numbers,p nears w,a in [range1+1,range2], b in [1,range1]
    # return a Hashfunction and it`s area
    a = random.randint(range1+1,range2)
    b = random.randint(1, range1)
    pl = pp.prime_range(w - 20, w + 20)
    p = pl[int(len(pl) / 2)]

    def Hashfunc(x):
        return (a * x + b) % p

    return Hashfunc, p
