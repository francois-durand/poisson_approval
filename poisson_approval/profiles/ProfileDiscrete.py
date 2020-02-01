import warnings
from poisson_approval.constants.constants import *
from math import isclose
from poisson_approval.utils.UtilCache import cached_property
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.profiles.ProfileCardinal import ProfileCardinal


class ProfileDiscrete(ProfileCardinal):
    """Profile with a discrete distribution of voters.

    Parameters
    ----------
    d : dict
        The first possible format is a dict of dict that, to a ranking (first key) and a utility (second key),
        associates the share of voters who have this ranking and this utility for their second candidate. The second
        possible format is a dict that, to a tuple (ranking, utility), associates the corresponding share of voters.
        The two formats can be mixed in the same profile declaration (cf. example below).
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.
    ratio_sincere : Number
        The ratio of sincere voters, in the interval [0, 1]. This is used for :meth:`tau`.
    ratio_fanatic : Number
        The ratio of fanatic voters, in the interval [0, 1]. This is used for :meth:`tau`. The sum of `ratio_sincere`
        and `ratio_fanatic` must not exceed 1.

    Attributes
    ----------
    d_ranking_utility_share : dict of dict
        To a ranking (first key) and a utility (second key), itassociates the share of voters who have this ranking and
        this utility for their second candidate.

    Notes
    -----
    If the input distribution is not normalized, the profile will be normalized anyway and a warning is
    issued (unless `normalization_warning` is False).

    Examples
    --------
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
        ...     ('bac', 0.1): Fraction(21, 100)
        ... })
        >>> profile
        ProfileDiscrete({'abc': {0.3: Fraction(13, 50), 0.8: Fraction(53, 100)}, 'bac': {0.1: Fraction(21, 100)}})
        >>> print(profile)
        <abc 0.3: 13/50, abc 0.8: 53/100, bac 0.1: 21/100> (Condorcet winner: a)
        >>> profile.d_ranking_share
        {'abc': Fraction(79, 100), 'bac': Fraction(21, 100)}
        >>> profile.abc
        Fraction(79, 100)
        >>> profile.have_ranking_with_utility_above_u('abc', 0.5)
        Fraction(53, 100)
        >>> profile.have_ranking_with_utility_below_u('abc', 0.5)
        Fraction(13, 50)
        >>> profile.have_ranking_with_utility_u('abc', 0.3)
        Fraction(13, 50)
    """

    def __init__(self, d, normalization_warning=True, ratio_sincere=0, ratio_fanatic=0):
        """
            >>> profile = ProfileDiscrete({42: 51})
            Traceback (most recent call last):
            TypeError: Key should be tuple or str, got: <class 'int'> instead.
        """
        super().__init__(ratio_sincere=ratio_sincere, ratio_fanatic=ratio_fanatic)
        self.d_ranking_utility_share = DictPrintingInOrderIgnoringZeros({
            ranking: DictPrintingInOrderIgnoringZeros() for ranking in RANKINGS})
        for key, value in d.items():
            if isinstance(key, tuple):
                ranking, utility = key
                share = value
                if share > 0:
                    self.d_ranking_utility_share[ranking][utility] = (
                        self.d_ranking_utility_share[ranking].get(utility, 0) + share)
            elif isinstance(key, str):
                ranking = key
                d_utility_share = value
                for utility, share in d_utility_share.items():
                    if share > 0:
                        self.d_ranking_utility_share[ranking][utility] = (
                            self.d_ranking_utility_share[ranking].get(utility, 0) + share)
            else:
                raise TypeError('Key should be tuple or str, got: %s instead.' % type(key))
        # Normalize if necessary
        total = sum([sum(d_utility_share.values()) for d_utility_share in self.d_ranking_utility_share.values()])
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: profile is not normalized, I will normalize it.")
            for d_utility_share in self.d_ranking_utility_share.values():
                for utility, share in d_utility_share.items():
                    d_utility_share[utility] = share / total

    @cached_property
    def d_ranking_share(self):
        return DictPrintingInOrderIgnoringZeros({
            ranking: sum(d_utility_share.values()) for ranking, d_utility_share in self.d_ranking_utility_share.items()
        })

    def have_ranking_with_utility_above_u(self, ranking, u):
        d_utility_share = self.d_ranking_utility_share[ranking]
        return sum([share for utility, share in d_utility_share.items() if utility > u])

    def have_ranking_with_utility_u(self, ranking, u):
        d_utility_share = self.d_ranking_utility_share[ranking]
        return sum([share for utility, share in d_utility_share.items() if utility == u])

    def have_ranking_with_utility_below_u(self, ranking, u):
        d_utility_share = self.d_ranking_utility_share[ranking]
        return sum([share for utility, share in d_utility_share.items() if utility < u])

    def __repr__(self):
        """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
        ...     ('bac', 0.1): Fraction(21, 100)
        ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10))
        >>> profile
        ProfileDiscrete({'abc': {0.3: Fraction(13, 50), 0.8: Fraction(53, 100)}, 'bac': {0.1: Fraction(21, 100)}}, \
ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5))
        """
        arguments = repr(self.d_ranking_utility_share)
        if self.ratio_sincere > 0:
            arguments += ', ratio_sincere=%r' % self.ratio_sincere
        if self.ratio_fanatic > 0:
            arguments += ', ratio_fanatic=%r' % self.ratio_fanatic
        return 'ProfileDiscrete(%s)' % arguments

    def __str__(self):
        """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
        ...     ('bac', 0.1): Fraction(21, 100)
        ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10))
        >>> print(profile)
        <abc 0.3: 13/50, abc 0.8: 53/100, bac 0.1: 21/100> (Condorcet winner: a) (ratio_sincere: 1/10) \
(ratio_fanatic: 1/5)
        """
        result = '<' + ', '.join([
            '%s %s: %s' % (ranking, utility, self.d_ranking_utility_share[ranking][utility])
            for ranking in sorted(self.d_ranking_utility_share.keys()) if self.d_ranking_utility_share[ranking]
            for utility in sorted(self.d_ranking_utility_share[ranking].keys())
        ]) + '>'
        if self.is_profile_condorcet:
            result += ' (Condorcet winner: %s)' % self.condorcet_winners
        if self.ratio_sincere > 0:
            result += ' (ratio_sincere: %s)' % self.ratio_sincere
        if self.ratio_fanatic > 0:
            result += ' (ratio_fanatic: %s)' % self.ratio_fanatic
        return result

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    def __eq__(self, other):
        """Equality test.

        Parameters
        ----------
        other : Object

        Returns
        -------
        bool
            True iff this profile is equal to `other`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> profile = ProfileDiscrete({
            ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
            ...     ('bac', 0.1): Fraction(21, 100)
            ... })
            >>> profile == ProfileDiscrete({
            ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
            ...     ('bac', 0.1): Fraction(21, 100)
            ... })
            True
        """
        return (isinstance(other, ProfileDiscrete)
                and all([self.d_ranking_utility_share[ranking] == other.d_ranking_utility_share[ranking]
                         for ranking in RANKINGS])
                and self.ratio_sincere == other.ratio_sincere
                and self.ratio_fanatic == other.ratio_fanatic)

    @cached_property
    def standardized_version(self):
        """ProfileDiscrete : Standardized version of the profile (makes it unique, up to permutations of the candidates).

        Examples
        --------
            >>> from fractions import Fraction
            >>> profile = ProfileDiscrete({
            ...     'abc': {0.3: Fraction(26, 100), 0.8: Fraction(53, 100)},
            ...     ('bac', 0.1): Fraction(21, 100)
            ... })
            >>> print(profile.standardized_version)
            <abc 0.3: 13/50, abc 0.8: 53/100, bac 0.1: 21/100> (Condorcet winner: a)
            >>> profile.is_standardized
            True
        """
        def translate(s, permute):
            return s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])

        best_d = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_test = {translate(ranking, perm): d_utility_share
                      for ranking, d_utility_share in self.d_ranking_utility_share.items()}
            signature_test = [[(utility, d_test[ranking][utility]) for utility in sorted(d_test[ranking].keys())]
                              for ranking in XYZ_RANKINGS]
            if signature_test > best_signature:
                best_signature = signature_test
                best_d = d_test
        return ProfileDiscrete({ranking: best_d[xyz_ranking] for ranking, xyz_ranking in zip(RANKINGS, XYZ_RANKINGS)},
                               ratio_sincere=self.ratio_sincere, ratio_fanatic=self.ratio_fanatic)
