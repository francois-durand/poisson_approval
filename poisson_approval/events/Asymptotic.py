from math import sqrt, log, pi, isclose, exp, factorial
import numpy as np
from poisson_approval.utils.Util import isnan, isposinf, isneginf


# noinspection NonAsciiCharacters
class Asymptotic:
    r"""An asymptotic development of the form :math:`\exp(\mu n + \nu \log n + \xi + o(1))`.

    Parameters
    ----------
    mu : Number, ``np.nan`` or ``np.inf``
        Coefficient of the term in `n` (called "magnitude").
    nu : Number, ``np.nan`` or ``np.inf``
        Coefficient of the term in `log n`.
    xi : Number, ``np.nan`` or ``np.inf``
        Constant coefficient.

    Attributes
    ----------
    μ : Number, ``np.nan`` or ``np.inf``
        Alias for :attr:`mu`.
    ν : Number, ``np.nan`` or ``np.inf``
        Alias for :attr:`nu`.
    ξ : Number, ``np.nan`` or ``np.inf``
        Alias for :attr:`xi`.

    Notes
    -----
    If a coefficient is ``np.nan``, it means that it is not known. In contrast, a coefficient 0 means that there is no
    corresponding term in the asymptotic development.

    If (and only if) the event is impossible, then ``mu = nu = xi = - np.inf``.

    Examples
    --------

        >>> asymptotic = Asymptotic(mu=-1 / 9, nu=-1 / 2, xi=-1 / 2 * log(8 * pi / 9))
        >>> print(asymptotic)
        exp(- 0.111111 n - 0.5 log n - 0.513473 + o(1))
        >>> asymptotic.mu
        -0.1111111111111111
        >>> asymptotic.nu
        -0.5
        >>> asymptotic.xi
        -0.5134734250965083
    """

    def __init__(self, mu, nu, xi):
        self.mu = mu
        self.nu = nu
        self.xi = xi
        self.μ = mu
        self.ν = nu
        self.ξ = xi

    def __repr__(self):
        """Repr.

        Returns
        -------
        str

        Examples
        --------
            >>> from fractions import Fraction
            >>> Asymptotic(mu=- Fraction(1, 10), nu=np.nan, xi=3)
            Asymptotic(mu=Fraction(-1, 10), nu=nan, xi=3)
        """
        return 'Asymptotic(mu=%r, nu=%r, xi=%r)' % (self.mu, self.nu, self.xi)

    def __str__(self):
        """Str.

        Returns
        -------
        str

        Examples
        --------
            >>> from fractions import Fraction
            >>> print(Asymptotic(mu=- Fraction(1, 10), nu=np.nan, xi=3))
            exp(- 0.1 n + ? log n + 3 + o(1))
            >>> print(Asymptotic(mu=-np.inf, nu=-np.inf, xi=-np.inf))
            exp(- inf)
        """
        if isneginf(self.mu) and isneginf(self.nu) and isneginf(self.xi):
            return "exp(- inf)"

        def nice(x, suffix):
            x = float(x)
            if isneginf(x):
                return ' - inf ' + suffix if suffix else ' - inf'
            if isposinf(x):
                return ' + inf ' + suffix if suffix else ' + inf'
            if isnan(x):
                return ' + ? ' + suffix if suffix else ' + ?'
            if isclose(x, 1) and suffix:
                return ' + ' + suffix
            if isclose(x, -1) and suffix:
                return ' - ' + suffix
            if isclose(x, 0):
                return ''
            result = ' + ' if x > 0 else ' - '
            result += "{:.6g}".format(float(abs(x)))
            result += ' ' + suffix if suffix else ''
            return result
        s = nice(self.mu, 'n') + nice(self.nu, 'log n') + nice(self.xi, '')
        s += ' + o(1)'
        if s[1] == "+":
            s = s[3:]
        else:
            s = s[1:]
        s = "exp(%s)" % s
        return s

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    @property
    def limit(self):
        """Number, ``np.nan`` or ``np.inf`` : Limit when `n` tends to infinity.

        Examples
        --------
            >>> Asymptotic(mu=-1, nu=0, xi=0).limit
            0
            >>> Asymptotic(mu=1, nu=0, xi=0).limit
            inf
            >>> Asymptotic(mu=-1, nu=np.nan, xi=np.nan).limit
            0
            >>> Asymptotic(mu=0, nu=-1, xi=np.nan).limit
            0

        ``np.nan`` means that the limit is unknown:

            >>> Asymptotic(mu=0, nu=0, xi=np.nan).limit
            nan
        """
        if isnan(float(self.mu)):
            return np.nan
        if isclose(self.mu, 0):
            if isnan(float(self.nu)):
                return np.nan
            if isclose(self.nu, 0):
                if isnan(float(self.xi)):
                    return np.nan
                return exp(self.xi)
            elif self.nu > 0:
                return np.inf
            else:
                return 0
        elif self.mu > 0:
            return np.inf
        else:
            return 0

    def __mul__(self, other):
        """Multiplication of two asymptotic developments.

        Parameters
        ----------
        other: `Asymptotic` or Number.

        Returns
        -------
        product : Asymptotic
            The product of this asymptotic development and `other`.

        Examples
        --------
            >>> print(Asymptotic(mu=42, nu=51, xi=69) * Asymptotic(mu=1, nu=2, xi=3))
            exp(43 n + 53 log n + 72 + o(1))
            >>> print(Asymptotic(mu=42, nu=51, xi=69) * Asymptotic(mu=1, nu=np.nan, xi=np.nan))
            exp(43 n + ? log n + ? + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, log(other))
        return Asymptotic(
            mu=0 if isclose(self.mu, -other.mu) else self.mu + other.mu,
            nu=0 if isclose(self.nu, -other.nu) else self.nu + other.nu,
            xi=0 if isclose(self.xi, -other.xi) else self.xi + other.xi
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """Division of two asymptotic developments.

        Parameters
        ----------
        other: `Asymptotic` or Number.

        Returns
        -------
        ratio : Asymptotic
            The division of this asymptotic development by `other`.

        Examples
        --------
            >>> print(Asymptotic(mu=42, nu=51, xi=69) / Asymptotic(mu=1, nu=2, xi=3))
            exp(41 n + 49 log n + 66 + o(1))
            >>> print(Asymptotic(mu=42, nu=51, xi=69) / Asymptotic(mu=1, nu=np.nan, xi=np.nan))
            exp(41 n + ? log n + ? + o(1))
            >>> print(1 / Asymptotic(mu=42, nu=51, xi=69))
            exp(- 42 n - 51 log n - 69 + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, log(other))
        return self * Asymptotic(- other.mu, - other.nu, - other.xi)

    def __rtruediv__(self, other):
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, log(other))
        return other / self

    # noinspection PyTypeChecker
    def __add__(self, other):
        """Addition of two asymptotic developments.

        Parameters
        ----------
        other: `Asymptotic` or Number.

        Returns
        -------
        sum : Asymptotic
            The sum of this asymptotic development and `other`.

        Examples
        --------
            >>> print(Asymptotic(mu=42, nu=2, xi=69) + Asymptotic(mu=1, nu=51, xi=3))
            exp(42 n + 2 log n + 69 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=69) + Asymptotic(mu=42, nu=51, xi=3))
            exp(42 n + 51 log n + 3 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=4) + Asymptotic(mu=42, nu=2, xi=3))
            exp(42 n + 2 log n + 4.31326 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=4) + 1)
            exp(42 n + 2 log n + 4 + o(1))
            >>> print(1 + Asymptotic(mu=42, nu=2, xi=4))
            exp(42 n + 2 log n + 4 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=69) + Asymptotic(mu=41.99999999, nu=51, xi=3))
            exp(42 n + 51 log n + 3 + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, log(other))
        if isnan(float(self.mu)) or isnan(float(other.mu)):
            return Asymptotic(np.nan, np.nan, np.nan)
        elif isclose(self.mu, other.mu):
            if isnan(float(self.nu)) or isnan(float(other.nu)):
                return Asymptotic(max(self.mu, other.mu), np.nan, np.nan)
            elif isclose(self.nu, other.nu):
                return Asymptotic(max(self.mu, other.mu), max(self.nu, other.nu), log(exp(self.xi) + exp(other.xi)))
            elif self.nu > other.nu:
                return Asymptotic(self.mu, self.nu, self.xi)
            else:
                return Asymptotic(other.mu, other.nu, other.xi)
        elif self.mu > other.mu:
            return Asymptotic(self.mu, self.nu, self.xi)
        else:
            return Asymptotic(other.mu, other.nu, other.xi)

    def __radd__(self, other):
        return self + other

    def isclose(self, other, *args, **kwargs):
        """Test near-equality.

        Parameters
        ----------
        other : Asymptotic
        *args
            Cf. :func:`math.isclose`.
        **kwargs
            Cf. :func:`math.isclose`.

        Returns
        -------
        isclose : bool
            True if this asymptotic development is approximately equal to `other`.

        Examples
        --------
            >>> Asymptotic(mu=1, nu=2, xi=3).isclose(
            ...     Asymptotic(mu=0.999999999999, nu=2.00000000001, xi=3))
            True
        """
        if not isinstance(other, Asymptotic):
            return False
        if isnan(float(self.mu)) or isnan(float(self.nu)) or isnan(float(self.xi))\
                or isnan(float(other.mu)) or isnan(float(other.nu)) or isnan(float(other.xi)):
            raise ValueError('Can assert isclose only when all coefficients are known.')
        return (
            isclose(self.mu, other.mu, *args, **kwargs)
            and isclose(self.nu, other.nu, * args, ** kwargs)
            and isclose(self.xi, other.xi, *args, **kwargs)
        )

    @classmethod
    def poisson_value(cls, tau, k):
        """Asymptotic development of ``P(X = k)``, where ``X ~ Poison(tau * n)``.

        Parameters
        ----------
        tau : Number
            The parameter of the Poisson distribution is ``tau * n``, where `n` tends to infinity.
        k : int
            The desired value in ``P(X = k)``.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X = k)``, where ``X ~ Poison(tau * n)``.

        Examples
        --------
            >>> print(Asymptotic.poisson_value(tau=0, k=0))
            exp(o(1))
            >>> print(Asymptotic.poisson_value(tau=0, k=1))
            exp(- inf)
            >>> print(Asymptotic.poisson_value(tau=1, k=1))
            exp(- n + log n + o(1))
            >>> from math import log
            >>> Asymptotic.poisson_value(tau=2, k=3).isclose(
            ...     Asymptotic(mu=-2, nu=3, xi=3 * log(2) - log(6)))
            True
        """
        if tau == 0:
            if k == 0:
                return cls(mu=0, nu=0, xi=0)
            else:
                return cls(mu=-np.inf, nu=-np.inf, xi=-np.inf)
        return cls(mu=- tau, nu=k, xi=k * log(tau) - log(factorial(k)))

    @classmethod
    def poisson_x1_eq_x2_plus_k(cls, tau_1, tau_2, k):
        """Asymptotic development of ``P(X_1 = X_2 + k)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.
        k : int
            The desired value in ``P(X_1 = X_2 + k)``.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 = X_2 + k)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import log, pi, sqrt
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=0))
            exp(- n + o(1))
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=1))
            exp(- inf)
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=0, k=1))
            exp(- n + log n + o(1))
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=2, tau_2=0, k=3).isclose(
            ...     Asymptotic(mu=-2, nu=3, xi=3 * log(2) - log(6)))
            True
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=1, k=0).isclose(
            ...     Asymptotic(mu=0, nu=- 1 / 2, xi=- 1 / 2 * log(4 * pi)))
            True
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=2, k=3).isclose(
            ...     Asymptotic(mu=- (1 - sqrt(2)) ** 2, nu=- 1 / 2, xi=- 1 / 2 * log(32 * pi * sqrt(2))))
            True
        """
        if tau_1 == 0:
            if k == 0:
                return cls(mu=- tau_2, nu=0, xi=0)
            else:
                return cls(mu=-np.inf, nu=-np.inf, xi=-np.inf)
        elif tau_2 == 0:
            return cls(mu=- tau_1, nu=k, xi=k * log(tau_1) - log(factorial(k)))
        elif tau_1 == tau_2:
            # Theoretically it falls into the general case. But in practice, the general case would give mu = -0.0,
            # which is not nice.
            return cls(
                mu=0,
                nu=- 1 / 2,
                xi=- 1 / 2 * log(4 * pi * tau_1)
            )
        else:
            return cls(
                mu=- (sqrt(tau_1) - sqrt(tau_2)) ** 2,
                nu=- 1 / 2,
                xi=- 1 / 2 * log(4 * pi * sqrt(tau_1 * tau_2) * tau_2**k / tau_1**k)
            )

    @classmethod
    def poisson_eq(cls, tau_1, tau_2):
        """Asymptotic development of ``P(X_1 = X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 = X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import pi, log
            >>> print(Asymptotic.poisson_eq(tau_1=0, tau_2=0))
            exp(o(1))
            >>> print(Asymptotic.poisson_eq(tau_1=1/10, tau_2=0))
            exp(- 0.1 n + o(1))
            >>> Asymptotic.poisson_eq(tau_1=1/10, tau_2=9/10).isclose(
            ...     Asymptotic(mu=-.4, nu=-.5, xi=-.5 * log(1.2 * pi)))
            True
        """
        return cls.poisson_x1_eq_x2_plus_k(tau_1, tau_2, 0)

    @classmethod
    def poisson_one_more(cls, tau_1, tau_2):
        """Asymptotic development of ``P(X_1 = X_2 + 1)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 = X_2 + 1)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import pi, log
            >>> print(Asymptotic.poisson_one_more(tau_1=0, tau_2=1/10))
            exp(- inf)
            >>> print(Asymptotic.poisson_one_more(tau_1=1/10, tau_2=0))
            exp(- 0.1 n + log n - 2.30259 + o(1))

        """
        return cls.poisson_x1_eq_x2_plus_k(tau_1, tau_2, 1)

    @classmethod
    def poisson_x1_ge_x2_plus_k(cls, tau_1, tau_2, k):
        """Asymptotic development of ``P(X_1 >= X_2 + k)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.
        k : int
            The desired value in ``P(X_1 >= X_2 + k)``.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 >= X_2 + k)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import log
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=0))
            exp(- n + o(1))
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=1))
            exp(- inf)
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=0, k=0))
            exp(o(1))
            >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=1, k=0).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=- log(2)))
            True
            >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=2, k=3).isclose(Asymptotic(
            ...     mu=- (1 - sqrt(2)) ** 2, nu=- 1 / 2,
            ...     xi=(- 1 / 2 * log(32 * pi * sqrt(2)) - log(1 - sqrt(1 / 2)))))
            True
        """
        if tau_1 == 0:
            if k == 0:
                return cls(mu=- tau_2, nu=0, xi=0)
            else:
                return cls(mu=-np.inf, nu=-np.inf, xi=-np.inf)
        elif tau_1 > tau_2:
            # Probability 1 => the log tends to 0.
            return cls(mu=0, nu=0, xi=0)
        elif tau_1 == tau_2:
            # Probability 1/2 => the log tends to - log(2).
            return cls(mu=0, nu=0, xi=- log(2))
        else:
            # Use the offset theorem with event X_1 = X_2, then infinite sum.
            return cls(
                mu=- (sqrt(tau_1) - sqrt(tau_2)) ** 2,
                nu=- 1 / 2,
                xi=(- 1 / 2 * log(4 * pi * sqrt(tau_1 * tau_2) * tau_2**k / tau_1**k)
                    - log(1 - sqrt(tau_1 / tau_2)))
            )

    @classmethod
    def poisson_ge(cls, tau_1, tau_2):
        """Asymptotic development of ``P(X_1 >= X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 >= X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import log
            >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=0))
            exp(o(1))
            >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=1/10))
            exp(- 0.1 n + o(1))
            >>> print(Asymptotic.poisson_ge(tau_1=1/10, tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_ge(tau_1=9/10, tau_2=1/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=0))
            True
            >>> Asymptotic.poisson_ge(tau_1=3/10, tau_2=3/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=-log(2)))
            True
            >>> asymptotic = Asymptotic.poisson_ge(tau_1=1/10, tau_2=9/10)
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=1/10, tau_2=9/10)
            >>> asymptotic.isclose(
            ...     Asymptotic(mu=asymptotic_eq.mu, nu=asymptotic_eq.nu, xi=asymptotic_eq.xi + log(3/2)))
            True
        """
        return cls.poisson_x1_ge_x2_plus_k(tau_1, tau_2, 0)

    @classmethod
    def poisson_gt(cls, tau_1, tau_2):
        """Asymptotic development of ``P(X_1 > X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 > X_2)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import log
            >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=0))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=1/10))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt(tau_1=1/10, tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_gt(tau_1=9/10, tau_2=1/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=0))
            True
            >>> Asymptotic.poisson_gt(tau_1=3/10, tau_2=3/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=-log(2)))
            True
            >>> asymptotic = Asymptotic.poisson_gt(tau_1=1/10, tau_2=9/10)
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=1/10, tau_2=9/10)
            >>> asymptotic.isclose(
            ...     Asymptotic(mu=asymptotic_eq.mu, nu=asymptotic_eq.nu, xi=asymptotic_eq.xi - log(2)))
            True
        """
        return cls.poisson_x1_ge_x2_plus_k(tau_1, tau_2, 1)

    @classmethod
    def poisson_gt_one_more(cls, tau_1, tau_2):
        """Asymptotic development of ``P(X_1 > X_2 + 1)``, where ``X_i ~ Poison(tau_i * n)``.

        Parameters
        ----------
        tau_1,tau_2 : Number
            The parameter of the Poisson distribution of ``X_i`` is ``tau_i * n``, where `n` tends to infinity.

        Returns
        -------
        Asymptotic
            The asymptotic development of ``P(X_1 > X_2 + 1)``, where ``X_i ~ Poison(tau_i * n)``.

        Examples
        --------
            >>> from math import log
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=0))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=1/10))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=1/10, tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_gt_one_more(tau_1=9/10, tau_2=1/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=0))
            True
            >>> Asymptotic.poisson_gt_one_more(tau_1=3/10, tau_2=3/10).isclose(
            ...     Asymptotic(mu=0, nu=0, xi=-log(2)))
            True
            >>> asymptotic = Asymptotic.poisson_gt_one_more(tau_1=1/10, tau_2=9/10)
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=1/10, tau_2=9/10)
            >>> asymptotic.isclose(
            ...     Asymptotic(mu=asymptotic_eq.mu, nu=asymptotic_eq.nu, xi=asymptotic_eq.xi - log(6)))
            True
        """
        return cls.poisson_x1_ge_x2_plus_k(tau_1, tau_2, 2)
