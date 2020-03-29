from poisson_approval import EventPivotStrict, TauVector


def test():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)}, symbolic=True)
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau = TauVector({'ab': Fraction(1, 10), 'c': Fraction(9, 10)}, symbolic=True)
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- 2*n/5 - log(n)/2 - log(54*pi/5)/2 - log(2/3) + o(1)), phi_c = 1/3, phi_ab = 3>
        >>> tau = TauVector({'a': Fraction(1, 6), 'b': Fraction(1, 6), 'c': Fraction(1, 6),
        ...                  'ab': Fraction(1, 6), 'ac': Fraction(1, 6), 'bc': Fraction(1, 6)}, symbolic=True)
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- log(n)/2 + log(sqrt(3)/(4*sqrt(pi))) + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, \
phi_ac = 1, phi_bc = 1>
        >>> tau = TauVector({'b': Fraction(1, 2), 'ac': Fraction(1, 2)}, symbolic=True)
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- inf)>
        >>> tau = TauVector({'a': Fraction(1, 9), 'b': Fraction(1, 9),
        ...                  'ab': Fraction(1, 9), 'ac': Fraction(1, 3), 'bc': Fraction(1, 3)}, symbolic=True)
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)  # doctest: +ELLIPSIS
        <asymptotic = exp(- 0.0181103...*n + ? log(n) + ? + o(1)), phi_a = 1.17453..., \
phi_b = 1.17453..., phi_ab = 1.37953..., phi_ac = 0.851398..., phi_bc = 0.851398...>
    """
    pass
