import sympy as sp
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventTrio import EventTrio
from poisson_approval.utils.Util import isclose


class EventPivotWeak(Event):
    """A 2-candidate weak pivot.

    Notes
    -----
    We consider the weak pivot between ``x`` and ``y``, i.e. situations where ``S_x = S_y >= S_z``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> from fractions import Fraction
        >>> event = EventPivotWeak(candidate_x='c', candidate_y='b', candidate_z='a',
        ...                        tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        >>> event
        <asymptotic = exp(n*(-1/10 - (-sqrt(15)/5 + sqrt(30)/10)**2) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
        >>> print(event.asymptotic)
        exp(n*(-1/10 - (-sqrt(15)/5 + sqrt(30)/10)**2) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1))
        >>> event.mu
        -1/10 - (-sqrt(15)/5 + sqrt(30)/10)**2
        >>> event.nu
        -1/2
        >>> event.xi
        -log(6*sqrt(2)*pi/5)/2
        >>> event.phi_a
        0
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        if (tau_x == 0 and tau_xz == 0) or (tau_y == 0 and tau_yz == 0):
            # Consecutive holes on one side
            # Piv = P(X_x = 0) P(X_y = 0) P(X_xz = 0) P(X_yz = 0) P(X_xy >= X_z)
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, 0) * Asymptotic.poisson_eq(tau_y, 0)
                               * Asymptotic.poisson_eq(tau_xz, 0) * Asymptotic.poisson_eq(tau_yz, 0)
                               * Asymptotic.poisson_ge(tau_xy, tau_z))
            self._phi_x = sp.S(0) if tau_x > 0 else sp.nan
            self._phi_y = sp.S(0) if tau_y > 0 else sp.nan
            self._phi_xz = sp.S(0) if tau_xz > 0 else sp.nan
            self._phi_yz = sp.S(0) if tau_yz > 0 else sp.nan
            if tau_xy >= tau_z:
                self._phi_xy = sp.S(1) if tau_xy > 0 else sp.nan
                self._phi_z = sp.S(1) if tau_z > 0 else sp.nan
            else:
                self._phi_xy = sp.sqrt(sp.S(tau_z) / tau_xy) if tau_xy > 0 else sp.nan
                self._phi_z = sp.sqrt(sp.S(tau_xy) / tau_z) if tau_z > 0 else sp.nan
        else:
            w_x = sp.S(tau_x + tau_xz)  # > 0
            w_y = sp.S(tau_y + tau_yz)  # > 0
            s_x = tau_xy + tau_x * sp.sqrt(sp.S(w_y) / w_x)
            s_z = tau_z + tau_yz * sp.sqrt(sp.S(w_x) / w_y)
            if isclose(s_x, s_z):
                if tau_z != 0 or tau_xy != 0 or (tau_x != 0 and tau_y != 0 and tau_xz != 0 and tau_yz != 0):
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y) * sp.Rational(1, 2)
                else:
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
                self._phi_x = sp.sqrt(sp.S(w_y) / w_x) if tau_x > 0 else sp.nan
                self._phi_xz = sp.sqrt(sp.S(w_y) / w_x) if tau_xz > 0 else sp.nan
                self._phi_y = sp.sqrt(sp.S(w_x) / w_y) if tau_y > 0 else sp.nan
                self._phi_yz = sp.sqrt(sp.S(w_x) / w_y) if tau_yz > 0 else sp.nan
                self._phi_z = sp.S(1) if tau_z > 0 else sp.nan
                self._phi_xy = sp.S(1) if tau_xy > 0 else sp.nan
            elif s_x > s_z:
                # "Easy" pivot
                # P(piv_ab) ~ P(S_a = S_b)
                self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
                self._phi_x = sp.sqrt(sp.S(w_y) / w_x) if tau_x > 0 else sp.nan
                self._phi_xz = sp.sqrt(sp.S(w_y) / w_x) if tau_xz > 0 else sp.nan
                self._phi_y = sp.sqrt(sp.S(w_x) / w_y) if tau_y > 0 else sp.nan
                self._phi_yz = sp.sqrt(sp.S(w_x) / w_y) if tau_yz > 0 else sp.nan
                self._phi_z = sp.S(1) if tau_z > 0 else sp.nan
                self._phi_xy = sp.S(1) if tau_xy > 0 else sp.nan
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
                self.asymptotic = pivot_trio.asymptotic / (1 - _phi_z_tilde)
