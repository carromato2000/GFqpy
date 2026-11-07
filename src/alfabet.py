from sage.all import *
from random import randint

class Alfabet():

    def __init__(self, alfabet_str):
        self.len = len(alfabet_str)
        self.alfabet_str = alfabet_str
        self.sym_to_index = dict()
        i = 0
        for sym in alfabet_str:
            self.sym_to_index[sym] = i
            i+=1

    def gen_random_text(self, n):
        text = []
        for _ in range(n):
            text.append(self.alfabet_str[randint(0,self.len-1)])
        return ''.join(text)
        
