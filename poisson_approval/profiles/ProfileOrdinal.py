import warnings
import numpy as np
from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.profiles.Profile import Profile
from poisson_approval.utils.UtilMasks import masks_area, masks_distribution, winners_distribution
from poisson_approval.strategies.StrategyOrdinal import StrategyOrdinal
from poisson_approval.tau_vector.TauVector import TauVector
from poisson_approval.containers.AnalyzedStrategies import AnalyzedStrategies
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.constants.EquilibriumStatus import EquilibriumStatus
from poisson_approval.utils.UtilCache import cached_property


# noinspection PyUnresolvedReferences
class ProfileOrdinal(Profile):
    """An ordinal profile of preference.

    Parameters
    ----------
    d_ranking_share : dict
        E.g. ``{'abc': 0.4, 'cab': 0.6}``. ``d_ranking_share['abc']`` is the probability that a voter prefers
        candidate ``a``, then candidate ``b``, then candidate ``c``.
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.
    well_informed_voters : bool.
        If True (default), it is the usual model. If False, voters "see" only the candidates' expected scores and
        believe that the scores follow independent Poisson distributions.

    Notes
    -----
    If the input distribution `d_ranking_share` is not normalized, the profile will be normalized anyway and a
    warning is issued (unless `normalization_warning` is False).

    Examples
    --------
        >>> from fractions import Fraction
        >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
        >>> r
        ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)})
        >>> print(r)
        <abc: 1/10, bac: 3/5, cab: 3/10> (Condorcet winner: b)
        >>> r.abc
        Fraction(1, 10)
        >>> r.d_ranking_share['abc']  # Alternate syntax for r.abc
        Fraction(1, 10)
        >>> r.weighted_maj_graph
        array([[0, Fraction(-1, 5), Fraction(2, 5)],
               [Fraction(1, 5), 0, Fraction(2, 5)],
               [Fraction(-2, 5), Fraction(-2, 5), 0]], dtype=object)
        >>> r.condorcet_winners
        Winners({'b'})
        >>> r.is_profile_condorcet
        1.0
        >>> r.has_majority_favorite  # Is one candidate 'top' in a majority of ballots?
        True
        >>> r.has_majority_ranking  # Does one ranking represent a majority of ballots?
        True
        >>> r.is_single_peaked  # Is the profile single-peaked?
        True
        >>> r.support_in_rankings
        {'abc', 'bac', 'cab'}
        >>> r.is_generic_in_rankings  # Are all rankings there?
        False
    """

    def __init__(self, d_ranking_share, normalization_warning=True, well_informed_voters=True):
        super().__init__()
        # Populate the dictionary and check for typos in the input
        self._d_ranking_share = DictPrintingInOrderIgnoringZeros()
        for ranking, share in d_ranking_share.items():
            if ranking in RANKINGS:
                self._d_ranking_share[ranking] = share
            else:
                raise ValueError('Unknown key: ' + ranking)
        for ranking in RANKINGS:
            if ranking not in self._d_ranking_share:
                self._d_ranking_share[ranking] = 0
        # Normalize if necessary
        total = sum(self._d_ranking_share.values())
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: profile is not normalized, I will normalize it.")
            for ranking in self._d_ranking_share.keys():
                self._d_ranking_share[ranking] = self._d_ranking_share[ranking] / total
        # Well-informed voters?
        self.well_informed_voters = well_informed_voters

    @cached_property
    def d_ranking_share(self):
        return self._d_ranking_share

    def __repr__(self):
        return 'ProfileOrdinal(%r)' % self._d_ranking_share

    def __str__(self):
        result = '<%s>' % str(self._d_ranking_share)[1:-1]
        if self.is_profile_condorcet:
            result += ' (Condorcet winner: %s)' % self.condorcet_winners
        return result

    def _repr_pretty_(self, p, cycle):
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
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r == ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            True
        """
        return isinstance(other, ProfileOrdinal) and self.d_ranking_share == other.d_ranking_share

    @cached_property
    def standardized_version(self):
        """ProfileOrdinal : Standardized version of the profile (makes it unique, up to permutations of the candidates).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.standardized_version
            ProfileOrdinal({'abc': Fraction(3, 5), 'bac': Fraction(1, 10), 'cba': Fraction(3, 10)})
            >>> r.is_standardized
            False
        """
        def translate(s, permute):
            return s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])

        best_d = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_test = {translate(ranking, perm): share for ranking, share in self.d_ranking_share.items()}
            signature_test = [d_test[ranking] for ranking in XYZ_RANKINGS]
            if signature_test > best_signature:
                best_signature = signature_test
                best_d = d_test
        return ProfileOrdinal({ranking: best_d[xyz_ranking] for ranking, xyz_ranking in zip(RANKINGS, XYZ_RANKINGS)})

    # Has full support
    @cached_property
    def support(self):
        """:class:`SetPrintingInOrder` of str : Alternate notation for :meth:`support_in_rankings`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.support
            {'abc', 'bac', 'cab'}
        """
        return self.support_in_rankings

    @cached_property
    def is_generic(self):
        """bool : Alternate notation for :meth:`is_generic_in_rankings`

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.is_generic
            False
        """
        return self.is_generic_in_rankings

    # Tau and strategy-related stuff

    def tau(self, sigma):
        """Tau-vector associated to a strategy.

        Parameters
        ----------
        sigma : StrategyOrdinal

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `sigma`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> sigma = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
            >>> tau = r.tau(sigma)
            >>> print(tau)
            <a: 1/10, ab: 3/5, c: 3/10> ==> a
            >>> tau = r.τ(sigma)  # Alternate notation
            >>> print(tau)
            <a: 1/10, ab: 3/5, c: 3/10> ==> a
        """
        t = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for ranking, ballot in sigma.d_ranking_ballot.items():
            if self.d_ranking_share[ranking] > 0:
                t[ballot] += self.d_ranking_share[ranking]
        if self.well_informed_voters:
            return TauVector(t)
        else:
            return TauVector(
                {'a': t['a'] + t['ab'] + t['ac'], 'b': t['b'] + t['ab'] + t['bc'], 'c': t['c'] + t['ac'] + t['bc']},
                normalization_warning=False)

    def is_equilibrium(self, sigma):
        """Whether a strategy is an equilibrium.

        Parameters
        ----------
        sigma : StrategyOrdinal

        Returns
        -------
        EquilibriumStatus
            Whether `sigma` is an equilibrium in this profile.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> sigma = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
            >>> r.is_equilibrium(sigma)
            EquilibriumStatus.EQUILIBRIUM
        """
        d_ranking_best_response = self.tau(sigma).d_ranking_best_response
        status = EquilibriumStatus.EQUILIBRIUM
        for ranking, share in self.d_ranking_share.items():
            if share == 0:
                continue
            best_response = d_ranking_best_response[ranking]
            if sigma.d_ranking_ballot[ranking] == '':
                status = min(status, EquilibriumStatus.INCONCLUSIVE)
            elif best_response.ballot == INCONCLUSIVE:
                status = min(status, EquilibriumStatus.INCONCLUSIVE)
            elif best_response.ballot == UTILITY_DEPENDENT:
                status = min(status, EquilibriumStatus.UTILITY_DEPENDENT)
            elif sigma.d_ranking_ballot[ranking] != best_response.ballot:
                return EquilibriumStatus.NOT_EQUILIBRIUM
        return status

    @cached_property
    def analyzed_strategies(self):
        """AnalyzedStrategies : Analyzed strategies of the profile.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.analyzed_strategies
            Equilibria:
            <abc: a, bac: b, cab: ac> ==> b (FF)
            <abc: a, bac: ab, cab: c> ==> a (D)
            <BLANKLINE>
            Utility-dependent equilibrium:
            <abc: ab, bac: b, cab: c> ==> b (FF)
            <BLANKLINE>
            Non-equilibria:
            <abc: a, bac: b, cab: c> ==> b (FF)
            <abc: a, bac: ab, cab: ac> ==> a (D)
            <abc: ab, bac: b, cab: ac> ==> b (FF)
            <abc: ab, bac: ab, cab: c> ==> a, b (FF)
            <abc: ab, bac: ab, cab: ac> ==> a (D)
            >>> print(r.analyzed_strategies.equilibria[0])
            <abc: a, bac: b, cab: ac> ==> b
        """
        equilibria = []
        utility_dependent = []
        inconclusive = []
        non_equilibria = []
        strat_abc = ['a', 'ab'] if self.abc > 0 else ['']
        strat_acb = ['a', 'ac'] if self.acb > 0 else ['']
        strat_bac = ['b', 'ab'] if self.bac > 0 else ['']
        strat_bca = ['b', 'bc'] if self.bca > 0 else ['']
        strat_cab = ['c', 'ac'] if self.cab > 0 else ['']
        strat_cba = ['c', 'bc'] if self.cba > 0 else ['']
        for s_abc in strat_abc:
            for s_acb in strat_acb:
                for s_bac in strat_bac:
                    for s_bca in strat_bca:
                        for s_cab in strat_cab:
                            for s_cba in strat_cba:
                                sigma = StrategyOrdinal({'abc': s_abc, 'acb': s_acb, 'bac': s_bac,
                                                         'bca': s_bca, 'cab': s_cab, 'cba': s_cba}, profile=self)
                                status = sigma.is_equilibrium
                                if status == EquilibriumStatus.EQUILIBRIUM:
                                    equilibria.append(sigma)
                                elif status == EquilibriumStatus.UTILITY_DEPENDENT:
                                    utility_dependent.append(sigma)
                                elif status == EquilibriumStatus.INCONCLUSIVE:
                                    inconclusive.append(sigma)
                                    warnings.warn('Met an inconclusive case: \nr = %r\nsigma = %r' % (self, sigma))
                                else:
                                    non_equilibria.append(sigma)
        return AnalyzedStrategies(equilibria, utility_dependent, inconclusive, non_equilibria)

    def proba_equilibrium(self, test=None):
        """Probability that an equilibrium exists (depending on the utilities).

        Parameters
        ----------
        test : callable
            A function ``StrategyOrdinal -> bool`` that gives a condition on the strategy. Default: always True.

        Returns
        -------
        float
            The probability that an equilibrium strategy exists, that meets the `test` condition.

        Notes
        -----
        The result is exact (not based on a Monte-Carlo estimation).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.proba_equilibrium()
            1
        """
        if test is None:
            # noinspection PyUnusedLocal
            def test(sigma):
                return True
        if any([test(sigma) for sigma in self.analyzed_strategies.equilibria]):
            return 1
        support = sorted(self.support)
        dim = len(support)
        masks = [
            [(sigma.d_ranking_best_response[ranking].threshold_utility, len(sigma.d_ranking_ballot[ranking]) == 2)
             for ranking in support]
            for sigma in self.analyzed_strategies.utility_dependent if test(sigma)
        ]
        return masks_area(inf=[0] * dim, sup=[1] * dim, masks=masks)

    def distribution_equilibria(self, test=None):
        """Distribution of numbers of equilibria (depending on the utilities).

        Parameters
        ----------
        test : callable
            A function ``StrategyOrdinal -> bool`` that gives a condition on the strategy. Default: always True.

        Returns
        -------
        list
            A list that represents an histogram. The distribution of number of equilibria (meeting the `test` condition).

        Notes
        -----
        The result is exact (not based on a Monte-Carlo estimation).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.distribution_equilibria()
            array([0.        , 0.        , 0.86290531, 0.13709469])
        """
        if test is None:
            # noinspection PyUnusedLocal
            def test(sigma):
                return True
        cover_alls = np.sum([test(sigma) for sigma in self.analyzed_strategies.equilibria], dtype=int)
        support = sorted(self.support)
        dim = len(support)
        masks = [
            [(sigma.d_ranking_best_response[ranking].threshold_utility, len(sigma.d_ranking_ballot[ranking]) == 2)
             for ranking in support]
            for sigma in self.analyzed_strategies.utility_dependent if test(sigma)
        ]
        return masks_distribution(inf=np.zeros(dim), sup=np.ones(dim), masks=masks, cover_alls=cover_alls)

    def distribution_winners(self, test=None):
        """Distribution of the number of equilibrium winners (depending on the utilities).

        Parameters
        ----------
        test : callable
            A function ``StrategyOrdinal -> bool`` that gives a condition on the strategy. Default: always True.

        Returns
        -------
        list
            A list that represents an histogram. The distribution of number of possible equilibrium winner (with
            strategies that meet the `test` condition).

        Notes
        -----
        The result is exact (not based on a Monte-Carlo estimation).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)})
            >>> r.distribution_winners()
            array([0., 0., 1., 0.])
        """
        if test is None:
            # noinspection PyUnusedLocal
            def test(sigma):
                return True
        cover_alls = set.union(*([set()] + [
            sigma.winners for sigma in self.analyzed_strategies.equilibria
            if test(sigma)
        ]))
        support = sorted(self.support)
        dim = len(support)
        masks_winners = [
            (
                [(sigma.d_ranking_best_response[ranking].threshold_utility, len(sigma.d_ranking_ballot[ranking]) == 2)
                 for ranking in support],
                sigma.winners
            )
            for sigma in self.analyzed_strategies.utility_dependent if test(sigma)
        ]
        return winners_distribution(inf=np.zeros(dim), sup=np.ones(dim), masks_winners=masks_winners,
                                    cover_alls=cover_alls)
