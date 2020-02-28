import sympy as sp
import numpy as np
from scipy.optimize import minimize
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event


class EventTrio(Event):
    """A 3-candidate tie.

    Notes
    -----
    We consider the 3-way tie, i.e. situations where ``S_x = S_y = S_z``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> from fractions import Fraction
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c',
        ...           tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(n*(-1/10 - (-sqrt(15)/5 + sqrt(30)/10)**2) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c',
        ...           tau_a=Fraction(1, 6), tau_b=Fraction(1, 6), tau_c=Fraction(1, 6),
        ...           tau_ab=Fraction(1, 6), tau_ac=Fraction(1, 6), tau_bc=Fraction(1, 6))
        <asymptotic = exp(? log(n) + ? + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, phi_ac = 1, phi_bc = 1>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        is_cross_diagram = (tau_x == 0 and tau_yz == 0) or (tau_y == 0 and tau_xz == 0) or (tau_z == 0 and tau_xy == 0)
        is_flower_diagram = ((tau_x == 0 and tau_xy == 0) or (tau_x == 0 and tau_xz == 0)
                             or (tau_y == 0 and tau_xy == 0) or (tau_y == 0 and tau_yz == 0)
                             or (tau_z == 0 and tau_xz == 0) or (tau_z == 0 and tau_yz == 0))
        if is_cross_diagram or is_flower_diagram:
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, tau_yz) * Asymptotic.poisson_eq(tau_y, tau_xz)
                               * Asymptotic.poisson_eq(tau_z, tau_xy))
            self._phi_x = sp.sqrt(sp.S(tau_yz) / tau_x) if tau_x > 0 else sp.nan
            self._phi_y = sp.sqrt(sp.S(tau_xz) / tau_y) if tau_y > 0 else sp.nan
            self._phi_z = sp.sqrt(sp.S(tau_xy) / tau_z) if tau_z > 0 else sp.nan
            self._phi_yz = sp.sqrt(sp.S(tau_x) / tau_yz) if tau_yz > 0 else sp.nan
            self._phi_xz = sp.sqrt(sp.S(tau_y) / tau_xz) if tau_xz > 0 else sp.nan
            self._phi_xy = sp.sqrt(sp.S(tau_z) / tau_xy) if tau_xy > 0 else sp.nan
        elif tau_xy == 0 and tau_xz == 0 and tau_yz == 0:
            # Tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross diagram.
            self.asymptotic = Asymptotic(mu=3 * sp.S(tau_x * tau_y * tau_z) ** sp.Rational(1, 3) - 1,
                                         nu=sp.nan, xi=sp.nan)
            self._phi_x = (sp.S(tau_y * tau_z) / tau_x ** 2) ** sp.Rational(1, 3)
            self._phi_y = (sp.S(tau_x * tau_z) / tau_y ** 2) ** sp.Rational(1, 3)
            self._phi_z = (sp.S(tau_x * tau_y) / tau_z ** 2) ** sp.Rational(1, 3)
            self._phi_xy = sp.nan
            self._phi_xz = sp.nan
            self._phi_yz = sp.nan
        elif tau_x == 0 and tau_y == 0 and tau_z == 0:
            # Inverted tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross
            # diagram.
            self.asymptotic = Asymptotic(mu=3 * sp.S(tau_xy * tau_xz * tau_yz) ** sp.Rational(1, 3) - 1,
                                         nu=sp.nan, xi=sp.nan)
            self._phi_x = sp.nan
            self._phi_y = sp.nan
            self._phi_z = sp.nan
            self._phi_xy = (sp.S(tau_xz * tau_yz) / tau_xy ** 2) ** sp.Rational(1, 3)
            self._phi_xz = (sp.S(tau_xy * tau_yz) / tau_xz ** 2) ** sp.Rational(1, 3)
            self._phi_yz = (sp.S(tau_xy * tau_xz) / tau_yz ** 2) ** sp.Rational(1, 3)
        elif tau_x - tau_yz == tau_y - tau_xz == tau_z - tau_xy:
            # Natural general tie.
            # This would work in the general case, but we can avoid numeric approximations easily!
            self.asymptotic = Asymptotic(mu=0, nu=sp.nan, xi=sp.nan)
            self._phi_x = sp.S(1) if tau_x > 0 else sp.nan
            self._phi_y = sp.S(1) if tau_y > 0 else sp.nan
            self._phi_z = sp.S(1) if tau_z > 0 else sp.nan
            self._phi_xy = sp.S(1) if tau_xy > 0 else sp.nan
            self._phi_xz = sp.S(1) if tau_xz > 0 else sp.nan
            self._phi_yz = sp.S(1) if tau_yz > 0 else sp.nan
        else:
            # Generic case
            optimizer = minimize(
                lambda x: 2 * np.sqrt(
                    (tau_x * x[0] + tau_xz) * (tau_yz / x[0] + tau_y)
                ) + tau_xy * x[0] + tau_z / x[0] - 1,
                np.array([1 + 1e-10, 1.]),  # We don't start exactly at 1. to avoid some (rare) bugs
                bounds=((1E-14, None), (1., 1.))
            )
            self.asymptotic = Asymptotic(mu=optimizer.fun, nu=sp.nan, xi=sp.nan)
            x_2 = optimizer.x[0]
            x_1 = np.sqrt((tau_yz / x_2 + tau_y) / (tau_x * x_2 + tau_xz))
            self._phi_x = x_1 * x_2 if tau_x > 0 else sp.nan
            self._phi_y = 1 / x_1 if tau_y > 0 else sp.nan
            self._phi_xz = x_1 if tau_xz > 0 else sp.nan
            self._phi_yz = 1 / (x_1 * x_2) if tau_yz > 0 else sp.nan
            self._phi_xy = x_2 if tau_xy > 0 else sp.nan
            self._phi_z = 1 / x_2 if tau_z > 0 else sp.nan
