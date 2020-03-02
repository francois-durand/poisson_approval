import math
import numpy as np
from poisson_approval.utils.ComputationEngine import ComputationEngine


class ComputationEngineApproximate(ComputationEngine):
    """Computation engine: approximate computation.

    This engine performs approximate computation, using floats when necessary:

        >>> ce = ComputationEngineApproximate
        >>> ce.inf
        inf
        >>> ce.nan
        nan
        >>> ce.exp(3)
        20.085536923187668
        >>> ce.log(3)
        1.0986122886681098
        >>> ce.Rational(1, 3)
        0.3333333333333333
        >>> ce.S(1) / 3
        0.3333333333333333
        >>> ce.simplify(- ce.Rational(1, 10) - (- ce.sqrt(15) / 5 + ce.sqrt(30) / 10)**2)
        -0.151471862576143
        >>> ce.sqrt(3)
        1.7320508075688772
    """

    # Constants

    inf = np.inf
    nan = np.nan

    # Functions

    @classmethod
    def exp(cls, x):
        return math.exp(x)

    @classmethod
    def log(cls, x):
        return math.log(x)

    @classmethod
    def Rational(cls, x, y):
        return x / y

    @classmethod
    def S(cls, x):
        return x

    @classmethod
    def simplify(cls, x):
        return x

    @classmethod
    def sqrt(cls, x):
        return math.sqrt(x)
