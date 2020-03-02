from poisson_approval import EventPivotWeak


def test():
    """
        >>> from fractions import Fraction
        >>> event = EventPivotWeak(candidate_x='c', candidate_y='b', candidate_z='a', symbolic=True,
        ...                        tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
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
