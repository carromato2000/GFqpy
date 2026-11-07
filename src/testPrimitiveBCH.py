from src.primitiveBCH import PrimitiveBCH
from src.alfabet import Alfabet

# alfabeto el hexadecimal
alfabet = Alfabet("0123456789ABCDEF")

bch = PrimitiveBCH(alfabet, 2, 11)
dataword = alfabet.gen_random_text(bch.k)
print(f"Dataword: {dataword}\n")
codeword = bch.systematic_codification(dataword)
print(f"Codeword: {codeword}\n")
print(f"Chech symbols: {codeword[bch.k:]}")