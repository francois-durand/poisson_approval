from time import time
import math
import sympy as sp

N_TRIALS_FLOAT = int(1E6)
t = time()
for _ in range(N_TRIALS_FLOAT):
    a = - 1 / 10 - (- math.sqrt(15) / 5 + math.sqrt(30) / 10)**2
duration_f = (time() - t) / N_TRIALS_FLOAT

N_TRIALS_SYMPY = int(1E3)
t = time()
for _ in range(N_TRIALS_SYMPY):
    a = sp.simplify(- sp.Rational(1, 10) - (- sp.sqrt(15) / 5 + sp.sqrt(30) / 10)**2)
duration_s = (time() - t) / N_TRIALS_SYMPY

print('Computation in floating points:', duration_f)
print('Simplify:', duration_s)
print('Slowdown factor:', duration_s / duration_f)
