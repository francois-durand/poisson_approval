import sympy as sp
from fractions import Fraction
from poisson_approval.utils.Util import isnan, isneginf, isclose


# noinspection NonAsciiCharacters
class Asymptotic:
    r"""An asymptotic development of the form :math:`\exp(\mu n + \nu \log n + \xi + o(1))`.

    Parameters
    ----------
    mu : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Coefficient of the term in `n` (called "magnitude").
    mu : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Coefficient of the term in `log n`.
    mu : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Constant coefficient.

    Attributes
    ----------
    μ : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Alias for :attr:`mu`.
    ν : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Alias for :attr:`nu`.
    ξ : Number, ``sp.nan``, ``np.nan``, ``- sp.oo`` or ``- np.inf``
        Alias for :attr:`xi`.

    Notes
    -----
    If a coefficient is ``sp.nan`` or ``np.nan``, it means that it is not known. In contrast, a coefficient 0 means
    that there is no corresponding term in the asymptotic development.

    If (and only if) the event is impossible, then ``mu = nu = xi = - inf``. It is possible to use either ``- sp.oo``
    or ``- np.inf``.

    Examples
    --------

        >>> asymptotic = Asymptotic(mu=-Fraction(1, 9), nu=-Fraction(1, 2), xi=-Fraction(1, 2) * sp.log(8 * sp.pi / 9))
        >>> print(asymptotic)
        exp(- n/9 - log(n)/2 - log(8*pi/9)/2 + o(1))
        >>> asymptotic.mu
        Fraction(-1, 9)
        >>> asymptotic.nu
        Fraction(-1, 2)
        >>> asymptotic.xi
        -log(8*pi/9)/2
    """

    def __init__(self, mu, nu, xi):
        self.mu = self.μ = mu
        self.nu = self.ν = nu
        self.xi = self.ξ = xi

    def __repr__(self):
        """Repr.

        Returns
        -------
        str

        Examples
        --------
            >>> Asymptotic(mu=- Fraction(1, 10), nu=sp.nan, xi=3)
            Asymptotic(mu=Fraction(-1, 10), nu=nan, xi=3)
            >>> Asymptotic(- (sp.sqrt(3) - sp.sqrt(2)) ** 2,
            ...            - sp.Rational(1, 2),
            ...            - sp.log(4 * sp.sqrt(6) * sp.pi) / 2)
            Asymptotic(mu=-(-sqrt(2) + sqrt(3))**2, nu=-1/2, xi=-log(4*sqrt(6)*pi)/2)
        """
        return 'Asymptotic(mu=%r, nu=%r, xi=%r)' % (self.mu, self.nu, self.xi)

    def __str__(self):
        """Str.

        Returns
        -------
        str

        Examples
        --------
            >>> print(Asymptotic(mu=- Fraction(1, 10), nu=sp.nan, xi=3))
            exp(- n/10 + ? log(n) + 3 + o(1))
            >>> print(Asymptotic(- (sp.sqrt(3) - sp.sqrt(2)) ** 2,
            ...                  - sp.Rational(1, 2),
            ...                  - sp.log(4 * sp.sqrt(6) * sp.pi) / 2))
            exp(- n*(-sqrt(2) + sqrt(3))**2 - log(n)/2 - log(4*sqrt(6)*pi)/2 + o(1))
            >>> print(Asymptotic(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo))
            exp(- inf)
        """
        if isneginf(self.mu) and isneginf(self.nu) and isneginf(self.xi):
            return "exp(- inf)"

        def nice(x, suffix):
            # x : coefficient, suffix : sympy expression
            if isnan(x):
                return ' + ?' if suffix == 1 else ' + ? %s' % suffix
            if x == 0:
                return ''
            a = sp.symbols('a')
            result = str(a + x * suffix)
            assert result[0:2] == 'a '
            return result[1:]

        n = sp.symbols('n')
        s = nice(self.mu, n) + nice(self.nu, sp.log(n)) + nice(self.xi, 1)
        s += ' + o(1)'
        if s[1] == "+":
            s = s[3:]
        else:
            s = s[1:]
        s = "exp(%s)" % s
        return s

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    @property
    def limit(self):
        """Number, ``sp.nan`` or ``sp.oo`` : Limit when `n` tends to infinity.

        Examples
        --------
            >>> Asymptotic(mu=-1, nu=0, xi=0).limit
            0
            >>> Asymptotic(mu=1, nu=0, xi=0).limit
            oo
            >>> Asymptotic(mu=-1, nu=sp.nan, xi=sp.nan).limit
            0
            >>> Asymptotic(mu=0, nu=-1, xi=sp.nan).limit
            0
            >>> Asymptotic(mu=0, nu=0, xi=2).limit
            exp(2)

        ``sp.nan`` means that the limit is unknown:

            >>> Asymptotic(mu=0, nu=0, xi=sp.nan).limit
            nan
        """
        if isnan(self.mu):
            return sp.nan
        elif self.mu > 0:
            return sp.oo
        elif self.mu < 0:
            return 0
        else:  # self.mu == 0
            if isnan(self.nu):
                return sp.nan
            elif self.nu > 0:
                return sp.oo
            elif self.nu < 0:
                return 0
            else:  # self.nu == 0:
                if isnan(self.xi):
                    return sp.nan
                else:
                    return sp.exp(self.xi)

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
            exp(43*n + 53*log(n) + 72 + o(1))
            >>> print(Asymptotic(mu=42, nu=51, xi=69) * Asymptotic(mu=1, nu=sp.nan, xi=sp.nan))
            exp(43*n + ? log(n) + ? + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, sp.log(other))

        def my_addition(x, y):
            return 0 if isclose(x, y) else x + y

        return Asymptotic(my_addition(self.mu, other.mu),
                          my_addition(self.nu, other.nu),
                          my_addition(self.xi, other.xi))

    def __rmul__(self, other):
        """
        Examples
        --------
            >>> print(3 * Asymptotic(mu=42, nu=51, xi=69))
            exp(42*n + 51*log(n) + log(3) + 69 + o(1))
        """
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
            exp(41*n + 49*log(n) + 66 + o(1))
            >>> print(Asymptotic(mu=42, nu=51, xi=69) / Asymptotic(mu=1, nu=sp.nan, xi=sp.nan))
            exp(41*n + ? log(n) + ? + o(1))
            >>> print(1 / Asymptotic(mu=42, nu=51, xi=69))
            exp(- 42*n - 51*log(n) - 69 + o(1))
            >>> print(Asymptotic(mu=42, nu=51, xi=69) / 2)
            exp(42*n + 51*log(n) - log(2) + 69 + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, sp.log(other))
        return self * Asymptotic(- other.mu, - other.nu, - other.xi)

    def __rtruediv__(self, other):
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, sp.log(other))
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
            exp(42*n + 2*log(n) + 69 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=69) + Asymptotic(mu=42, nu=51, xi=3))
            exp(42*n + 51*log(n) + 3 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=4) + Asymptotic(mu=42, nu=2, xi=3))
            exp(42*n + 2*log(n) + log(exp(3) + exp(4)) + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=4) + 1)
            exp(42*n + 2*log(n) + 4 + o(1))
            >>> print(1 + Asymptotic(mu=42, nu=2, xi=4))
            exp(42*n + 2*log(n) + 4 + o(1))
            >>> print(Asymptotic(mu=42, nu=2, xi=69) + Asymptotic(mu=41.99999999, nu=51, xi=3))
            exp(42*n + 51*log(n) + 3 + o(1))
        """
        if not isinstance(other, Asymptotic):
            other = Asymptotic(0, 0, sp.log(other))
        if isnan(self.mu) or isnan(other.mu):
            return Asymptotic(sp.nan, sp.nan, sp.nan)
        elif isclose(self.mu, other.mu):
            mu = max(self.mu, other.mu)
            if isnan(self.nu) or isnan(other.nu):
                return Asymptotic(mu, sp.nan, sp.nan)
            elif isclose(self.nu, other.nu):
                nu = max(self.nu, other.nu)
                xi = sp.log(sp.exp(self.xi) + sp.exp(other.xi))
                return Asymptotic(mu, nu, xi)
            elif self.nu > other.nu:
                return Asymptotic(mu, self.nu, self.xi)
            else:
                return Asymptotic(mu, other.nu, other.xi)
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
            True if this asymptotic development is approximately equal to `other`, in the sense of :func:`isclose`.

        Examples
        --------
            >>> Asymptotic(mu=1, nu=2, xi=3).isclose(
            ...     Asymptotic(mu=0.999999999999, nu=2.00000000001, xi=3))
            True
            >>> Asymptotic(mu=1, nu=2, xi=3).isclose(
            ...     Asymptotic(mu=Fraction(999999999999, 1000000000000), nu=2, xi=3))
            False
        """
        if not isinstance(other, Asymptotic):
            return False
        some_coefficients_are_nan = (isnan(self.mu) or isnan(self.nu) or isnan(self.xi)
                                     or isnan(other.mu) or isnan(other.nu) or isnan(other.xi))
        if some_coefficients_are_nan:
            raise ValueError('Can assert isclose only when all coefficients are known.')
        return (isclose(self.mu, other.mu, *args, **kwargs)
                and isclose(self.nu, other.nu, * args, ** kwargs)
                and isclose(self.xi, other.xi, *args, **kwargs))

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
            exp(- n + log(n) + o(1))
            >>> Asymptotic.poisson_value(tau=2, k=3)
            Asymptotic(mu=-2, nu=3, xi=-log(6) + 3*log(2))
        """
        if tau == 0:
            if k == 0:
                return cls(mu=0, nu=0, xi=0)
            else:
                return cls(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
        return cls(mu=- tau, nu=k, xi=k * sp.log(tau) - sp.log(sp.factorial(k)))

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
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=0))
            exp(- n + o(1))
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=1))
            exp(- inf)
            >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=0, k=1))
            exp(- n + log(n) + o(1))
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=2, tau_2=0, k=3)
            Asymptotic(mu=-2, nu=3, xi=-log(6) + 3*log(2))
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=1, k=0)
            Asymptotic(mu=0, nu=-1/2, xi=-log(4*pi)/2)
            >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=2, k=3)
            Asymptotic(mu=-(1 - sqrt(2))**2, nu=-1/2, xi=-log(32*sqrt(2)*pi)/2)
        """
        if tau_1 == 0:
            if k == 0:
                return cls(mu=- tau_2, nu=0, xi=0)
            else:
                return cls(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
        elif tau_2 == 0:
            return cls(mu=- tau_1, nu=k, xi=k * sp.log(tau_1) - sp.log(sp.factorial(k)))
        else:
            return cls(
                mu=- (sp.sqrt(tau_1) - sp.sqrt(tau_2)) ** 2,
                nu=- sp.Rational(1, 2),
                xi=- sp.Rational(1, 2) * sp.log(4 * sp.pi * sp.sqrt(tau_1 * tau_2) * sp.S(tau_2**k) / tau_1**k)
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
            >>> print(Asymptotic.poisson_eq(tau_1=0, tau_2=0))
            exp(o(1))
            >>> print(Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=0))
            exp(- n/10 + o(1))
            >>> Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            Asymptotic(mu=-2/5, nu=-1/2, xi=-log(6*pi/5)/2)
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
            >>> print(Asymptotic.poisson_one_more(tau_1=0, tau_2=Fraction(1, 10)))
            exp(- inf)
            >>> print(Asymptotic.poisson_one_more(tau_1=Fraction(1, 10), tau_2=0))
            exp(- n/10 + log(n) - log(10) + o(1))
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
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=0))
            exp(- n + o(1))
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=1))
            exp(- inf)
            >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=0, k=0))
            exp(o(1))
            >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=1, k=0)
            Asymptotic(mu=0, nu=0, xi=-log(2))
            >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=2, k=3)
            Asymptotic(mu=-(1 - sqrt(2))**2, nu=-1/2, xi=-log(32*sqrt(2)*pi)/2 - log(1 - sqrt(2)/2))
        """
        if tau_1 == 0:
            if k == 0:
                return cls(mu=- tau_2, nu=0, xi=0)
            else:
                return cls(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
        elif tau_1 > tau_2:
            # Probability 1 => the log tends to 0.
            return cls(mu=0, nu=0, xi=0)
        elif tau_1 == tau_2:
            # Probability 1/2 => the log tends to - log(2).
            return cls(mu=0, nu=0, xi=- sp.log(2))
        else:
            # Use the offset theorem with event X_1 = X_2, then infinite sum.
            return cls(
                mu=- (sp.sqrt(tau_1) - sp.sqrt(tau_2)) ** 2,
                nu=- sp.Rational(1, 2),
                xi=(- sp.Rational(1, 2) * sp.log(4 * sp.pi * sp.sqrt(tau_1 * tau_2) * sp.S(tau_2**k) / tau_1**k)
                    - sp.log(1 - sp.sqrt(sp.S(tau_1) / tau_2)))
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
            >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=0))
            exp(o(1))
            >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=Fraction(1, 10)))
            exp(- n/10 + o(1))
            >>> print(Asymptotic.poisson_ge(tau_1=Fraction(1, 10), tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_ge(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10))
            Asymptotic(mu=0, nu=0, xi=0)
            >>> Asymptotic.poisson_ge(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10))
            Asymptotic(mu=0, nu=0, xi=-log(2))
            >>> asymptotic = Asymptotic.poisson_ge(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic.isclose(Asymptotic(mu=asymptotic_eq.mu,
            ...                               nu=asymptotic_eq.nu,
            ...                               xi=asymptotic_eq.xi + sp.log(sp.Rational(3, 2))))
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
            >>> from poisson_approval import Asymptotic
            >>> import sympy as sp
            >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=0))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=Fraction(1, 10)))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt(tau_1=Fraction(1, 10), tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_gt(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10))
            Asymptotic(mu=0, nu=0, xi=0)
            >>> Asymptotic.poisson_gt(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10))
            Asymptotic(mu=0, nu=0, xi=-log(2))
            >>> asymptotic = Asymptotic.poisson_gt(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic.isclose(Asymptotic(mu=asymptotic_eq.mu,
            ...                               nu=asymptotic_eq.nu,
            ...                               xi=asymptotic_eq.xi - sp.log(2)))
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
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=0))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=Fraction(1, 10)))
            exp(- inf)
            >>> print(Asymptotic.poisson_gt_one_more(tau_1=Fraction(1, 10), tau_2=0))
            exp(o(1))
            >>> Asymptotic.poisson_gt_one_more(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10))
            Asymptotic(mu=0, nu=0, xi=0)
            >>> Asymptotic.poisson_gt_one_more(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10))
            Asymptotic(mu=0, nu=0, xi=-log(2))
            >>> asymptotic = Asymptotic.poisson_gt_one_more(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10))
            >>> asymptotic.isclose(Asymptotic(mu=asymptotic_eq.mu,
            ...                               nu=asymptotic_eq.nu,
            ...                               xi=asymptotic_eq.xi - sp.log(6)))
            True
        """
        return cls.poisson_x1_ge_x2_plus_k(tau_1, tau_2, 2)
