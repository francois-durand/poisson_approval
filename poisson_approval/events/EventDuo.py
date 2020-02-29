import sympy as sp
from poisson_approval.events.Event import Event
from poisson_approval.events.Asymptotic import Asymptotic
from poisson_approval.utils.Util import my_simplify


class EventDuo(Event):
    """A 2-candidate tie.

    Notes
    -----
    We consider the situations where ``S_x = S_y``. It is not necessary a pivot, because ``z`` can
    have a greater score.

    For parameters and attributes, cf. :class:`Event`.

    Examples
    --------
        >>> from fractions import Fraction
        >>> EventDuo(candidate_x='a', candidate_y='b', candidate_z='c',
        ...          tau_a=Fraction(1, 10), tau_ab=Fraction(6, 10), tau_c=Fraction(3, 10))
        <asymptotic = exp(- n/10 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
    """

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        w_x = sp.S(tau_x + tau_xz)
        w_y = sp.S(tau_y + tau_yz)
        self.asymptotic = Asymptotic.poisson_eq(w_x, w_y)
        self._phi_x = my_simplify(sp.sqrt(w_y / w_x)) if tau_x > 0 else sp.nan
        self._phi_xz = my_simplify(sp.sqrt(w_y / w_x)) if tau_xz > 0 else sp.nan
        self._phi_y = my_simplify(sp.sqrt(w_x / w_y)) if tau_y > 0 else sp.nan
        self._phi_yz = my_simplify(sp.sqrt(w_x / w_y)) if tau_yz > 0 else sp.nan
        self._phi_z = my_simplify(sp.S(1)) if tau_z > 0 else sp.nan
        self._phi_xy = my_simplify(sp.S(1)) if tau_xy > 0 else sp.nan
