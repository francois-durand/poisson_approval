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
        >>> from poisson_approval import TauVector
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(6, 10), 'c': Fraction(3, 10)})
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> from poisson_approval import TauVector
        >>> tau = TauVector({'a': Fraction(1, 6), 'b': Fraction(1, 6), 'c': Fraction(1, 6),
        ...                  'ab': Fraction(1, 6), 'ac': Fraction(1, 6), 'bc': Fraction(1, 6)})
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', tau=tau)
        <asymptotic = exp(? log n + ? + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, phi_ac = 1, phi_bc = 1>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        ce = self.ce
        is_cross_diagram = (tau_x == 0 and tau_yz == 0) or (tau_y == 0 and tau_xz == 0) or (tau_z == 0 and tau_xy == 0)
        is_flower_diagram = ((tau_x == 0 and tau_xy == 0) or (tau_x == 0 and tau_xz == 0)
                             or (tau_y == 0 and tau_xy == 0) or (tau_y == 0 and tau_yz == 0)
                             or (tau_z == 0 and tau_xz == 0) or (tau_z == 0 and tau_yz == 0))
        if is_cross_diagram or is_flower_diagram:
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, tau_yz, symbolic=self.symbolic)
                               * Asymptotic.poisson_eq(tau_y, tau_xz, symbolic=self.symbolic)
                               * Asymptotic.poisson_eq(tau_z, tau_xy, symbolic=self.symbolic))
            self._phi_x = ce.simplify(ce.sqrt(ce.S(tau_yz) / tau_x)) if tau_x > 0 else ce.nan
            self._phi_y = ce.simplify(ce.sqrt(ce.S(tau_xz) / tau_y)) if tau_y > 0 else ce.nan
            self._phi_z = ce.simplify(ce.sqrt(ce.S(tau_xy) / tau_z)) if tau_z > 0 else ce.nan
            self._phi_yz = ce.simplify(ce.sqrt(ce.S(tau_x) / tau_yz)) if tau_yz > 0 else ce.nan
            self._phi_xz = ce.simplify(ce.sqrt(ce.S(tau_y) / tau_xz)) if tau_xz > 0 else ce.nan
            self._phi_xy = ce.simplify(ce.sqrt(ce.S(tau_z) / tau_xy)) if tau_xy > 0 else ce.nan
        elif tau_xy == 0 and tau_xz == 0 and tau_yz == 0:
            # Tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross diagram.
            self.asymptotic = Asymptotic(
                mu=ce.simplify(3 * ce.S(tau_x * tau_y * tau_z) ** ce.Rational(1, 3) - 1), nu=ce.nan, xi=ce.nan,
                symbolic=self.symbolic)
            self._phi_x = ce.simplify((ce.S(tau_y * tau_z) / tau_x ** 2) ** ce.Rational(1, 3))
            self._phi_y = ce.simplify((ce.S(tau_x * tau_z) / tau_y ** 2) ** ce.Rational(1, 3))
            self._phi_z = ce.simplify((ce.S(tau_x * tau_y) / tau_z ** 2) ** ce.Rational(1, 3))
            self._phi_xy = ce.nan
            self._phi_xz = ce.nan
            self._phi_yz = ce.nan
        elif tau_x == 0 and tau_y == 0 and tau_z == 0:
            # Inverted tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross
            # diagram.
            self.asymptotic = Asymptotic(
                mu=ce.simplify(3 * ce.S(tau_xy * tau_xz * tau_yz) ** ce.Rational(1, 3) - 1), nu=ce.nan, xi=ce.nan,
                symbolic=self.symbolic)
            self._phi_x = ce.nan
            self._phi_y = ce.nan
            self._phi_z = ce.nan
            self._phi_xy = ce.simplify((ce.S(tau_xz * tau_yz) / tau_xy ** 2) ** ce.Rational(1, 3))
            self._phi_xz = ce.simplify((ce.S(tau_xy * tau_yz) / tau_xz ** 2) ** ce.Rational(1, 3))
            self._phi_yz = ce.simplify((ce.S(tau_xy * tau_xz) / tau_yz ** 2) ** ce.Rational(1, 3))
        elif tau_x - tau_yz == tau_y - tau_xz == tau_z - tau_xy:
            # Natural general tie.
            # This would work in the general case, but we can avoid numeric approximations easily!
            self.asymptotic = Asymptotic(mu=0, nu=ce.nan, xi=ce.nan, symbolic=self.symbolic)
            self._phi_x = ce.S(1) if tau_x > 0 else ce.nan
            self._phi_y = ce.S(1) if tau_y > 0 else ce.nan
            self._phi_z = ce.S(1) if tau_z > 0 else ce.nan
            self._phi_xy = ce.S(1) if tau_xy > 0 else ce.nan
            self._phi_xz = ce.S(1) if tau_xz > 0 else ce.nan
            self._phi_yz = ce.S(1) if tau_yz > 0 else ce.nan
        else:
            # Generic case: we work with floats, not sympy expressions.
            tau_x_f, tau_y_f, tau_z_f = float(tau_x), float(tau_y), float(tau_z)
            tau_xy_f, tau_xz_f, tau_yz_f = float(tau_xy), float(tau_xz), float(tau_yz)
            optimizer = minimize(
                lambda x: 2 * np.sqrt(
                    (tau_x_f * x[0] + tau_xz_f) * (tau_yz_f / x[0] + tau_y_f)
                ) + tau_xy_f * x[0] + tau_z_f / x[0] - 1,
                np.array([1 + 1e-10, 1.]),  # We don't start exactly at 1. to avoid some (rare) bugs
                bounds=((1E-14, None), (1., 1.))
            )
            self.asymptotic = Asymptotic(mu=ce.S(optimizer.fun), nu=ce.nan, xi=ce.nan, symbolic=self.symbolic)
            x_2 = ce.S(optimizer.x[0])
            x_1 = ce.simplify(ce.sqrt((ce.S(tau_yz) / x_2 + tau_y) / (tau_x * x_2 + tau_xz)))
            self._phi_x = ce.simplify(x_1 * x_2) if tau_x > 0 else ce.nan
            self._phi_y = ce.simplify(ce.S(1) / x_1) if tau_y > 0 else ce.nan
            self._phi_xz = x_1 if tau_xz > 0 else ce.nan
            self._phi_yz = ce.simplify(ce.S(1) / (x_1 * x_2)) if tau_yz > 0 else ce.nan
            self._phi_xy = x_2 if tau_xy > 0 else ce.nan
            self._phi_z = ce.simplify(1 / x_2) if tau_z > 0 else ce.nan
