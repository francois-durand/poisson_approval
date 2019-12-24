import numpy as np
from poisson_approval.constants.constants import *
from poisson_approval.utils.SetPrintingInOrder import SetPrintingInOrder
from poisson_approval.containers.Winners import Winners
from poisson_approval.utils.UtilCache import cached_property


# noinspection PyUnresolvedReferences
class Profile():
    """A profile of preference (abstract class)."""

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    @cached_property
    def d_ranking_share(self):
        """dict : Shares of rankings.
            E.g. ``'abc': 0.3`` means that a ratio 0.3 of the voters have ranking ``'abc'``.
        """
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    @cached_property
    def standardized_version(self):
        """Profile : Standardized version of the profile (makes it unique, up to permutations of the candidates)."""
        raise NotImplementedError

    @cached_property
    def is_standardized(self):
        """bool : Whether the profile is standardized. Cf. :meth:`standardized_version`."""
        return self == self.standardized_version

    # Condorcet stuff

    @cached_property
    def weighted_maj_graph(self):
        """np.ndarray : Weighted majority graph."""
        ab = self.abc + self.acb + self.cab - self.bac - self.bca - self.cba
        ac = self.abc + self.acb + self.bac - self.bca - self.cab - self.cba
        bc = self.abc + self.bac + self.bca - self.acb - self.cab - self.cba
        return np.array([[0, ab, ac], [-ab, 0, bc], [-ac, -bc, 0]])

    @cached_property
    def condorcet_winners(self):
        """Winners : Condorcet winner(s)."""
        m = self.weighted_maj_graph
        min_score = {'a': min(m[0, 1], m[0, 2]), 'b': min(m[1, 0], m[1, 2]), 'c': min(m[2, 0], m[2, 1])}
        return Winners({candidate for candidate in ['a', 'b', 'c'] if min_score[candidate] > - 10**(-8)})

    @cached_property
    def is_profile_condorcet(self):
        """float : Whether the profile is Condorcet. 1. means there is a strict Condorcet winner, 0.5 means there are
        one or more weak Condorcet winner(s), 0. means there is no Condorcet winner.
        """
        m = self.weighted_maj_graph
        min_score = [min(m[0, 1], m[0, 2]), min(m[1, 0], m[1, 2]), min(m[2, 0], m[2, 1])]
        maximin = max(min_score)
        if maximin > 10**(-8):
            return 1.
        elif maximin > - 10**(-8):
            return .5
        else:
            return 0.

    @cached_property
    def has_majority_favorite(self):
        """bool : Whether there is a `majority favorite` (a candidate ranked first by strictly more than half of the
        voters).
        """
        return self.abc + self.acb > 0.5 or self.bac + self.bca > 0.5 or self.cab + self.cba > 0.5

    @cached_property
    def has_majority_ranking(self):
        """bool : Whether there is a majority ranking (a ranking shared by strictly more than half of the voters)."""
        return max(self.d_ranking_share.values()) > 0.5

    # Single-peakedness
    @cached_property
    def is_single_peaked(self):
        """bool : Whether the profile is single-peaked."""
        return ((self.abc == 0 and self.bac == 0)
                or (self.acb == 0 and self.cab == 0)
                or (self.bca == 0 and self.cba == 0))

    # Has full support
    @cached_property
    def support_in_rankings(self):
        """:class:`SetPrintingInOrder` of str : Support of the profile (in terms of rankings)."""
        return SetPrintingInOrder({key for key, val in self.d_ranking_share.items() if val > 0})

    @cached_property
    def is_generic_in_rankings(self):
        """bool : Whether the profile is generic in rankings (contains all rankings)."""
        return 0 not in self.d_ranking_share.values()

    # Tau and strategy-related stuff

    def tau(self, sigma):
        """Tau-vector associated to this profile and a given strategy.

        Parameters
        ----------
        sigma : Strategy

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `sigma`.
        """
        raise NotImplementedError

    # noinspection NonAsciiCharacters
    def τ(self, sigma):
        """Tau-vector (alternate notation).

        Parameters
        ----------
        sigma : Strategy

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `sigma`.
        """
        return self.tau(sigma)

    def is_equilibrium(self, sigma):
        """Whether a strategy is an equilibrium in this profile.

        Parameters
        ----------
        sigma : Strategy

        Returns
        -------
        EquilibriumStatus
            Whether `sigma` is an equilibrium in this profile.
        """
        raise NotImplementedError


def make_property_ranking_share(ranking, doc):
    def _f(self):
        return self.d_ranking_share[ranking]
    _f.__doc__ = doc
    return property(_f)


for my_ranking in RANKINGS:
    setattr(Profile, my_ranking, make_property_ranking_share(my_ranking, 'Number : Share of voters with this ranking.'))
