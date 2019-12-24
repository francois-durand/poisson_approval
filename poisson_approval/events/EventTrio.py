from scipy.optimize import minimize
from math import sqrt
import numpy as np
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
        >>> EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', tau_a=0.1, tau_ab=0.6, tau_c=0.3)
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        is_cross_diagram = (tau_x == 0 and tau_yz == 0) or (tau_y == 0 and tau_xz == 0) or (tau_z == 0 and tau_xy == 0)
        is_flower_diagram = ((tau_x == 0 and tau_xy == 0) or (tau_x == 0 and tau_xz == 0)
                             or (tau_y == 0 and tau_xy == 0) or (tau_y == 0 and tau_yz == 0)
                             or (tau_z == 0 and tau_xz == 0) or (tau_z == 0 and tau_yz == 0))
        if is_cross_diagram or is_flower_diagram:
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, tau_yz) * Asymptotic.poisson_eq(tau_y, tau_xz)
                               * Asymptotic.poisson_eq(tau_z, tau_xy))
            self._phi_x = sqrt(tau_yz / tau_x) if tau_x > 0 else np.nan
            self._phi_y = sqrt(tau_xz / tau_y) if tau_y > 0 else np.nan
            self._phi_z = sqrt(tau_xy / tau_z) if tau_z > 0 else np.nan
            self._phi_yz = sqrt(tau_x / tau_yz) if tau_yz > 0 else np.nan
            self._phi_xz = sqrt(tau_y / tau_xz) if tau_xz > 0 else np.nan
            self._phi_xy = sqrt(tau_z / tau_xy) if tau_xy > 0 else np.nan
        elif tau_xy == 0 and tau_xz == 0 and tau_yz == 0:
            # Tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross diagram.
            self.asymptotic = Asymptotic(mu=3 * (tau_x * tau_y * tau_z) ** (1 / 3) - 1, nu=np.nan, xi=np.nan)
            self._phi_x = (tau_y * tau_z / tau_x ** 2) ** (1 / 3)
            self._phi_y = (tau_x * tau_z / tau_y ** 2) ** (1 / 3)
            self._phi_z = (tau_x * tau_y / tau_z ** 2) ** (1 / 3)
            self._phi_xy = np.nan
            self._phi_xz = np.nan
            self._phi_yz = np.nan
        elif tau_x == 0 and tau_y == 0 and tau_z == 0:
            # Inverted tripod. Note that the other coefficient are not 0, otherwise it would be a (degenerate) cross
            # diagram.
            self.asymptotic = Asymptotic(mu=3 * (tau_xy * tau_xz * tau_yz) ** (1 / 3) - 1, nu=np.nan, xi=np.nan)
            self._phi_x = np.nan
            self._phi_y = np.nan
            self._phi_z = np.nan
            self._phi_xy = (tau_xz * tau_yz / tau_xy ** 2) ** (1 / 3)
            self._phi_xz = (tau_xy * tau_yz / tau_xz ** 2) ** (1 / 3)
            self._phi_yz = (tau_xy * tau_xz / tau_yz ** 2) ** (1 / 3)
        elif tau_x - tau_yz == tau_y - tau_xz == tau_z - tau_xy:
            # Natural general tie.
            # This would work in the general case, but we can avoid numeric approximations easily!
            self.asymptotic = Asymptotic(mu=0, nu=np.nan, xi=np.nan)
            self._phi_x = 1 if tau_x > 0 else np.nan
            self._phi_y = 1 if tau_y > 0 else np.nan
            self._phi_z = 1 if tau_z > 0 else np.nan
            self._phi_xy = 1 if tau_xy > 0 else np.nan
            self._phi_xz = 1 if tau_xz > 0 else np.nan
            self._phi_yz = 1 if tau_yz > 0 else np.nan
        else:
            # Generic case
            optimizer = minimize(
                lambda x: 2 * sqrt(
                    (tau_x * x[0] + tau_xz) * (tau_yz / x[0] + tau_y)
                ) + tau_xy * x[0] + tau_z / x[0] - 1,
                np.array([1 + 1e-10, 1.]),  # We don't start exactly at 1. to avoid some (rare) bugs
                bounds=((1E-14, None), (1., 1.))
            )
            self.asymptotic = Asymptotic(mu=optimizer.fun, nu=np.nan, xi=np.nan)
            x_2 = optimizer.x[0]
            x_1 = sqrt((tau_yz / x_2 + tau_y) / (tau_x * x_2 + tau_xz))
            # print('x_2 =', x_2)
            # print('x_1 =', x_1)
            self._phi_x = x_1 * x_2 if tau_x > 0 else np.nan
            self._phi_y = 1 / x_1 if tau_y > 0 else np.nan
            self._phi_xz = x_1 if tau_xz > 0 else np.nan
            self._phi_yz = 1 / (x_1 * x_2) if tau_yz > 0 else np.nan
            self._phi_xy = x_2 if tau_xy > 0 else np.nan
            self._phi_z = 1 / x_2 if tau_z > 0 else np.nan
