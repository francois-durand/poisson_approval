import sympy as sp
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventTrio import EventTrio
from poisson_approval.utils.Util import look_equal


class EventPivotStrict(Event):
    """A 2-candidate strict pivot.

    Notes
    -----
    We consider the strict pivot between ``x`` and ``y``, i.e. situations where ``S_x = S_y > S_z``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> from fractions import Fraction
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_ab=Fraction(1, 10), tau_c=Fraction(9, 10))
        <asymptotic = exp(- 2*n/5 - log(n)/2 - log(54*pi/5)/2 - log(2/3) + o(1)), phi_c = 1/3, phi_ab = 3>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_a=Fraction(1, 6), tau_b=Fraction(1, 6), tau_c=Fraction(1, 6),
        ...                  tau_ab=Fraction(1, 6), tau_ac=Fraction(1, 6), tau_bc=Fraction(1, 6))
        <asymptotic = exp(- log(n)/2 - log(4*pi/3)/2 - log(2) + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, \
phi_ac = 1, phi_bc = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_b=Fraction(1, 2), tau_ac=Fraction(1, 2))
        <asymptotic = exp(- inf)>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_a=Fraction(1, 9), tau_b=Fraction(1, 9),
        ...                  tau_ab=Fraction(1, 9), tau_ac=Fraction(1, 3), tau_bc=Fraction(1, 3))
        <asymptotic = exp(- 0.0181103257825368*n + ? log(n) + ? + o(1)), phi_a = 1.1745395129505587, \
phi_b = 1.1745395129505587, phi_ab = 1.3795430674821356, phi_ac = 0.8513974957623195, phi_bc = 0.8513974957623194>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        if (tau_x == 0 and tau_xz == 0) or (tau_y == 0 and tau_yz == 0):
            # Consecutive holes on one side
            # Piv = P(X_x = 0) P(X_y = 0) P(X_xz = 0) P(X_yz = 0) P(X_xy > X_z)
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, 0) * Asymptotic.poisson_eq(tau_y, 0)
                               * Asymptotic.poisson_eq(tau_xz, 0) * Asymptotic.poisson_eq(tau_yz, 0)
                               * Asymptotic.poisson_gt(tau_xy, tau_z))
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
            s_x = tau_xy + tau_x * sp.sqrt(w_y / w_x)
            s_z = tau_z + tau_yz * sp.sqrt(w_x / w_y)
            if look_equal(s_x, s_z):
                if tau_z != 0 or tau_xy != 0 or (tau_x != 0 and tau_y != 0 and tau_xz != 0 and tau_yz != 0):
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y) * sp.Rational(1, 2)
                    self._phi_x = sp.sqrt(sp.S(w_y) / w_x) if tau_x > 0 else sp.nan
                    self._phi_xz = sp.sqrt(sp.S(w_y) / w_x) if tau_xz > 0 else sp.nan
                    self._phi_y = sp.sqrt(sp.S(w_x) / w_y) if tau_y > 0 else sp.nan
                    self._phi_yz = sp.sqrt(sp.S(w_x) / w_y) if tau_yz > 0 else sp.nan
                    self._phi_z = sp.S(1) if tau_z > 0 else sp.nan
                    self._phi_xy = sp.S(1) if tau_xy > 0 else sp.nan
                else:
                    self.asymptotic = Asymptotic(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
                    self._phi_x = sp.nan
                    self._phi_y = sp.nan
                    self._phi_z = sp.nan
                    self._phi_xy = sp.nan
                    self._phi_xz = sp.nan
                    self._phi_yz = sp.nan
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
                if _phi_z_tilde == 0:
                    # The general formula for the asymptotic would be valid, but I prefer to forbid multiplication by 0
                    # in ``Asymptotic``, so that I have to validate such cases explicitly.
                    self.asymptotic = Asymptotic(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
                    # Also, the offsets are different in that case: they are not defined.
                    self._phi_x = sp.nan
                    self._phi_y = sp.nan
                    self._phi_z = sp.nan
                    self._phi_xy = sp.nan
                    self._phi_xz = sp.nan
                    self._phi_yz = sp.nan
                else:
                    self.asymptotic = pivot_trio.asymptotic * (_phi_z_tilde / (1 - _phi_z_tilde))
