from poisson_approval import EventPivotTjk, TauVector


def test():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)}, symbolic=True)
        >>> EventPivotTjk(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- n/10 + log(n) - log(10) + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
    """
    pass
