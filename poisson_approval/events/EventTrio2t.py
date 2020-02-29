import sympy as sp
from poisson_approval.utils.Util import isneginf
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.events.Event import Event
from poisson_approval.events.EventTrio import EventTrio
from poisson_approval.utils.Util import my_simplify


class EventTrio2t(Event):
    """A 3-candidate almost-tie of the type (X - 1, X - 1, X).

    Notes
    -----
    We consider the trios of type 1, i.e. situations where ``S_x + 1 = S_y + 1 = S_z``.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> from fractions import Fraction
        >>> EventTrio2t(candidate_x='a', candidate_y='b', candidate_z='c',
        ...             tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(12*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        event_trio = EventTrio(candidate_x='x', candidate_y='y', candidate_z='z',
                               tau_x=tau_x, tau_y=tau_y, tau_z=tau_z, tau_xy=tau_xy, tau_xz=tau_xz, tau_yz=tau_yz)
        self._phi_x = event_trio.phi['x']
        self._phi_y = event_trio.phi['y']
        self._phi_z = event_trio.phi['z']
        self._phi_xy = event_trio.phi['xy']
        self._phi_xz = event_trio.phi['xz']
        self._phi_yz = event_trio.phi['yz']
        if tau_z == 0 and tau_xy == 0:
            # Cross diagram 1
            self.asymptotic = Asymptotic.poisson_one_more(tau_yz, tau_x) * Asymptotic.poisson_one_more(tau_xz, tau_y)
        elif (tau_x == 0 and tau_yz == 0) or (tau_y == 0 and tau_xz == 0):
            # Cross diagram 2
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, tau_yz) * Asymptotic.poisson_eq(tau_y, tau_xz)
                               * Asymptotic.poisson_one_more(tau_z, tau_xy))
        elif (tau_z == 0 and tau_xz == 0) or (tau_z == 0 and tau_yz == 0):
            # Flower diagram 1
            self.asymptotic = Asymptotic(mu=-sp.oo, nu=-sp.oo, xi=-sp.oo)
        elif (tau_x == 0 and tau_xz == 0) or (tau_y == 0 and tau_yz == 0):
            # Flower diagram 2
            self.asymptotic = (Asymptotic.poisson_eq(tau_x, tau_yz) * Asymptotic.poisson_eq(tau_y, tau_xz)
                               * Asymptotic.poisson_one_more(tau_z, tau_xy))
        elif (tau_x == 0 and tau_xy == 0) or (tau_y == 0 and tau_xy == 0):
            # Flower diagram 3
            self.asymptotic = (
                (Asymptotic.poisson_value(tau_z, 0)
                 * Asymptotic.poisson_one_more(tau_yz, tau_x) * Asymptotic.poisson_one_more(tau_xz, tau_y))
                + (Asymptotic.poisson_one_more(tau_z, 1)
                   * Asymptotic.poisson_eq(tau_x, tau_yz) * Asymptotic.poisson_eq(tau_y, tau_xz))
            )
        else:
            _phi_xy_tilde = self._phi_xy if tau_xy != 0 else my_simplify(self._phi_x * self._phi_y)
            self.asymptotic = event_trio.asymptotic * _phi_xy_tilde
        if isneginf(self.asymptotic.mu):
            self._phi_x = sp.nan
            self._phi_y = sp.nan
            self._phi_z = sp.nan
            self._phi_xy = sp.nan
            self._phi_xz = sp.nan
            self._phi_yz = sp.nan
