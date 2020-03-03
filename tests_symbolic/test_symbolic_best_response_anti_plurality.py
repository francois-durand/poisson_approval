from fractions import Fraction
from poisson_approval import TauVector, BestResponseAntiPlurality, ANTI_PLURALITY, UTILITY_DEPENDENT


def test_best_response_anti_plurality():
    """
        >>> tau = TauVector({'ab': Fraction(9, 15), 'ac': Fraction(4, 15), 'bc': Fraction(2, 15)},
        ...                 symbolic=True, voting_rule=ANTI_PLURALITY)
        >>> best_response = BestResponseAntiPlurality(tau, 'abc')
        >>> print(best_response._str_very_verbose)
        tau = <ab: 3/5, ac: 4/15, bc: 2/15> ==> a (Anti-plurality)
        ranking = abc
        voting_rule  = Anti-plurality
        duo_ij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ji = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ik = <asymptotic = exp(n*(-11/15 + 2*sqrt(2)/5) - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_ab = sqrt(2)/3, phi_ac = 1, phi_bc = 3*sqrt(2)/2>
        duo_ki = <asymptotic = exp(n*(-11/15 + 2*sqrt(2)/5) - log(n)/2 - log(4*sqrt(2)*pi/5)/2 + o(1)), phi_ab = sqrt(2)/3, phi_ac = 1, phi_bc = 3*sqrt(2)/2>
        duo_jk = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_ab = 2/3, phi_ac = 3/2, phi_bc = 1>
        duo_kj = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/5)/2 + o(1)), phi_ab = 2/3, phi_ac = 3/2, phi_bc = 1>
        pivot_weak_ij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_weak_ji = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_weak_ik = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_weak_ki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_weak_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_weak_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_strict_ij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_strict_ji = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_strict_ik = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_strict_ki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_strict_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_strict_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tij_ijk = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij_ikj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tij_jik = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + log(1 + sqrt(2)) + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij_jki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tij_kij = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tij_kji = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tjk_ijk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tjk_ikj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tjk_jik = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tjk_jki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_tjk_kij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tjk_kji = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + log(1 + sqrt(2)) + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij = <asymptotic = exp(n*(-2/5 + 4*sqrt(2)/15) - log(n)/2 - log(8*sqrt(2)*pi/15)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_ab = 1, phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tjk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_1t_i = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_1t_j = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_1t_k = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_ij = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_ji = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_ik = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_ki = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_jk = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        trio_2t_kj = <asymptotic = exp(n*(-1 + 2*3**(2/3)/5) + ? log(n) + ? + o(1)), phi_ab = 2*3**(2/3)/9, phi_ac = 3**(2/3)/2, phi_bc = 3**(2/3)>
        pivot_ij_easy_or_tight = True
        pivot_ji_easy_or_tight = True
        pivot_ik_easy_or_tight = False
        pivot_ki_easy_or_tight = False
        pivot_jk_easy_or_tight = False
        pivot_kj_easy_or_tight = False
        threshold_utility = 1
        justification = Anti-plurality analysis
        ballot = ac
    """
    pass
