from bitstring import BitArray
import random

key = random.getrandbits(256)
print(type(key))
print(bin(key))

kb = BitArray(bit=bin(key))
print(kb)