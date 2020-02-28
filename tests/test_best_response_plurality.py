from fractions import Fraction
from poisson_approval import TauVector, BestResponsePlurality, PLURALITY, UTILITY_DEPENDENT


def test_best_response_plurality():
    """
        >>> tau = TauVector({'a': Fraction(9, 15), 'b': Fraction(4, 15), 'c': Fraction(2, 15)}, voting_rule=PLURALITY)
        >>> best_response = BestResponsePlurality(tau, 'abc')
        >>> print(best_response._str_very_verbose)
        tau = <a: 3/5, b: 4/15, c: 2/15> ==> a (Plurality)
        ranking = abc
        voting_rule  = Plurality
        duo_ij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        duo_ij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        duo_ji = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        duo_ik = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        duo_ki = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        duo_jk = <asymptotic = exp(- n*(-sqrt(30)/15 + 2*sqrt(15)/15)**2 - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_a = 1, phi_b = sqrt(2)/2, phi_c = sqrt(2)>
        duo_kj = <asymptotic = exp(- n*(-sqrt(30)/15 + 2*sqrt(15)/15)**2 - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_a = 1, phi_b = sqrt(2)/2, phi_c = sqrt(2)>
        pivot_weak_ij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_weak_ji = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_weak_ik = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_weak_ki = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_weak_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_weak_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_strict_ij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_strict_ji = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_strict_ik = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_strict_ki = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_strict_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_strict_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_tij_ijk = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + log(5/3) + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_tij_ikj = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + log(sqrt(2)/3 + 1) + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_tij_jik = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + log(5/2) + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_tij_jki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_tij_kij = <asymptotic = exp(- n*(-sqrt(15)/5 + sqrt(30)/15)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + log(1 + 3*sqrt(2)/2) + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_tij_kji = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_tjk_ijk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_tjk_ikj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_tjk_jik = <asymptotic = exp(- n*(-sqrt(15)/5 + sqrt(30)/15)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + log(sqrt(2)/3 + 1) + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_tjk_jki = <asymptotic = exp(- n*(-sqrt(30)/15 + sqrt(15)/5)**2 - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + log(1 + 3*sqrt(2)/2) + o(1)), phi_a = sqrt(2)/3, phi_b = 1, phi_c = 3*sqrt(2)/2>
        pivot_tjk_kij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + log(5/3) + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_tjk_kji = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + log(5/2) + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_tij = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + log(5/3) + o(1)), phi_a = 2/3, phi_b = 3/2, phi_c = 1>
        pivot_tjk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_1t_i = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_1t_j = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_1t_k = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_ij = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_ji = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_ik = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_ki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        trio_2t_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_a = 2*3**(2/3)/9, phi_b = 3**(2/3)/2, phi_c = 3**(2/3)>
        pivot_ij_easy_or_tight = True
        pivot_ji_easy_or_tight = True
        pivot_ik_easy_or_tight = True
        pivot_ki_easy_or_tight = True
        pivot_jk_easy_or_tight = False
        pivot_kj_easy_or_tight = False
        threshold_utility = 1
        justification = Plurality analysis
        ballot = a
    """
    pass


def test_best_response_is_j():
    tau = TauVector({'a': 1 / 5, 'b': 2 / 5, 'c': 2 / 5}, voting_rule=PLURALITY)
    best_response = BestResponsePlurality(tau, 'abc')
    assert best_response.ballot == 'b'


def test_best_response_is_utility_dependent():
    tau = TauVector({'a': 1 / 5, 'b': 3 / 5, 'c': 1 / 5}, voting_rule=PLURALITY)
    best_response = BestResponsePlurality(tau, 'abc')
    assert best_response.threshold_utility == Fraction(1, 2)
    assert best_response.ballot == UTILITY_DEPENDENT


def test_best_response_is_not_utility_dependent():
    tau = TauVector({'a': 0, 'b': 1, 'c': 0}, voting_rule=PLURALITY)
    best_response = BestResponsePlurality(tau, 'abc')
    assert best_response.ballot == 'a'
