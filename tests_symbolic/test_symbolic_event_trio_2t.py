from poisson_approval import EventTrio2t, TauVector


def test():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)}, symbolic=True)
        >>> EventTrio2t(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(12*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """
    pass
