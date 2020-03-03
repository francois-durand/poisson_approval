from poisson_approval import EventTrio, TauVector


def test():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)}, symbolic=True)
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> tau = TauVector({'a': Fraction(1, 6), 'b': Fraction(1, 6), 'c': Fraction(1, 6),
        ...                  'ab': Fraction(1, 6), 'ac': Fraction(1, 6), 'bc': Fraction(1, 6)}, symbolic=True)
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(? log(n) + ? + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, phi_ac = 1, phi_bc = 1>
    """
    pass
