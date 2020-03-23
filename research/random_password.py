#!/usr/bin/python2
#
# generates a random password from an alphabet
#
# From: http://utcc.utoronto.ca/~cks/space/blog/python/LargeIntegersLike
#


from math import log, ceil

def genpass(nchars, alphabet):
    alen = len(alphabet)
    bits = int(ceil(log(alen, 2) * nchars))
    rnum = getnbits(bits)
    pw = ''
    while nchars:
        # extract a character's worth
        # of randomness.
        idx = rnum % alen
        rnum = rnum // alen
        pw += alphabet[idx]
        nchars -= 1
    return pw


def getnbits(nbits):
    fp = open("/dev/urandom", "r")
    bytes = (nbits + 7) // 8
    buf = fp.read(bytes)
    fp.close()
    base = 0L
    for c in list(buf):
        base = (base << 8L) + ord(c)
    return base


if __name__ == '__main__':

    print genpass(24, "abcdefghijklmnopqrstuvwxyz")

