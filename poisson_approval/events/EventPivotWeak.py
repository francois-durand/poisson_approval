from math import sqrt, isclose
import numpy as np
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventTrio import EventTrio


class EventPivotWeak(Event):
    """A 2-candidate weak pivot.

    Notes
    -----
    We consider the weak pivot between ``x`` and ``y``, i.e. situations where ``S_x = S_y >= S_z``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> event = EventPivotWeak(candidate_x='c', candidate_y='b', candidate_z='a', tau_a=0.1, tau_ab=0.6, tau_c=0.3)
        >>> event
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> print(event.asymptotic)
        exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1))
        >>> event.mu
        -0.151471862576143
        >>> event.nu
        -0.5
        >>> event.xi
        -0.8368125164616638
        >>> event.phi_a
        0.0
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        if (tau_x == 0 and tau_xz == 0) or (tau_y == 0 and tau_yz == 0):
            # Consecutive holes on one side
            # Piv = P(X_x = 0) P(X_y = 0) P(X_xz = 0) P(X_yz = 0) P(X_xy >= X_z)
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, 0) * Asymptotic.poisson_eq(tau_y, 0)
                               * Asymptotic.poisson_eq(tau_xz, 0) * Asymptotic.poisson_eq(tau_yz, 0)
                               * Asymptotic.poisson_ge(tau_xy, tau_z))
            self._phi_x = 0 if tau_x > 0 else np.nan
            self._phi_y = 0 if tau_y > 0 else np.nan
            self._phi_xz = 0 if tau_xz > 0 else np.nan
            self._phi_yz = 0 if tau_yz > 0 else np.nan
            if tau_xy >= tau_z:
                self._phi_xy = 1 if tau_xy > 0 else np.nan
                self._phi_z = 1 if tau_z > 0 else np.nan
            else:
                self._phi_xy = sqrt(tau_z / tau_xy) if tau_xy > 0 else np.nan
                self._phi_z = sqrt(tau_xy / tau_z) if tau_z > 0 else np.nan
        else:
            w_x = tau_x + tau_xz  # > 0
            w_y = tau_y + tau_yz  # > 0
            s_x = tau_xy + tau_x * sqrt(w_y / w_x)
            s_z = tau_z + tau_yz * sqrt(w_x / w_y)
            if isclose(s_x, s_z):
                if tau_z != 0 or tau_xy != 0 or (tau_x != 0 and tau_y != 0 and tau_xz != 0 and tau_yz != 0):
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y) * (1 / 2)
                else:
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
                self._phi_x = sqrt(w_y / w_x) if tau_x > 0 else np.nan
                self._phi_xz = sqrt(w_y / w_x) if tau_xz > 0 else np.nan
                self._phi_y = sqrt(w_x / w_y) if tau_y > 0 else np.nan
                self._phi_yz = sqrt(w_x / w_y) if tau_yz > 0 else np.nan
                self._phi_z = 1 if tau_z > 0 else np.nan
                self._phi_xy = 1 if tau_xy > 0 else np.nan
            elif s_x > s_z:
                # "Easy" pivot
                # P(piv_ab) ~ P(S_a = S_b)
                self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
                self._phi_x = sqrt(w_y / w_x) if tau_x > 0 else np.nan
                self._phi_xz = sqrt(w_y / w_x) if tau_xz > 0 else np.nan
                self._phi_y = sqrt(w_x / w_y) if tau_y > 0 else np.nan
                self._phi_yz = sqrt(w_x / w_y) if tau_yz > 0 else np.nan
                self._phi_z = 1 if tau_z > 0 else np.nan
                self._phi_xy = 1 if tau_xy > 0 else np.nan
            else:
                # "Difficult" pivot
                # mu_ab = mu_abc
                pivot_trio = EventTrio('x', 'y', 'z', tau_x=tau_x, tau_y=tau_y, tau_z=tau_z,
                                       tau_xy=tau_xy, tau_xz=tau_xz, tau_yz=tau_yz)
                self._phi_x = pivot_trio.phi['x']
                self._phi_y = pivot_trio.phi['y']
                self._phi_z = pivot_trio.phi['z']
                self._phi_xy = pivot_trio.phi['xy']
                self._phi_xz = pivot_trio.phi['xz']
                self._phi_yz = pivot_trio.phi['yz']
                if tau_z > 0:
                    _phi_z_tilde = self._phi_z
                else:
                    _phi_z_tilde = self._phi_xz * self._phi_yz
                # print(_phi_z_tilde)
                # print(1 / (1 - _phi_z_tilde))
                self.asymptotic = pivot_trio.asymptotic * (1 / (1 - _phi_z_tilde))


if __name__ == '__main__':
    tau = {'tau_a': 1/10, 'tau_b': 4/10, 'tau_ac': 4/10, 'tau_bc': 1/10}
    print('EventPivotWeak ab')
    pivot = EventPivotWeak('a', 'b', 'c', **tau)
    print(pivot)
    pivot = EventPivotWeak('b', 'a', 'c', **tau)
    print(pivot)
    print('EventPivotWeak ac')
    pivot = EventPivotWeak('a', 'c', 'b', **tau)
    print(pivot)
    pivot = EventPivotWeak('c', 'a', 'b', **tau)
    print(pivot)
    print('EventPivotWeak bc')
    pivot = EventPivotWeak('b', 'c', 'a', **tau)
    print(pivot)
    pivot = EventPivotWeak('c', 'b', 'a', **tau)
    print(pivot)
