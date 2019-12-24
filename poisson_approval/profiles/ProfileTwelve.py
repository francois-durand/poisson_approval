import warnings
from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import ballot_one, ballot_one_two
from poisson_approval.utils.SetPrintingInOrder import SetPrintingInOrder
from poisson_approval.profiles.ProfileCardinal import ProfileCardinal
from poisson_approval.tau_vector.TauVector import TauVector
from poisson_approval.strategies.StrategyTwelve import StrategyTwelve
from poisson_approval.containers.AnalyzedStrategies import AnalyzedStrategies
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.constants.EquilibriumStatus import EquilibriumStatus
from poisson_approval.utils.UtilCache import cached_property


# noinspection PyUnresolvedReferences
class ProfileTwelve(ProfileCardinal):
    """A profile of preference with twelve types.

    Parameters
    ----------
    d_type_share : dict
        E.g. ``{'ab_c': 0.4, 'c_ab': 0.6}``. ``d_type_share['ab_c']`` is the probability
        that a voter prefers candidate ``a``, then candidate ``b``, then candidate ``c``, with a utility for ``b``
        that is infinitely close to 1. In contrast, ``d_type_share['a_bc']`` is the probability that a voter prefers
        ``a`` then ``b`` then ``c``, with a utility for ``b`` that is infinitely close to 0.
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.

    Notes
    -----
    If the input distribution `d_type_share` is not normalized, the profile will be normalized anyway and a
    warning is issued (unless `normalization_warning` is False).

    Examples
    --------
        >>> from fractions import Fraction
        >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
        >>> r
        ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(3, 5), 'c_ab': Fraction(1, 5), \
'ca_b': Fraction(1, 10)})
        >>> print(r)
        <ab_c: 1/10, b_ac: 3/5, c_ab: 1/5, ca_b: 1/10> (Condorcet winner: b)
        >>> r.c_ab
        Fraction(1, 5)
        >>> r.d_type_share['c_ab']  # Alternate syntax for r.c_ab
        Fraction(1, 5)
        >>> r.cab
        Fraction(3, 10)
        >>> r.d_ranking_share['cab']  # Alternate syntax for r.cab
        Fraction(3, 10)
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

    def __init__(self, d_type_share, normalization_warning=True):
        super().__init__()
        # Populate the dictionary and check for typos in the input
        self.d_type_share = DictPrintingInOrderIgnoringZeros()
        for t, share in d_type_share.items():
            if t in TWELVE_TYPES:
                self.d_type_share[t] = share
            else:
                raise ValueError('Unknown key: ' + t)
        for t in TWELVE_TYPES:
            if t not in self.d_type_share:
                self.d_type_share[t] = 0
        # Normalize if necessary
        total = sum(self.d_type_share.values())
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: profile is not normalized, I will normalize it.")
            for t in self.d_type_share.keys():
                self.d_type_share[t] = self.d_type_share[t] / total

    def have_ranking_with_utility_above_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly above a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_above_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.have_ranking_with_utility_above_u(ranking='cab', u=.5)
            Fraction(1, 10)
        """
        high_u = self.d_type_share[ranking[:2] + '_' + ranking[2:]]  # E.g. ab_c
        low_u = self.d_type_share[ranking[:1] + '_' + ranking[1:]]   # E.g. a_bc
        if u == 1:
            return 0
        if u == 0:
            return high_u + low_u
        return high_u

    def have_ranking_with_utility_u(self, ranking, u):
        """Share of voters who have a given ranking and a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.have_ranking_with_utility_u(ranking='cab', u=.5)
            0
        """
        return 0

    def have_ranking_with_utility_below_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly below a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_below_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.have_ranking_with_utility_below_u(ranking='cab', u=.5)
            Fraction(1, 5)
        """
        high_u = self.d_type_share[ranking[:2] + '_' + ranking[2:]]  # E.g. ab_c
        low_u = self.d_type_share[ranking[:1] + '_' + ranking[1:]]   # E.g. a_bc
        if u == 1:
            return high_u + low_u
        if u == 0:
            return 0
        return low_u

    def __repr__(self):
        return 'ProfileTwelve(%r)' % self.d_type_share

    def __str__(self):
        result = '<%s>' % str(self.d_type_share)[1:-1]
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
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r == ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                     'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            True
        """
        return isinstance(other, ProfileTwelve) and self.d_type_share == other.d_type_share

    # Standardized version of the profile (makes it unique, up to permutations)

    @cached_property
    def standardized_version(self):
        """ProfileTwelve : Standardized version of the profile (makes it unique, up to permutations of the candidates).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> print(r.standardized_version)
            <a_bc: 3/5, ba_c: 1/10, c_ba: 1/5, cb_a: 1/10> (Condorcet winner: a)
            >>> r.is_standardized
            False
        """
        def translate(s, permute):
            return s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])

        best_d = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_test = {translate(t, perm): share for t, share in self.d_type_share.items()}
            signature_test = [d_test[t] for t in XYZ_TWELVE_TYPES]
            if signature_test > best_signature:
                best_signature = signature_test
                best_d = d_test
        return ProfileTwelve({t: best_d[xyz_t] for t, xyz_t in zip(TWELVE_TYPES, XYZ_TWELVE_TYPES)})

    @cached_property
    def has_majority_type(self):
        """bool : Whether there is a majority type (a type shared by strictly more than half of the voters).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.has_majority_type
            True
        """
        return max(self.d_type_share.values()) > 0.5

    # Has full support
    @cached_property
    def support_in_types(self):
        """:class:`SetPrintingInOrder` of str : Support of the profile (in terms of types).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.support_in_types
            {'ab_c', 'b_ac', 'c_ab', 'ca_b'}
        """
        return SetPrintingInOrder({t for t, share in self.d_type_share.items() if share > 0})

    @cached_property
    def is_generic_in_types(self):
        """bool : Whether the profile is generic in types (contains all types).

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.is_generic_in_types
            False
        """
        return 0 not in self.d_type_share.values()

    # Tau and strategy-related stuff

    def tau(self, sigma):
        """Tau-vector associated to a strategy.

        Parameters
        ----------
        sigma : StrategyTwelve

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `sigma`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> sigma = StrategyTwelve({'abc': 'ab', 'bac': 'b', 'cab': 'utility-dependent'})
            >>> tau = r.tau(sigma)
            >>> print(tau)
            <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
            >>> tau = r.τ(sigma)  # Alternate notation
            >>> print(tau)
            <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        """
        t = {'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 0, 'bc': 0}
        for ranking, ballot in sigma.d_ranking_ballot.items():
            if self.d_ranking_share[ranking] == 0:
                continue
            # For a ranking abc, ballot can be '', 'a', 'ab' or 'utility-dependent'.
            if ballot == UTILITY_DEPENDENT:
                t[ballot_one(ranking)] += self.have_ranking_with_utility_below_u(ranking, u=.5)
                t[ballot_one_two(ranking)] += self.have_ranking_with_utility_above_u(ranking, u=.5)
            else:
                t[ballot] += self.d_ranking_share[ranking]
        return TauVector(t)

    def is_equilibrium(self, sigma):
        """Whether a strategy is an equilibrium.

        Parameters
        ----------
        sigma : StrategyTwelve

        Returns
        -------
        EquilibriumStatus
            Whether `sigma` is an equilibrium in this profile.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> sigma = StrategyTwelve({'abc': 'ab', 'bac': 'b', 'cab': 'utility-dependent'})
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
            else:
                type_1 = ranking[:1] + '_' + ranking[1:]  # E.g. a_bc
                type_12 = ranking[:2] + '_' + ranking[2:]  # E.g. ab_c
                if best_response.ballot == UTILITY_DEPENDENT:
                    best_ballot_1 = ballot_one(ranking)
                    best_ballot_12 = ballot_one_two(ranking)
                else:
                    best_ballot_1 = best_response.ballot
                    best_ballot_12 = best_response.ballot
                if self.d_type_share[type_1] > 0 and getattr(sigma, type_1) != best_ballot_1:
                    return EquilibriumStatus.NOT_EQUILIBRIUM
                if self.d_type_share[type_12] > 0 and getattr(sigma, type_12) != best_ballot_12:
                    return EquilibriumStatus.NOT_EQUILIBRIUM
        return status

    @cached_property
    def analyzed_strategies(self):
        """AnalyzedStrategies : Analyzed strategies of the profile.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
            ...                    'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)})
            >>> r.analyzed_strategies
            Equilibria:
            <abc: a, bac: b, cab: ac> ==> b (FF)
            <abc: a, bac: ab, cab: c> ==> a (D)
            <abc: ab, bac: b, cab: utility-dependent> ==> b (FF)
            <BLANKLINE>
            Non-equilibria:
            <abc: a, bac: b, cab: c> ==> b (FF)
            <abc: a, bac: b, cab: utility-dependent> ==> b (FF)
            <abc: a, bac: ab, cab: ac> ==> a (D)
            <abc: a, bac: ab, cab: utility-dependent> ==> a (D)
            <abc: ab, bac: b, cab: c> ==> b (FF)
            <abc: ab, bac: b, cab: ac> ==> b (FF)
            <abc: ab, bac: ab, cab: c> ==> a, b (FF)
            <abc: ab, bac: ab, cab: ac> ==> a (D)
            <abc: ab, bac: ab, cab: utility-dependent> ==> a (D)
        """
        equilibria = []
        utility_dependent = []
        inconclusive = []
        non_equilibria = []

        def possible_strategies(share_ranking_1, share_ranking_12, strategy_1, strategy_12):
            if share_ranking_1 > 0 and share_ranking_12 > 0:
                return [strategy_1, strategy_12, UTILITY_DEPENDENT]
            elif share_ranking_1 > 0 or share_ranking_12 > 0:
                return [strategy_1, strategy_12]
            else:
                return ['']

        for s_abc in possible_strategies(self.a_bc, self.ab_c, 'a', 'ab'):
            for s_acb in possible_strategies(self.a_cb, self.ac_b, 'a', 'ac'):
                for s_bac in possible_strategies(self.b_ac, self.ba_c, 'b', 'ab'):
                    for s_bca in possible_strategies(self.b_ca, self.bc_a, 'b', 'bc'):
                        for s_cab in possible_strategies(self.c_ab, self.ca_b, 'c', 'ac'):
                            for s_cba in possible_strategies(self.c_ba, self.cb_a, 'c', 'bc'):
                                sigma = StrategyTwelve({'abc': s_abc, 'acb': s_acb, 'bac': s_bac,
                                                        'bca': s_bca, 'cab': s_cab, 'cba': s_cba}, profile=self)
                                status = sigma.is_equilibrium
                                if status == EquilibriumStatus.EQUILIBRIUM:
                                    equilibria.append(sigma)
                                elif status == EquilibriumStatus.UTILITY_DEPENDENT:
                                    utility_dependent.append(sigma)
                                    warnings.warn('Met a utility-dependent case: \nr = %r\nsigma = %r' % (self, sigma))
                                elif status == EquilibriumStatus.INCONCLUSIVE:
                                    inconclusive.append(sigma)
                                    warnings.warn('Met an inconclusive case: \nr = %r\nsigma = %r' % (self, sigma))
                                else:
                                    non_equilibria.append(sigma)
        return AnalyzedStrategies(equilibria, utility_dependent, inconclusive, non_equilibria)


def make_property_type_share(t, doc):
    def _f(self):
        return self.d_type_share[t]
    _f.__doc__ = doc
    return property(_f)


for my_t in TWELVE_TYPES:
    setattr(ProfileTwelve, my_t, make_property_type_share(my_t, 'Number : Share of voters with this type.'))
