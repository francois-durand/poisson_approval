import warnings
from math import isclose
from functools import partial
from fractions import Fraction
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import sort_ballot
from poisson_approval.containers.Scores import Scores
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.best_response.BestResponse import BestResponse
from poisson_approval.utils.UtilCache import cached_property
from poisson_approval.events.EventDuo import EventDuo
from poisson_approval.events.EventPivotStrict import EventPivotStrict
from poisson_approval.events.EventPivotTij import EventPivotTij
from poisson_approval.events.EventPivotTjk import EventPivotTjk
from poisson_approval.events.EventPivotWeak import EventPivotWeak
from poisson_approval.events.EventTrio import EventTrio
from poisson_approval.events.EventTrio1t import EventTrio1t
from poisson_approval.events.EventTrio2t import EventTrio2t
from poisson_approval.constants.Focus import Focus


# noinspection PyUnresolvedReferences
class TauVector:
    """A vector 'tau' (ballot distribution)

    Parameters
    ----------
    d_ballot_share : dict
        Ballot distribution, e.g. ``{'a': 0.1, 'ab': 0.6, 'c':0.3}``.
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.

    Notes
    -----
    If the input distribution `d_ballot_share` is not normalized, the tau vector will be normalized anyway and a
    warning is issued (unless `normalization_warning` is False).

    Examples
    --------
        >>> from fractions import Fraction
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
        >>> tau
        TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
        >>> print(tau)
        <a: 1/10, ab: 3/5, c: 3/10> ==> a
        >>> tau.a
        Fraction(1, 10)
        >>> tau.b
        0
        >>> tau.c
        Fraction(3, 10)
        >>> tau.ab
        Fraction(3, 5)
        >>> tau.ba  # Alternate notation for tau.ab
        Fraction(3, 5)
        >>> tau.ac
        0
        >>> tau.ca  # Alternate notation for tau.ac, etc.
        0
        >>> tau.bc
        0
        >>> tau.cb
        0
        >>> tau.duo_ab
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.duo_ba
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.duo_ac
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.duo_ca
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.duo_bc
        <asymptotic = exp(- 0.0514719 n - 0.5 log n - 0.836813 + o(1)), phi_a = 1, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.duo_cb
        <asymptotic = exp(- 0.0514719 n - 0.5 log n - 0.836813 + o(1)), phi_a = 1, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.pivot_weak_ab
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_weak_ba
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_weak_ac
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_weak_ca
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_weak_bc
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        >>> tau.pivot_weak_cb
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = \
0.707107>
        >>> tau.pivot_strict_ab
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_strict_ba
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_strict_ac
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_strict_ca
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_strict_bc
        <asymptotic = exp(- inf)>
        >>> tau.pivot_strict_cb
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tij_abc
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tij_acb
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.371758 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_tij_bac
        <asymptotic = exp(- 0.1 n + log n - 2.30259 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tij_bca
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.302013 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        >>> tau.pivot_tij_cab
        <asymptotic = exp(- 0.0834849 n - 0.5 log n + 0.0518905 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_tij_cba
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        >>> tau.pivot_tjk_abc
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tjk_acb
        <asymptotic = exp(- inf)>
        >>> tau.pivot_tjk_bac
        <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.371758 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_tjk_bca
        <asymptotic = exp(- 0.0834849 n - 0.5 log n + 0.0518905 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
        >>> tau.pivot_tjk_cab
        <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.pivot_tjk_cba
        <asymptotic = exp(- 0.1 n + log n - 2.30259 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
        >>> tau.trio
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        >>> tau.trio_1t_a
        <asymptotic = exp(- inf)>
        >>> tau.trio_1t_b
        <asymptotic = exp(- 0.151472 n + 0.5 log n - 3.48597 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.trio_1t_c
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.490239 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        >>> tau.trio_2t_ab
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 1.18339 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.trio_2t_ac
        <asymptotic = exp(- inf)>
        >>> tau.trio_2t_bc
        <asymptotic = exp(- 0.151472 n + 0.5 log n - 3.1394 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.trio_2t_ba
        <asymptotic = exp(- 0.151472 n - 0.5 log n - 1.18339 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
        >>> tau.trio_2t_ca
        <asymptotic = exp(- inf)>
        >>> tau.trio_2t_cb
        <asymptotic = exp(- 0.151472 n + 0.5 log n - 3.1394 + o(1)), phi_a = 0, phi_c = 1.41421, phi_ab = 0.707107>
    """

    def __init__(self, d_ballot_share: dict = None, normalization_warning: bool = True):
        # Populate the dictionary and check for typos in the input
        self.d_ballot_share = DictPrintingInOrderIgnoringZeros()
        for ballot, share in d_ballot_share.items():
            if ballot in BALLOTS_WITH_INVERSIONS:
                sorted_key = ''.join(sorted(ballot))
                self.d_ballot_share[sorted_key] = share
            else:
                raise ValueError('Unknown key: ' + ballot)
        for ballot in BALLOTS_WITHOUT_INVERSIONS:
            if ballot not in self.d_ballot_share:
                self.d_ballot_share[ballot] = 0
        # Normalize if necessary
        total = sum(self.d_ballot_share.values())
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: tau is not normalized, I will normalize it.")
            for ballot in self.d_ballot_share.keys():
                self.d_ballot_share[ballot] = self.d_ballot_share[ballot] / total

    def __repr__(self):
        return 'TauVector(%r)' % self.d_ballot_share

    def __str__(self):
        return '<%s>' % str(self.d_ballot_share)[1:-1] + ' ==> ' + str(self.winners)

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    @cached_property
    def scores(self):
        """Scores : The scores.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.scores
            {'a': Fraction(7, 10), 'b': Fraction(3, 5), 'c': Fraction(3, 10)}
        """
        return Scores(dict(a=self.a + self.ab + self.ac,
                           b=self.b + self.ab + self.bc,
                           c=self.c + self.ac + self.bc))

    @property
    def winners(self):
        """Winners : The winners.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.winners
            Winners({'a'})
        """
        return self.scores.winners

    def __eq__(self, other):
        """Equality test.

        Parameters
        ----------
        other : Object

        Returns
        -------
        bool
            True iff it is the same tau-vector.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau == TauVector({'a': Fraction(10, 100), 'ab': Fraction(60, 100), 'c': Fraction(30, 100)})
            True
        """
        return isinstance(other, TauVector) and self.d_ballot_share == other.d_ballot_share

    @cached_property
    def standardized_version(self):
        """Standardized version of the profile (makes it unique, up to permutations).

        Notes
        -----
        It returns the same profile, up to a permutation of the candidates. how the permutation is chosen in
        practice does not really matter: the important point is that the `standardized version` is the same for all the
        profile that are identical up to a permutation of the candidates.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.standardized_version
            TauVector({'a': Fraction(3, 10), 'b': Fraction(1, 10), 'bc': Fraction(3, 5)})
        """
        def translate(s, permute):
            return ''.join(sorted(s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])))

        best_d = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_test = {translate(ballot, perm): share for ballot, share in self.d_ballot_share.items()}
            signature_test = [d_test[ballot] for ballot in XYZ_BALLOTS_WITHOUT_INVERSION]
            if signature_test > best_signature:
                best_signature = signature_test
                best_d = d_test
        return TauVector({ballot: best_d[xyz_ballot]
                          for ballot, xyz_ballot in zip(BALLOTS_WITHOUT_INVERSIONS, XYZ_BALLOTS_WITHOUT_INVERSION)})

    @cached_property
    def is_standardized(self):
        """Whether the profile is standardized or not. Cf. :meth:`standardized_version`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.is_standardized
            False
        """
        return self == self.standardized_version

    # Pivots

    @cached_property
    def trio(self):
        """Event: trio."""
        return EventTrio(candidate_x='a', candidate_y='b', candidate_z='c',
                         tau_a=self.a, tau_b=self.b, tau_c=self.c, tau_ab=self.ab, tau_ac=self.ac, tau_bc=self.bc)

    @property
    def focus(self):
        """Focus : Focus of this tau-vector.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.focus
            Focus.DIRECT
        """
        magnitudes = sorted([self.pivot_weak_ab.mu, self.pivot_weak_ac.mu, self.pivot_weak_bc.mu])
        if isclose(magnitudes[0], magnitudes[2]):
            return Focus.UNFOCUSED
        elif isclose(magnitudes[0], magnitudes[1]):
            return Focus.FORWARD_FOCUSED
        elif isclose(magnitudes[1], magnitudes[2]):
            return Focus.BACKWARD_FOCUSED
        else:
            return Focus.DIRECT

    def print_weak_pivots(self):
        """Print the weak pivots (including the 3-way tie).

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.print_weak_pivots()
            pivot_weak_ab:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_weak_ac:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_weak_bc:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            trio:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
        """
        for pair in PAIRS_WITHOUT_INVERSIONS:
            print('pivot_weak_%s: ' % pair, getattr(self, 'pivot_weak_%s' % pair))
        print('trio: ', self.trio)

    def print_all_pivots(self):
        """Print all the pivots.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.print_all_pivots()
            pivot_weak_ab:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_weak_ac:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_weak_bc:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            pivot_strict_ab:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_strict_ac:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_strict_bc:  <asymptotic = exp(- inf)>
            pivot_tij_abc:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_tij_acb:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.371758 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_tij_bac:  <asymptotic = exp(- 0.1 n + log n - 2.30259 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_tij_bca:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.302013 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            pivot_tij_cab:  <asymptotic = exp(- 0.0834849 n - 0.5 log n + 0.0518905 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_tij_cba:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            pivot_tjk_abc:  <asymptotic = exp(- inf)>
            pivot_tjk_acb:  <asymptotic = exp(- inf)>
            pivot_tjk_bac:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.371758 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_tjk_bca:  <asymptotic = exp(- 0.0834849 n - 0.5 log n + 0.0518905 + o(1)), phi_a = 0.654654, \
phi_c = 1.52753, phi_ab = 0.654654>
            pivot_tjk_cab:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            pivot_tjk_cba:  <asymptotic = exp(- 0.1 n + log n - 2.30259 + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            trio:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            trio_1t_a:  <asymptotic = exp(- inf)>
            trio_1t_b:  <asymptotic = exp(- 0.151472 n + 0.5 log n - 3.48597 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            trio_1t_c:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 0.490239 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            trio_2t_ab:  <asymptotic = exp(- 0.151472 n - 0.5 log n - 1.18339 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            trio_2t_ac:  <asymptotic = exp(- inf)>
            trio_2t_bc:  <asymptotic = exp(- 0.151472 n + 0.5 log n - 3.1394 + o(1)), phi_a = 0, phi_c = 1.41421, \
phi_ab = 0.707107>
            duo_ab:  <asymptotic = exp(- 0.1 n + o(1)), phi_a = 0, phi_c = 1, phi_ab = 1>
            duo_ac:  <asymptotic = exp(- 0.0834849 n - 0.5 log n - 0.87535 + o(1)), phi_a = 0.654654, phi_c = 1.52753, \
phi_ab = 0.654654>
            duo_bc:  <asymptotic = exp(- 0.0514719 n - 0.5 log n - 0.836813 + o(1)), phi_a = 1, phi_c = 1.41421, \
phi_ab = 0.707107>
        """
        for pair in PAIRS_WITHOUT_INVERSIONS:
            print('pivot_weak_%s: ' % pair, getattr(self, 'pivot_weak_%s' % pair))
        for pair in PAIRS_WITHOUT_INVERSIONS:
            print('pivot_strict_%s: ' % pair, getattr(self, 'pivot_strict_%s' % pair))
        for ranking in RANKINGS:
            print('pivot_tij_%s: ' % ranking, getattr(self, 'pivot_tij_%s' % ranking))
        for ranking in RANKINGS:
            print('pivot_tjk_%s: ' % ranking, getattr(self, 'pivot_tjk_%s' % ranking))
        print('trio: ', self.trio)
        for candidate in CANDIDATES:
            print('trio_1t_%s: ' % candidate, getattr(self, 'trio_1t_%s' % candidate))
        for pair in PAIRS_WITHOUT_INVERSIONS:
            print('trio_2t_%s: ' % pair, getattr(self, 'trio_2t_%s' % pair))
        for pair in PAIRS_WITHOUT_INVERSIONS:
            print('duo_%s: ' % pair, getattr(self, 'duo_%s' % pair))

    @cached_property
    def d_ranking_best_response(self):
        """dict : Best response profile.

        * Key: a ranking (e.g. ``'abc'``).
        * Value: a :class:`BestResponse`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
            >>> tau.d_ranking_best_response['abc']
            <ballot = a, threshold_utility = 1, justification = Asymptotic method, pivot_tij = exp(- 0.1 n + o(1)), \
pivot_tjk = exp(- inf), trio_1t = exp(- inf), trio_2t = exp(- 0.151472 n - 0.5 log n - 1.18339 + o(1)), \
trio = exp(- 0.151472 n - 0.5 log n - 0.836813 + o(1))>
        """
        _d_ranking_best_response = dict()
        for ranking in RANKINGS:
            _d_ranking_best_response[ranking] = BestResponse(
                ranking,
                pivot_tij=getattr(self, 'pivot_tij_' + ranking),
                pivot_tjk=getattr(self, 'pivot_tjk_' + ranking),
                trio_1t=getattr(self, 'trio_1t_' + ranking[0]),
                trio_2t=getattr(self, 'trio_2t_' + ranking[0] + ranking[1]),
                trio=self.trio,
            )
        return _d_ranking_best_response


def _f_ballot_share(self, ballot):
    """Share of this ballot"""
    # This function is used to define an attribute for each ballot.
    return self.d_ballot_share[sort_ballot(ballot)]


for my_ballot in BALLOTS_WITH_INVERSIONS:
    setattr(TauVector, my_ballot, property(partial(_f_ballot_share, ballot=my_ballot)))
    if sort_ballot(my_ballot) == my_ballot:
        getattr(TauVector, my_ballot).__doc__ = "Number: Share of the ballot ``'%s'``." % my_ballot
    else:
        getattr(TauVector, my_ballot).__doc__ = \
            "Number: Share of the ballot ``'%s'`` (alternate notation)." % sort_ballot(my_ballot)

# Events based on a duo: create cached properties like duo_ab, etc.


def _f_duo(self, candidate_x, candidate_y, candidate_z, cls, stub):
    if candidate_x < candidate_y:
        return cls(candidate_x=candidate_x, candidate_y=candidate_y, candidate_z=candidate_z,
                   tau_a=self.a, tau_b=self.b, tau_c=self.c, tau_ab=self.ab, tau_ac=self.ac, tau_bc=self.bc)
    else:
        return getattr(self, stub + '_%s%s' % (candidate_y, candidate_x))


for event_class, event_stub, event_doc in [
        (EventDuo, 'duo', 'EventDuo : These two candidates have the same score.'),
        (EventPivotWeak, 'pivot_weak',
            'EventPivotWeak : These two candidates have the same score, at least as high as the other.'),
        (EventPivotStrict, 'pivot_strict',
            'EventPivotStrict : These two candidates have the same score, strictly higher than the other.'),
        (EventTrio2t, 'trio_2t',
            'EventTrio1t : These candidates have one vote less than the other.')]:
    for x, y, z in RANKINGS:
        name = event_stub + '_%s%s' % (x, y)
        setattr(TauVector, name, partial(_f_duo, candidate_x=x, candidate_y=y, candidate_z=z,
                                         cls=event_class, stub=event_stub))
        getattr(TauVector, name).__name__ = name
        setattr(TauVector, name, cached_property(getattr(TauVector, name)))
        getattr(TauVector, name).__doc__ = event_doc


# Events based on a permutation: create cached properties like pivot_tij_abc, etc.


def _f_ranking(self, candidate_x, candidate_y, candidate_z, cls):
    return cls(candidate_x=candidate_x, candidate_y=candidate_y, candidate_z=candidate_z,
               tau_a=self.a, tau_b=self.b, tau_c=self.c, tau_ab=self.ab, tau_ac=self.ac, tau_bc=self.bc)


for event_class, event_stub, event_doc in [
        (EventPivotTij, 'pivot_tij',
            'EventPivotTij: Personalized pivot of type Tij (between the two most-liked candidates).'),
        (EventPivotTjk, 'pivot_tjk',
            'EventPivotTjk: Personalized pivot of type Tjk (between the two least-liked candidates).')]:
    for x, y, z in RANKINGS:
        name = event_stub + '_%s%s%s' % (x, y, z)
        if event_stub == 'pivot_tjk':
            setattr(TauVector, name, partial(_f_ranking, candidate_x=z, candidate_y=y, candidate_z=x, cls=event_class))
        else:
            setattr(TauVector, name, partial(_f_ranking, candidate_x=x, candidate_y=y, candidate_z=z, cls=event_class))
        getattr(TauVector, name).__name__ = name
        setattr(TauVector, name, cached_property(getattr(TauVector, name)))
        getattr(TauVector, name).__doc__ = event_doc


# Events based on one candidate: create cached properties like trio_1t_a, etc.


for event_class, event_stub, event_doc in [
        (EventTrio1t, 'trio_1t', 'EventTrio1t : This candidate has one vote less than the two others.')]:
    for x, y, z in RANKINGS:
        if y > z:
            continue
        name = event_stub + '_%s' % x
        setattr(TauVector, name, partial(_f_ranking, candidate_x=x, candidate_y=y, candidate_z=z, cls=event_class))
        getattr(TauVector, name).__name__ = name
        setattr(TauVector, name, cached_property(getattr(TauVector, name)))
        getattr(TauVector, name).__doc__ = event_doc
