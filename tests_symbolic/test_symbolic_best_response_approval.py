from fractions import Fraction
from poisson_approval import TauVector, BestResponseApproval, isnan, RANKINGS


def test_best_response_approval():
    """
        >>> tau = TauVector({'a': Fraction(9, 15), 'b': Fraction(4, 15), 'ac': Fraction(1, 15), 'bc': Fraction(1, 15)},
        ...                 symbolic=True)
        >>> best_response = BestResponseApproval(tau, 'abc')
        >>> print(best_response._str_very_verbose)
        tau = <a: 3/5, ac: 1/15, b: 4/15, bc: 1/15> ==> a
        ranking = abc
        voting_rule  = Approval
        duo_ij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ji = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        duo_ik = <asymptotic = exp(- 4*n/15 - log(n)/2 - log(4*pi/5)/2 + o(1)), phi_a = 1/3, phi_b = 1, phi_ac = 1, phi_bc = 3>
        duo_ki = <asymptotic = exp(- 4*n/15 - log(n)/2 - log(4*pi/5)/2 + o(1)), phi_a = 1/3, phi_b = 1, phi_ac = 1, phi_bc = 3>
        duo_jk = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/15)/2 + o(1)), phi_a = 1, phi_b = 1/2, phi_ac = 2, phi_bc = 1>
        duo_kj = <asymptotic = exp(- n/15 - log(n)/2 - log(8*pi/15)/2 + o(1)), phi_a = 1, phi_b = 1/2, phi_ac = 2, phi_bc = 1>
        pivot_weak_ij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_weak_ji = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_weak_ik = <asymptotic = exp(- n/3 - log(n) + log(5*sqrt(6)/(4*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_weak_ki = <asymptotic = exp(- n/3 - log(n) + log(5*sqrt(6)/(4*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_weak_jk = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/45) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_weak_kj = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/45) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_strict_ij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_strict_ji = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_strict_ik = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_strict_ki = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_strict_jk = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_strict_kj = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tij_ijk = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij_ikj = <asymptotic = exp(- n/3 - log(n) + log(35*sqrt(6)/(24*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tij_jik = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + log(1 + sqrt(2)) + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij_jki = <asymptotic = exp(- n/3 - log(n) + log(35*sqrt(6)/(32*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tij_kij = <asymptotic = exp(- n/3 - log(n) + log(5*sqrt(6)/pi) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tij_kji = <asymptotic = exp(- n/3 - log(n) + log(45*sqrt(6)/(16*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tjk_ijk = <asymptotic = exp(- n/3 - log(n) - log(16*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tjk_ikj = <asymptotic = exp(- n/3 - log(n) + log(35*sqrt(6)/(48*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tjk_jik = <asymptotic = exp(- n/3 - log(n) + log(5*sqrt(6)/(12*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tjk_jki = <asymptotic = exp(- n/3 - log(n) + log(35*sqrt(6)/(16*pi)) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_tjk_kij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tjk_kji = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + log(1 + sqrt(2)) + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tij = <asymptotic = exp(n*(-1 + 2*sqrt(2)/3) - log(n)/2 - log(4*sqrt(2)*pi/3)/2 + log(sqrt(2)/2 + 1) + o(1)), phi_a = sqrt(2)/2, phi_b = sqrt(2), phi_ac = sqrt(2)/2, phi_bc = sqrt(2)>
        pivot_tjk = <asymptotic = exp(- n/3 - log(n) - log(16*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_1t_i = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/5) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_1t_j = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_1t_k = <asymptotic = exp(- n/3 - log(n) - log(2*sqrt(6)*pi/45) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_ij = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/5) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_ji = <asymptotic = exp(- n/3 - log(n) - log(8*sqrt(6)*pi/5) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_ik = <asymptotic = exp(- n/3 - log(n) - log(2*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_ki = <asymptotic = exp(- n/3 - log(n) - log(2*sqrt(6)*pi/15) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_jk = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/45) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        trio_2t_kj = <asymptotic = exp(- n/3 - log(n) - log(4*sqrt(6)*pi/45) + o(1)), phi_a = 1/3, phi_b = 1/2, phi_ac = 2, phi_bc = 3>
        pivot_ij_easy_or_tight = True
        pivot_ji_easy_or_tight = True
        pivot_ik_easy_or_tight = False
        pivot_ki_easy_or_tight = False
        pivot_jk_easy_or_tight = False
        pivot_kj_easy_or_tight = False
        utility_threshold = 1
        justification = Easy vs difficult pivot
        ballot = a
    """
    pass
