from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventTrio import EventTrio


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
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_ab=Fraction(1, 10), tau_c=Fraction(9, 10))
        <asymptotic = exp(- 0.4 n - 0.5 log n - 1.35667 + o(1)), phi_c = 0.333333, phi_ab = 3>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_a=Fraction(1, 6), tau_b=Fraction(1, 6), tau_c=Fraction(1, 6),
        ...                  tau_ab=Fraction(1, 6), tau_ac=Fraction(1, 6), tau_bc=Fraction(1, 6))
        <asymptotic = exp(- 0.5 log n - 1.40935 + o(1)), phi_a = 1, phi_b = 1, phi_c = 1, phi_ab = 1, phi_ac = 1, \
phi_bc = 1>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_b=Fraction(1, 2), tau_ac=Fraction(1, 2))
        <asymptotic = exp(- inf)>
        >>> EventPivotStrict(candidate_x='a', candidate_y='b', candidate_z='c',
        ...                  tau_a=Fraction(1, 9), tau_b=Fraction(1, 9),
        ...                  tau_ab=Fraction(1, 9), tau_ac=Fraction(1, 3), tau_bc=Fraction(1, 3))
        <asymptotic = exp(- 0.0181103 n + ? log n + ? + o(1)), phi_a = 1.17454, phi_b = 1.17454, phi_ab = 1.37954, \
phi_ac = 0.851397, phi_bc = 0.851397>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        ce = self.ce
        if (tau_x == 0 and tau_xz == 0) or (tau_y == 0 and tau_yz == 0):
            # Consecutive holes on one side
            # Piv = P(X_x = 0) P(X_y = 0) P(X_xz = 0) P(X_yz = 0) P(X_xy > X_z)
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, 0, symbolic=self.symbolic)
                               * Asymptotic.poisson_eq(tau_y, 0, symbolic=self.symbolic)
                               * Asymptotic.poisson_eq(tau_xz, 0, symbolic=self.symbolic)
                               * Asymptotic.poisson_eq(tau_yz, 0, symbolic=self.symbolic)
                               * Asymptotic.poisson_gt(tau_xy, tau_z, symbolic=self.symbolic))
            self._phi_x = ce.S(0) if tau_x > 0 else ce.nan
            self._phi_y = ce.S(0) if tau_y > 0 else ce.nan
            self._phi_xz = ce.S(0) if tau_xz > 0 else ce.nan
            self._phi_yz = ce.S(0) if tau_yz > 0 else ce.nan
            if tau_xy >= tau_z:
                self._phi_xy = ce.S(1) if tau_xy > 0 else ce.nan
                self._phi_z = ce.S(1) if tau_z > 0 else ce.nan
            else:
                self._phi_xy = ce.simplify(ce.sqrt(ce.S(tau_z) / tau_xy)) if tau_xy > 0 else ce.nan
                self._phi_z = ce.simplify(ce.sqrt(ce.S(tau_xy) / tau_z)) if tau_z > 0 else ce.nan
        else:
            w_x = ce.S(tau_x + tau_xz)  # > 0
            w_y = ce.S(tau_y + tau_yz)  # > 0
            s_x = ce.simplify(tau_xy + tau_x * ce.sqrt(w_y / w_x))
            s_z = ce.simplify(tau_z + tau_yz * ce.sqrt(w_x / w_y))
            if ce.look_equal(s_x, s_z):
                if tau_z != 0 or tau_xy != 0 or (tau_x != 0 and tau_y != 0 and tau_xz != 0 and tau_yz != 0):
                    self.asymptotic = Asymptotic.poisson_eq(w_x, w_y, symbolic=self.symbolic) * ce.Rational(1, 2)
                    self._phi_x = ce.simplify(ce.sqrt(ce.S(w_y) / w_x)) if tau_x > 0 else ce.nan
                    self._phi_xz = ce.simplify(ce.sqrt(ce.S(w_y) / w_x)) if tau_xz > 0 else ce.nan
                    self._phi_y = ce.simplify(ce.sqrt(ce.S(w_x) / w_y)) if tau_y > 0 else ce.nan
                    self._phi_yz = ce.simplify(ce.sqrt(ce.S(w_x) / w_y)) if tau_yz > 0 else ce.nan
                    self._phi_z = ce.S(1) if tau_z > 0 else ce.nan
                    self._phi_xy = ce.S(1) if tau_xy > 0 else ce.nan
                else:
                    self.asymptotic = Asymptotic(mu=-ce.inf, nu=-ce.inf, xi=-ce.inf, symbolic=self.symbolic)
                    self._phi_x = ce.nan
                    self._phi_y = ce.nan
                    self._phi_z = ce.nan
                    self._phi_xy = ce.nan
                    self._phi_xz = ce.nan
                    self._phi_yz = ce.nan
            elif s_x > s_z:
                # "Easy" pivot
                # P(piv_ab) ~ P(S_a = S_b)
                self.asymptotic = Asymptotic.poisson_eq(w_x, w_y, symbolic=self.symbolic)
                self._phi_x = ce.simplify(ce.sqrt(ce.S(w_y) / w_x)) if tau_x > 0 else ce.nan
                self._phi_xz = ce.simplify(ce.sqrt(ce.S(w_y) / w_x)) if tau_xz > 0 else ce.nan
                self._phi_y = ce.simplify(ce.sqrt(ce.S(w_x) / w_y)) if tau_y > 0 else ce.nan
                self._phi_yz = ce.simplify(ce.sqrt(ce.S(w_x) / w_y)) if tau_yz > 0 else ce.nan
                self._phi_z = ce.S(1) if tau_z > 0 else ce.nan
                self._phi_xy = ce.S(1) if tau_xy > 0 else ce.nan
            else:
                # "Difficult" pivot
                # mu_ab = mu_abc
                pivot_trio = EventTrio('x', 'y', 'z', symbolic=self.symbolic,
                                       tau_x=tau_x, tau_y=tau_y, tau_z=tau_z,
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
                    _phi_z_tilde = ce.simplify(self._phi_xz * self._phi_yz)
                if _phi_z_tilde == 0:
                    # The general formula for the asymptotic would be valid, but I prefer to forbid multiplication by 0
                    # in ``Asymptotic``, so that I have to validate such cases explicitly.
                    self.asymptotic = Asymptotic(mu=-ce.inf, nu=-ce.inf, xi=-ce.inf, symbolic=self.symbolic)
                    # Also, the offsets are different in that case: they are not defined.
                    self._phi_x = ce.nan
                    self._phi_y = ce.nan
                    self._phi_z = ce.nan
                    self._phi_xy = ce.nan
                    self._phi_xz = ce.nan
                    self._phi_yz = ce.nan
                else:
                    self.asymptotic = pivot_trio.asymptotic * (_phi_z_tilde / (1 - _phi_z_tilde))
