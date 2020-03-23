#!/usr/bin/env python3
'''Demonstrate converting random bytes into a float in [0.0, 1.0).

    Code adapted from Python 3.7.3's random.py module:

        https://github.com/python/cpython/blob/v3.7.3/Lib/random.py#L679
'''

import math
import time

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF
#SOURCE = "/dev/hwrng"
SOURCE = "/dev/urandom"


def _test_generator(n, func, args):
    #print(func.__name__)
    print(n, 'times', func.__name__, end=', ')
    total = 0.0
    sqsum = 0.0
    smallest = 1e10
    largest = -1e10
    t0 = time.perf_counter()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x*x
        smallest = min(x, smallest)
        largest = max(x, largest)
    t1 = time.perf_counter()
    print(round(t1-t0, 3), 'sec,', end=' ')
    avg = total/n
    stddev = math.sqrt(sqsum/n - avg*avg)
    print('avg %g, stddev %g, min %g, max %g' % \
              (avg, stddev, smallest, largest))


def random():
    """Get the next random number in the range [0.0, 1.0)."""
    buf = open(SOURCE, "rb").read(7)
    return (int.from_bytes(buf, 'big') >> 3) * RECIP_BPF


if __name__ == '__main__':

    print("Here's something random:", random())

    _test_generator(2000, random, ())
