from poisson_approval import EventTrio


def test():
    """
        >>> from fractions import Fraction
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...           tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...           tau_a=Fraction(1, 6), tau_b=Fraction(1, 6), tau_c=Fraction(1, 6),
        ...           tau_ab=Fraction(1, 6), tau_ac=Fraction(1, 6), tau_bc=Fraction(1, 6))
        <asymptotic = exp(? log(n) + ? + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, phi_ac = 1, phi_bc = 1>
    """
    pass
