import sympy as sp
from poisson_approval.utils.ComputationEngine import ComputationEngine


class ComputationEngineExact(ComputationEngine):
    """Computation engine: exact computation.

    This engine relies on the external package `sympy` in order to perform exact computation:

        >>> ce = ComputationEngineExact
        >>> ce.inf
        oo
        >>> ce.nan
        nan
        >>> ce.exp(3)
        exp(3)
        >>> ce.log(3)
        log(3)
        >>> ce.Rational(1, 3)
        1/3
        >>> ce.S(1) / 3
        1/3
        >>> ce.simplify(- ce.Rational(1, 10) - (- ce.sqrt(15) / 5 + ce.sqrt(30) / 10)**2)
        -1 + 3*sqrt(2)/5
        >>> ce.sqrt(3)
        sqrt(3)
    """

    # Constants

    inf = sp.oo
    nan = sp.nan

    # Functions

    @classmethod
    def exp(cls, x):
        return sp.exp(x)

    @classmethod
    def log(cls, x):
        return sp.log(x)

    @classmethod
    def Rational(cls, x, y):
        return sp.Rational(x, y)

    @classmethod
    def S(cls, x):
        return sp.S(x)

    @classmethod
    def simplify(cls, x):
        return sp.simplify(x)

    @classmethod
    def sqrt(cls, x):
        return sp.sqrt(x)
