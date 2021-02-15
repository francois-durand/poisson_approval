from poisson_approval import TauVector


def test_main():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau
        TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
        >>> print(tau)
        <a: 1/10, ab: 3/5, c: 3/10> ==> a
        >>> tau.a
        Fraction(1, 10)
        >>> tau.b
        0
        >>> tau.c
        Fraction(3, 10)
        >>> tau.ab
        Fraction(3, 5)
        >>> tau.ba  # Alternate notation for tau.ab
        Fraction(3, 5)
        >>> tau.ac
        0
        >>> tau.ca  # Alternate notation for tau.ac, etc.
        0
        >>> tau.bc
        0
        >>> tau.cb
        0
        >>> tau.duo_ab
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.duo_ba
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.duo_ac
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.duo_ca
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.duo_bc
        <asymptotic = exp(n*(-9/10 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 1, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.duo_cb
        <asymptotic = exp(n*(-9/10 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 1, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.pivot_weak_ab
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_weak_ba
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_weak_ac
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_weak_ca
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_weak_bc
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.pivot_weak_cb
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.pivot_strict_ab
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_strict_ba
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_strict_ac
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_strict_ca
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_strict_bc
        <asymptotic = exp(- inf)>
        >>> tau.pivot_strict_cb
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tij_abc
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tij_acb
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 \
- log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(3 + sqrt(21)) + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_tij_bac
        <asymptotic = exp(- n/10 + log(n) - log(10) + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tij_bca
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 + \
log(sqrt(15)*2**(1/4)*(sqrt(2) + 2)/(12*sqrt(pi))) + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.pivot_tij_cab
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 \
- log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(sqrt(21) + 7) + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_tij_cba
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.pivot_tjk_abc
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tjk_acb
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tjk_bac
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 \
- log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(3 + sqrt(21)) + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_tjk_bca
        <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 \
- log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(sqrt(21) + 7) + o(1)), \
phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        >>> tau.pivot_tjk_cab
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tjk_cba
        <asymptotic = exp(- n/10 + log(n) - log(10) + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.trio
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_1t_a
        <asymptotic = exp(- inf)>
        >>> tau.trio_1t_b
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) + log(n)/2 \
- 9*log(2)/4 - log(15)/2 - log(pi)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_1t_c
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(3*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_2t_ab
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(12*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_2t_ac
        <asymptotic = exp(- inf)>
        >>> tau.trio_2t_bc
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) + log(n)/2 \
- log(15)/2 - 7*log(2)/4 - log(pi)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_2t_ba
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(12*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau.trio_2t_ca
        <asymptotic = exp(- inf)>
        >>> tau.trio_2t_cb
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) + log(n)/2 \
- log(15)/2 - 7*log(2)/4 - log(pi)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """
    pass


def test_scores():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.scores
        {'a': Fraction(7, 10), 'b': Fraction(3, 5), 'c': Fraction(3, 10)}
    """
    pass


def test_winners():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.winners
        Winners({'a'})
    """
    pass


def test_eq():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau == TauVector({'a': Fraction(10, 100), 'ab': Fraction(60, 100), 'c': Fraction(30, 100)}, symbolic=True)
        True
    """
    pass


def test_isclose():
    """
        >>> tau = TauVector({'ab': 0.4, 'b': 0.6}, symbolic=True)
        >>> tau.isclose(TauVector({'ab': 0.4, 'b': 0.59999999999999999999999999}, symbolic=True))
        True
    """
    pass


def test_standardized_version():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.standardized_version
        TauVector({'a': Fraction(3, 10), 'b': Fraction(1, 10), 'bc': Fraction(3, 5)})
    """
    pass


def test_is_standardized():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.is_standardized
        False
    """
    pass


def test_focus():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.focus
        Focus.DIRECT
    """
    pass


def test_print_weak_pivots():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.print_weak_pivots()
        pivot_weak_ab:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_weak_ac:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_weak_bc:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        trio:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """
    pass


def test_print_all_pivots():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.print_all_pivots()
        pivot_weak_ab:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_weak_ac:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_weak_bc:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        pivot_strict_ab:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_strict_ac:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_strict_bc:  <asymptotic = exp(- inf)>
        pivot_tij_abc:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_tij_acb:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(3 + sqrt(21)) + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_tij_bac:  <asymptotic = exp(- n/10 + log(n) - log(10) + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_tij_bca:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 + log(sqrt(15)*2**(1/4)*(sqrt(2) + 2)/(12*sqrt(pi))) + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        pivot_tij_cab:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(sqrt(21) + 7) + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_tij_cba:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        pivot_tjk_abc:  <asymptotic = exp(- inf)>
        pivot_tjk_acb:  <asymptotic = exp(- inf)>
        pivot_tjk_bac:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(3 + sqrt(21)) + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_tjk_bca:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(42) - log(pi)/2 + log(21)/4 + log(10)/2 + log(sqrt(21) + 7) + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        pivot_tjk_cab:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        pivot_tjk_cba:  <asymptotic = exp(- n/10 + log(n) - log(10) + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        trio:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        trio_1t_a:  <asymptotic = exp(- inf)>
        trio_1t_b:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) + log(n)/2 - 9*log(2)/4 - log(15)/2 - log(pi)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        trio_1t_c:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(3*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        trio_2t_ab:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(12*sqrt(2)*pi/5)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        trio_2t_ac:  <asymptotic = exp(- inf)>
        trio_2t_bc:  <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) + log(n)/2 - log(15)/2 - 7*log(2)/4 - log(pi)/2 + o(1)), phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        duo_ab:  <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        duo_ac:  <asymptotic = exp(n*(-1 + sqrt(21)/5) - log(n)/2 - log(2*sqrt(21)*pi/5)/2 + o(1)), phi_a = sqrt(21)/7, phi_c = sqrt(21)/3, phi_ab = sqrt(21)/7>
        duo_bc:  <asymptotic = exp(n*(-9/10 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 1, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """
    pass


def test_d_ranking_best_response():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)}, symbolic=True)
        >>> tau.d_ranking_best_response['abc']
        <ballot = a, utility_threshold = 1, justification = Asymptotic method>
    """
    pass
