from math import sqrt
import numpy as np
from poisson_approval.events.Event import Event
from poisson_approval.events.Asymptotic import Asymptotic


class EventDuo(Event):
    """A 2-candidate tie.

    Notes
    -----
    We consider the situations where ``S_x = S_y``. It is not necessary a pivot, because ``z`` can
    have a greater score.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> EventDuo(candidate_x='a', candidate_y='b', candidate_z='c', tau_a=0.1, tau_ab=0.6, tau_c=0.3)
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        w_x = tau_x + tau_xz
        w_y = tau_y + tau_yz
        self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
        self._phi_x = sqrt(w_y / w_x) if tau_x > 0 else np.nan
        self._phi_xz = sqrt(w_y / w_x) if tau_xz > 0 else np.nan
        self._phi_y = sqrt(w_x / w_y) if tau_y > 0 else np.nan
        self._phi_yz = sqrt(w_x / w_y) if tau_yz > 0 else np.nan
        self._phi_z = 1 if tau_z > 0 else np.nan
        self._phi_xy = 1 if tau_xy > 0 else np.nan
