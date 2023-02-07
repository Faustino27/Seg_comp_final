import random

die = random.SystemRandom()

def test(n, a):
    exp = n-1
    while exp%2 == 0 and exp != 0:
        exp >>= 1
    
    if pow(a, exp, n) == 1:
        return True
    
    while exp < n - 1:
        if pow (a, exp, n) == n-1:
            return True
        exp <<= 1
    
    return False

def millerRabin (n, k=40):
    if n == 2 or n == 3:
        return True
    if n%2 == 0:
        return False
    for i in range(k):
        a = die.randrange(2, n-1)
        if not test(n, a):
            return False
    return True

def getKey(n_bits=1024):
    while True:
        random_number = die.getrandbits(n_bits)
        if(millerRabin(random_number)):
            return random_number