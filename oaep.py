import random
import hashlib 

dice = random.SystemRandom()

class OAEP():
    k0 = 256
    size = 0
    k1 = 0
    #msgLeN + k0 + k1 = 1024

    def __init__(self, size):
        self.size = size


    def padding(self, m):
        mPaddedBits = m
        mPaddedBits <<= self.k1 #adiciona bit 0
        
        return mPaddedBits

    def unpadding(self, mPadded):
        mBits = mPadded
        mBits >>= self.k1 #remove os ultimos bits
        
        return mBits

    def oaep(self, m):
        sizeX = 0
        sizeY = 0
        self.newk1(m)
        mPaddedBits = self.padding(m)
        r = dice.getrandbits(self.k0) # gera o nonce com k0 bits
        G = hashlib.sha3_512(str.encode(str(r))).hexdigest() + hashlib.sha3_256(str.encode(str(r))).hexdigest() # gera o G
        X = mPaddedBits ^ int(G, 16)
        H = hashlib.sha3_256(str.encode(str(X))) # gera o H
        Y = int(H.hexdigest(), 16) ^ r
        sizeX = X.bit_length()
        sizeY = Y.bit_length()

        return str(X)+str(Y), len(str(X))
    
    def reverseOaep(self, mPadded, sizeX):
        mPadded = str(mPadded)
        X = mPadded[:sizeX]
        Y = mPadded[sizeX:]
        H = hashlib.sha3_256(str.encode(X)).hexdigest()
        r = int(Y) ^ int(H,16)
        G = hashlib.sha3_512(str.encode(str(r))).hexdigest() + hashlib.sha3_256(str.encode(str(r))).hexdigest()
        mPadded = int(X) ^ int(G, 16)
        mBits = self.unpadding(mPadded)
        return mBits
    
    def newk1(self, msg):
        self.k1 = self.size - self.k0 - len(str(msg))


# enzo = OAEP(1024)

# msg = 37
# s, sx=enzo.oaep(msg)
# print("s:", s)
# print("len: ", int(s).bit_length())
# rs = enzo.reverseOaep(s, sx)
# print(rs)
# #print(len(rs))
    
            