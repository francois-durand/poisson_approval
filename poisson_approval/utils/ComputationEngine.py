import math
from abc import ABC, abstractmethod


# noinspection PyPropertyDefinition,PyNestedDecorators
class ComputationEngine(ABC):
    """Computation engine

    Define how some mathematical operations are performed. Cf. :class:`ComputationEngineSymbolic` and
    :class:`ComputationEngineNumeric` for some examples.
    """

    # Constants

    @property
    @classmethod
    @abstractmethod
    def inf(cls):
        """Positive infinity.
        """
        pass

    @property
    @classmethod
    @abstractmethod
    def nan(cls):
        """Not a Number.
        """
        pass

    @property
    @classmethod
    @abstractmethod
    def pi(cls):
        """Pi.
        """
        pass

    # Functions

    @classmethod
    @abstractmethod
    def exp(cls, x):
        """Exponential.
        """
        pass

    @classmethod
    @abstractmethod
    def factorial(cls, x):
        """Factorial.
        """
        pass

    @classmethod
    @abstractmethod
    def log(cls, x):
        """Logarithm.
        """
        pass

    @classmethod
    @abstractmethod
    def multiply_with_absorbing_zero(cls, x, y):
        """Multiplication with absorbing zero.

        Parameters
        ----------
        x, y : Number

        Returns
        -------
        Number
            If `x` or `y` is 0, then 0 (even if the other input is ``nan``). Otherwise, the product
            of `x` and `y`.
        """
        x = cls.simplify(x)
        y = cls.simplify(y)
        return cls.S(0) if x == 0 or y == 0 else x * y

    # noinspection PyPep8Naming
    @classmethod
    @abstractmethod
    def Rational(cls, x, y):
        """Rational number. Should return a fraction, even in an approximate engine.
        """
        pass

    # noinspection PyPep8Naming
    @classmethod
    @abstractmethod
    def S(cls, x):
        """Convert the number if necessary.

        Return a number that has the same value as `x`. Cf. function ``S`` of the package `sympy`.
        """
        pass

    @classmethod
    @abstractmethod
    def simplify(cls, x):
        """Simplify the number if necessary.

        Return a number that has the same value as `x`. Cf. function ``simplify`` of the package `sympy`.
        """
        pass

    @classmethod
    @abstractmethod
    def sqrt(cls, x):
        """Square root.
        """
        pass

    @classmethod
    def look_equal(cls, x, y, *args, **kwargs):
        """Test if two numbers can reasonably be considered as equal.

        Parameters
        ----------
        x : Number
        y : Number
        *args
            Cf. :func:`math.isclose`.
        **kwargs
            Cf. :func:`math.isclose`.

        Returns
        -------
        bool
            If `x` or `y` is a float or numpy float (but not a sympy float), then return
            ``math.isclose(x, y, *args, **kwargs)``. In all other cases, return True iff `x` is equal to `y`.
        """
        if isinstance(x, float) or isinstance(y, float):
            return math.isclose(x, y, *args, **kwargs)
        else:
            return cls.simplify(x - y) == 0
