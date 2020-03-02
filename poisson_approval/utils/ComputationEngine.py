from abc import ABC, abstractmethod


# noinspection PyPropertyDefinition,PyNestedDecorators
class ComputationEngine(ABC):
    """Computation engine

    Define how some mathematical operations are performed. Cf. :class:`ComputationEngineExact` and
    :class:`ComputationEngineApproximate` for some examples.
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

    # Functions

    @classmethod
    @abstractmethod
    def exp(cls, x):
        """Exponential.
        """
        pass

    @classmethod
    @abstractmethod
    def log(cls, x):
        """Logarithm.
        """
        pass

    # noinspection PyPep8Naming
    @classmethod
    @abstractmethod
    def Rational(cls, x, y):
        """Rational number.
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
