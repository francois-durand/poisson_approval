from poisson_approval import EventPivotStrict


def test():
    """
        >>> from fractions import Fraction
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...                  tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...                  tau_ab=Fraction(1, 10), tau_c=Fraction(9, 10))
        <asymptotic = exp(- 2*n/5 - log(n)/2 - log(54*pi/5)/2 - log(2/3) + o(1)), phi_c = 1/3, phi_ab = 3>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...                  tau_a=Fraction(1, 6), tau_b=Fraction(1, 6), tau_c=Fraction(1, 6),
        ...                  tau_ab=Fraction(1, 6), tau_ac=Fraction(1, 6), tau_bc=Fraction(1, 6))
        <asymptotic = exp(- log(n)/2 + log(sqrt(3)/(4*sqrt(pi))) + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, \
phi_ac = 1, phi_bc = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...                  tau_b=Fraction(1, 2), tau_ac=Fraction(1, 2))
        <asymptotic = exp(- inf)>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c', symbolic=True,
        ...                  tau_a=Fraction(1, 9), tau_b=Fraction(1, 9),
        ...                  tau_ab=Fraction(1, 9), tau_ac=Fraction(1, 3), tau_bc=Fraction(1, 3))
        <asymptotic = exp(- 0.0181103257825368*n + ? log(n) + ? + o(1)), phi_a = 1.17453951295056, \
phi_b = 1.17453951295056, phi_ab = 1.37954306748214, phi_ac = 0.851397495762319, phi_bc = 0.851397495762319>
    """
    pass
