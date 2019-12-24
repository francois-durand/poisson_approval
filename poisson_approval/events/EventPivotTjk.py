import numpy as np
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventPivotWeak import EventPivotWeak


class EventPivotTjk(Event):
    """A `personalized pivot` of type ``Tjk``.

    Notes
    -----
    We consider the personalized pivot for the two least-liked candidates of a voter ``zyx``, i.e. situations
    where, if the voter add a reasonable ballot (``z`` or ``yz``), it become a strict pivot for ``xy``. In other words,
    situations where ``S_x = S_y > S_z + 1`` or ``S_x = S_y + 1 > S_z + 1``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> EventPivotTjk(candidate_x='a', candidate_y='b', candidate_z='c', tau_a=0.1, tau_ab=0.6, tau_c=0.3)
        <asymptotic = exp(- 0.1 n + log n - 2.30259 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        pivot_weak = EventPivotWeak(candidate_x='x', candidate_y='y', candidate_z='z',
                                    tau_x=tau_x, tau_y=tau_y, tau_z=tau_z, tau_xy=tau_xy, tau_xz=tau_xz, tau_yz=tau_yz)
        self._phi_x = pivot_weak.phi['x']
        self._phi_y = pivot_weak.phi['y']
        self._phi_z = pivot_weak.phi['z']
        self._phi_xy = pivot_weak.phi['xy']
        self._phi_xz = pivot_weak.phi['xz']
        self._phi_yz = pivot_weak.phi['yz']
        if tau_xy == 0 and (tau_x == 0 or tau_y == 0):
            # Flower diagram: holes `at the bottom`, i.e. around ``xy``
            self.asymptotic = Asymptotic(mu=-np.inf, nu=-np.inf, xi=-np.inf)
        elif tau_x == 0 and tau_xz == 0:
            # Flower diagram: consecutive holes on the ``x`` side
            self.asymptotic = (Asymptotic.poisson_value(tau_yz, 0) * Asymptotic.poisson_value(tau_y, 0)
                               * Asymptotic.poisson_gt_one_more(tau_xy, tau_z))
        elif tau_y == 0 and tau_yz == 0:
            # Flower diagram: consecutive holes on the ``y`` side
            self.asymptotic = (
                Asymptotic.poisson_value(tau_x, 0)
                * (Asymptotic.poisson_value(tau_xz, 0) + Asymptotic.poisson_value(tau_xz, 1))
                * Asymptotic.poisson_gt_one_more(tau_xy, tau_z)
            ) + (
                Asymptotic.poisson_value(tau_x, 1)
                * Asymptotic.poisson_value(tau_xz, 0)
                * Asymptotic.poisson_gt(tau_xy, tau_z)
            )
        elif tau_z == 0 and (tau_xz == 0 or tau_yz == 0):
            # Flower diagram: holes `at the top`, i.e. around ``z``
            self.asymptotic = (Asymptotic.poisson_eq(tau_x + tau_xz, tau_y + tau_yz)
                               + Asymptotic.poisson_one_more(tau_x + tau_xz, tau_y + tau_yz))
        else:
            _phi_z_tilde = self._phi_z if tau_z != 0 else self._phi_xz * self._phi_yz
            _phi_y_tilde = self._phi_y if tau_y != 0 else self._phi_xy * self._phi_yz
            self.asymptotic = pivot_weak.asymptotic * (_phi_z_tilde**2 * (1 + _phi_y_tilde))
        if np.isinf(float(self.asymptotic.mu)):
            self._phi_x = np.nan
            self._phi_y = np.nan
            self._phi_z = np.nan
            self._phi_xy = np.nan
            self._phi_xz = np.nan
            self._phi_yz = np.nan
