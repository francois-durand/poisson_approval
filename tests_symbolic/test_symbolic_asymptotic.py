import numpy as np
import sympy as sp
from fractions import Fraction
from poisson_approval import Asymptotic


def test_main():
    """
        >>> asymptotic = Asymptotic(mu=-Fraction(1, 9), nu=-Fraction(1, 2), xi=-Fraction(1, 2) * sp.log(8 * sp.pi / 9),
        ...                         symbolic=True)
        >>> print(asymptotic)
        exp(- n/9 - log(n)/2 - log(8*pi/9)/2 + o(1))
        >>> asymptotic.mu
        Fraction(-1, 9)
        >>> asymptotic.nu
        Fraction(-1, 2)
        >>> asymptotic.xi
        -log(8*pi/9)/2
    """
    pass


def test_repr():
    """
        >>> Asymptotic(mu=- Fraction(1, 10), nu=sp.nan, xi=3, symbolic=True)
        Asymptotic(mu=Fraction(-1, 10), nu=nan, xi=3)
        >>> Asymptotic(- (sp.sqrt(3) - sp.sqrt(2)) ** 2,
        ...            - sp.Rational(1, 2),
        ...            - sp.log(4 * sp.sqrt(6) * sp.pi) / 2, symbolic=True)
        Asymptotic(mu=-(-sqrt(2) + sqrt(3))**2, nu=-1/2, xi=-log(4*sqrt(6)*pi)/2)
    """
    pass


def test_str():
    """
        >>> print(Asymptotic(mu=- Fraction(1, 10), nu=sp.nan, xi=3, symbolic=True))
        exp(- n/10 + ? log(n) + 3 + o(1))
        >>> print(Asymptotic(- (sp.sqrt(3) - sp.sqrt(2)) ** 2,
        ...                  - sp.Rational(1, 2),
        ...                  - sp.log(4 * sp.sqrt(6) * sp.pi) / 2, symbolic=True))
        exp(- n*(-sqrt(2) + sqrt(3))**2 - log(n)/2 - log(4*sqrt(6)*pi)/2 + o(1))
        >>> print(Asymptotic(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo, symbolic=True))
        exp(- inf)
    """
    pass


def test_limit():
    """
        >>> Asymptotic(mu=-1, nu=0, xi=0, symbolic=True).limit
        0
        >>> Asymptotic(mu=1, nu=0, xi=0, symbolic=True).limit
        oo
        >>> Asymptotic(mu=-1, nu=sp.nan, xi=sp.nan, symbolic=True).limit
        0
        >>> Asymptotic(mu=0, nu=-1, xi=sp.nan, symbolic=True).limit
        0
        >>> Asymptotic(mu=0, nu=0, xi=2, symbolic=True).limit
        exp(2)
        >>> Asymptotic(mu=0, nu=0, xi=sp.nan, symbolic=True).limit
        nan
    """
    pass


def test_mul():
    """
        >>> print(Asymptotic(mu=42, nu=51, xi=69, symbolic=True) * Asymptotic(mu=1, nu=2, xi=3))
        exp(43*n + 53*log(n) + 72 + o(1))
        >>> print(Asymptotic(mu=42, nu=51, xi=69, symbolic=True) * Asymptotic(mu=1, nu=np.nan, xi=sp.nan))
        exp(43*n + ? log(n) + ? + o(1))
    """
    pass


def test_rmul():
    """
        >>> print(3 * Asymptotic(mu=42, nu=51, xi=69, symbolic=True))
        exp(42*n + 51*log(n) + log(3) + 69 + o(1))
    """
    pass


def test_truediv():
    """
        >>> print(Asymptotic(mu=42, nu=51, xi=69, symbolic=True) / Asymptotic(mu=1, nu=2, xi=3, symbolic=True))
        exp(41*n + 49*log(n) + 66 + o(1))
        >>> print(Asymptotic(mu=42, nu=51, xi=69, symbolic=True) / Asymptotic(mu=1, nu=sp.nan, xi=sp.nan, symbolic=True))
        exp(41*n + ? log(n) + ? + o(1))
        >>> print(1 / Asymptotic(mu=42, nu=51, xi=69, symbolic=True))
        exp(- 42*n - 51*log(n) - 69 + o(1))
        >>> print(Asymptotic(mu=42, nu=51, xi=69, symbolic=True) / 2)
        exp(42*n + 51*log(n) - log(2) + 69 + o(1))
    """
    pass


def test_add():
    """
        >>> print(Asymptotic(mu=42, nu=2, xi=69, symbolic=True) + Asymptotic(mu=1, nu=51, xi=3, symbolic=True))
        exp(42*n + 2*log(n) + 69 + o(1))
        >>> print(Asymptotic(mu=42, nu=2, xi=69, symbolic=True) + Asymptotic(mu=42, nu=51, xi=3, symbolic=True))
        exp(42*n + 51*log(n) + 3 + o(1))
        >>> print(Asymptotic(mu=42, nu=2, xi=4, symbolic=True) + Asymptotic(mu=42, nu=2, xi=3, symbolic=True))
        exp(42*n + 2*log(n) + log(1 + E) + 3 + o(1))
        >>> print(Asymptotic(mu=42, nu=2, xi=4, symbolic=True) + 1)
        exp(42*n + 2*log(n) + 4 + o(1))
        >>> print(1 + Asymptotic(mu=42, nu=2, xi=4, symbolic=True))
        exp(42*n + 2*log(n) + 4 + o(1))
        >>> print(Asymptotic(mu=42, nu=2, xi=69, symbolic=True) + Asymptotic(mu=41.99999999, nu=51, xi=3, symbolic=True))
        exp(42*n + 51*log(n) + 3 + o(1))
    """
    pass


def test_look_equal():
    """
        >>> Asymptotic(mu=1, nu=2, xi=3, symbolic=True).look_equal(
        ...     Asymptotic(mu=0.999999999999, nu=2.00000000001, xi=3, symbolic=True))
        True
        >>> Asymptotic(mu=1, nu=2, xi=3, symbolic=True).look_equal(
        ...     Asymptotic(mu=Fraction(999999999999, 1000000000000), nu=2, xi=3, symbolic=True))
        False
    """
    pass


def test_poisson_value():
    """
        >>> print(Asymptotic.poisson_value(tau=0, k=0, symbolic=True))
        exp(o(1))
        >>> print(Asymptotic.poisson_value(tau=0, k=1, symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_value(tau=1, k=1, symbolic=True))
        exp(- n + log(n) + o(1))
        >>> Asymptotic.poisson_value(tau=2, k=3, symbolic=True)
        Asymptotic(mu=-2, nu=3, xi=log(4/3))
    """
    pass


def test_poisson_x1_eq_x2_plus_k():
    """
        >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=0, symbolic=True))
        exp(- n + o(1))
        >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=0, tau_2=1, k=1, symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=0, k=1, symbolic=True))
        exp(- n + log(n) + o(1))
        >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=2, tau_2=0, k=3, symbolic=True)
        Asymptotic(mu=-2, nu=3, xi=log(4/3))
        >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=1, k=0, symbolic=True)
        Asymptotic(mu=0, nu=-1/2, xi=-log(4*pi)/2)
        >>> Asymptotic.poisson_x1_eq_x2_plus_k(tau_1=1, tau_2=2, k=3, symbolic=True)
        Asymptotic(mu=-3 + 2*sqrt(2), nu=-1/2, xi=-11*log(2)/4 - log(pi)/2)
    """
    pass


def test_poisson_eq():
    """
        >>> print(Asymptotic.poisson_eq(tau_1=0, tau_2=0, symbolic=True))
        exp(o(1))
        >>> print(Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=0, symbolic=True))
        exp(- n/10 + o(1))
        >>> Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        Asymptotic(mu=-2/5, nu=-1/2, xi=-log(6*pi/5)/2)
    """
    pass


def test_poisson_one_more():
    """
        >>> print(Asymptotic.poisson_one_more(tau_1=0, tau_2=Fraction(1, 10), symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_one_more(tau_1=Fraction(1, 10), tau_2=0, symbolic=True))
        exp(- n/10 + log(n) - log(10) + o(1))
    """
    pass


def test_poisson_x1_ge_x2_plus_k():
    """
        >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=0, symbolic=True))
        exp(- n + o(1))
        >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=0, tau_2=1, k=1, symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=0, k=0, symbolic=True))
        exp(o(1))
        >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=1, k=0, symbolic=True)
        Asymptotic(mu=0, nu=0, xi=-log(2))
        >>> Asymptotic.poisson_x1_ge_x2_plus_k(tau_1=1, tau_2=2, k=3, symbolic=True)
        Asymptotic(mu=-3 + 2*sqrt(2), nu=-1/2, xi=-11*log(2)/4 - log(pi)/2 - log(1 - sqrt(2)/2))
    """
    pass


def test_poisson_ge():
    """
        >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=0, symbolic=True))
        exp(o(1))
        >>> print(Asymptotic.poisson_ge(tau_1=0, tau_2=Fraction(1, 10), symbolic=True))
        exp(- n/10 + o(1))
        >>> print(Asymptotic.poisson_ge(tau_1=Fraction(1, 10), tau_2=0, symbolic=True))
        exp(o(1))
        >>> Asymptotic.poisson_ge(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=0)
        >>> Asymptotic.poisson_ge(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=-log(2))
        >>> asymptotic = Asymptotic.poisson_ge(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic.look_equal(Asymptotic(mu=asymptotic_eq.mu,
        ...                                  nu=asymptotic_eq.nu,
        ...                                  xi=asymptotic_eq.xi + sp.log(sp.Rational(3, 2)), symbolic=True))
        True
    """
    pass


def test_poisson_gt():
    """
        >>> from poisson_approval import Asymptotic
        >>> import sympy as sp
        >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=0, symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_gt(tau_1=0, tau_2=Fraction(1, 10), symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_gt(tau_1=Fraction(1, 10), tau_2=0, symbolic=True))
        exp(o(1))
        >>> Asymptotic.poisson_gt(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=0)
        >>> Asymptotic.poisson_gt(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=-log(2))
        >>> asymptotic = Asymptotic.poisson_gt(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic.look_equal(Asymptotic(mu=asymptotic_eq.mu,
        ...                                  nu=asymptotic_eq.nu,
        ...                                  xi=asymptotic_eq.xi - sp.log(2), symbolic=True))
        True
    """
    pass


def test_poisson_gt_one_more():
    """
        >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=0, symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_gt_one_more(tau_1=0, tau_2=Fraction(1, 10), symbolic=True))
        exp(- inf)
        >>> print(Asymptotic.poisson_gt_one_more(tau_1=Fraction(1, 10), tau_2=0, symbolic=True))
        exp(o(1))
        >>> Asymptotic.poisson_gt_one_more(tau_1=Fraction(9, 10), tau_2=Fraction(1, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=0)
        >>> Asymptotic.poisson_gt_one_more(tau_1=Fraction(3, 10), tau_2=Fraction(3, 10), symbolic=True)
        Asymptotic(mu=0, nu=0, xi=-log(2))
        >>> asymptotic = Asymptotic.poisson_gt_one_more(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic_eq = Asymptotic.poisson_eq(tau_1=Fraction(1, 10), tau_2=Fraction(9, 10), symbolic=True)
        >>> asymptotic.look_equal(Asymptotic(mu=asymptotic_eq.mu,
        ...                                  nu=asymptotic_eq.nu,
        ...                                  xi=asymptotic_eq.xi - sp.log(6), symbolic=True))
        True
    """
    pass
