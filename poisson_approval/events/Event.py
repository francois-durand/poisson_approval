from poisson_approval.utils.Util import isnan


class Event:
    """An event with all its attributes: magnitudes, offsets, asymptotic if possible (abstract class).

    Parameters
    ----------
    candidate_x : str
        A candidate (e.g. ``'a'``).
    candidate_y : str
        A candidate (e.g. ``'b'``).
    candidate_z : str
        A candidate (e.g. ``'c'``).
    kwargs
        Use ``tau_..`` for the values of the tau-vector (probability for each kind of ballot). For example, ``tau_a``,
        ``tau_ab``, etc.

    Attributes
    ----------
    asymptotic : Asymptotic
        The asymptotic development of the probability of the event when `n` tends to infinity.
    mu : Number, ``np.nan`` or ``np.inf``
        Shortcut for ``asymptotic.mu``.
    nu : Number, ``np.nan`` or ``np.inf``
        Shortcut for ``asymptotic.nu``.
    xi : Number, ``np.nan`` or ``np.inf``
        Shortcut for ``asymptotic.xi``.
    phi_ab : Number or ``np.nan``
        The offset for this kind of ballot. An offset is ``np.nan`` if it is not defined.
        Other offsets are denoted ``phi_a``, etc.

    Notes
    -----
    The permutation of ``candidate_x``, ``candidate_y`` and ``candidate_z`` is generally important in the subclasses.
    For example, in :class:`EventDuo`, we consider a tie between candidates ``x`` and ``y`` (hence in that case, if is
    the same if ``x`` and ``y`` are exchanged, but not if ``x`` and ``z`` are exchanged for example).

    Examples
    --------
    Cf. :class:`EventPivotWeak`.
    """

    def __init__(self, candidate_x, candidate_y, candidate_z, **kwargs):
        # -------------
        # Preliminaries
        # -------------
        # Create labels
        self._label_x, self._label_y, self._label_z = candidate_x, candidate_y, candidate_z
        self._label_xy = ''.join(sorted([self._label_x, self._label_y]))
        self._label_xz = ''.join(sorted([self._label_x, self._label_z]))
        self._label_yz = ''.join(sorted([self._label_y, self._label_z]))
        self._label_xyd = self._label_xy[1] + self._label_xy[0]
        self._label_xzd = self._label_xz[1] + self._label_xz[0]
        self._label_yzd = self._label_yz[1] + self._label_yz[0]
        self._labels_std_one = {self._label_x: 'x', self._label_y: 'y', self._label_z: 'z'}
        self._labels_std_two = {self._label_xy: 'xy', self._label_xz: 'xz', self._label_yz: 'yz'}
        self._labels_std_two_down = {self._label_xyd: 'xy', self._label_xzd: 'xz', self._label_yzd: 'yz'}
        self._labels_std = self._labels_std_one.copy()
        self._labels_std.update(self._labels_std_two)
        self._labels_std.update(self._labels_std_two_down)
        # Declare variables to tranquilize PyCharm's syntax checker
        self._tau_x, self._tau_y, self._tau_z = 0, 0, 0
        self._tau_xy, self._tau_xz, self._tau_yz = 0, 0, 0
        # Initialize variables such as self.tau_a and self._tau_x
        for label, label_std in self._labels_std.items():
            # Ex: label = 'ab', label_std = 'xy'
            # Update variable such as self._tau_xy if provided.
            if 'tau_' + label in kwargs.keys():
                setattr(self, '_tau_' + label_std, kwargs.pop('tau_' + label))
            # Anyway, define variable such as tau_ab (0 if not provided).
            setattr(self, 'tau_' + label, getattr(self, '_tau_' + label_std))
        # Check that no unused argument remains
        if kwargs:
            raise ValueError('Unknown arguments: ', kwargs.keys())
        # Declare the computed variables
        self._phi_x, self._phi_y, self._phi_z = None, None, None
        self._phi_xy, self._phi_xz, self._phi_yz = None, None, None
        self.asymptotic = None
        # ------------------------------------------------
        # Magnitudes, offsets and (if possible) asymptotic
        # ------------------------------------------------
        self._compute(tau_x=self._tau_x, tau_y=self._tau_y, tau_z=self._tau_z,
                      tau_xy=self._tau_xy, tau_xz=self._tau_xz, tau_yz=self._tau_yz)
        self.mu = self.asymptotic.mu
        self.nu = self.asymptotic.nu
        self.xi = self.asymptotic.xi
        # -----------------------------------------------------
        # Create the variables like self.phi_ab, self.phi['ab']
        # -----------------------------------------------------
        self.phi = dict()
        for label, label_std in self._labels_std.items():
            # Ex: label = 'ab', label_std = 'xy'
            setattr(self, 'phi_' + label, getattr(self, '_phi_' + label_std))
            self.phi[label] = getattr(self, '_phi_' + label_std)

    def _compute(self, tau_x, tau_y, tau_z, tau_xy, tau_xz, tau_yz):
        """
        Compute the magnitude, offsets and (if possible) asymptotic.

        Should update:

            * ``self.asymptotic`` (with, at least, the magnitude).
            * ``self._phi_x``, `self._phi_y``, `self._phi_z``, `self._phi_xy``, `self._phi_xz``, `self._phi_yz``,
        """
        raise NotImplementedError

    def __repr__(self):
        s = 'asymptotic = %s' % self.asymptotic
        lab_sorted = sorted(self._labels_std_one.keys())
        lab_sorted.extend(sorted(self._labels_std_two.keys()))
        for label in lab_sorted:
            val = getattr(self, 'phi_' + label)
            if not isnan(val):
                s += ', phi_' + label + ' = {:.6g}'.format(float(val))
        return '<%s>' % s

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')
