from key import getKey
import random
from hashlib import sha3_256
from egcd import egcd
from math import gcd

dice = random.SystemRandom()


class RSA:
    def __init__(self):
        self.p, self.q = self.getKeys()
        self.n = self.p*self.q
        self.phi = (self.p-1)*(self.q-1)
        self.e = 2

        while True:
            self.e = dice.getrandbits(1024)
            if gcd(self.e, self.phi) == 1:
                break
        self.d = egcd(self.e, self.phi)[1] #aplica o algoritmo euclideano extendido

        if(self.d < 0):
            self.d += self.phi

        self.private = [self.n, self.d]
        self.public = [self.n, self.e]

    def getKeys(self):
        p = getKey()
        q = getKey()
        while p == q:
            q = getKey()
        return p,q

    def encryptPublic(self, m: int):
        c = pow(m, self.e, self.n)
        return c
    
    def decryptPublic(self, c: int):
        m = pow(c, self.e, self.n)
        return m

    def encryptPrivate(self, m: int):
        c = pow(m, self.d, self.n)
        return c

    def decryptPrivate(self, c: int):
        m = pow(c, self.d, self.n)
        return m

    def prinKeys(self, msg):
        print("p: ", self.p)
        print("q: ", self.q)
        print("n: ", self.n)
        print("phi: ", self.phi)
        print("e: ", self.e)
        print("d: ", self.d)

