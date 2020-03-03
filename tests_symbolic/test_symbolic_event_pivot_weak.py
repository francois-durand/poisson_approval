from poisson_approval import EventPivotWeak, TauVector


def test():
    """
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)}, symbolic=True)
        >>> event = EventPivotWeak(candidate_x='c', candidate_y='b', candidate_z='a', tau=tau)
        >>> event
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> print(event.asymptotic)
        exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1))
        >>> event.mu
        -1 + 3*sqrt(2)/5
        >>> event.nu
        -1/2
        >>> event.xi
        -log(6*sqrt(2)*pi/5)/2
        >>> event.phi_a
        0
    """
    pass
