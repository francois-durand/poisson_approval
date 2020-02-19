import numpy as np
from poisson_approval.constants.constants import *
from poisson_approval.containers.Winners import Winners
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold
from poisson_approval.utils.SetPrintingInOrder import SetPrintingInOrder
from poisson_approval.utils.Util import is_lover, my_division, sort_ballot
from poisson_approval.utils.UtilCache import cached_property, DeleteCacheMixin, property_deleting_cache


# noinspection PyUnresolvedReferences
class Profile(DeleteCacheMixin):
    """A profile of preference (abstract class)."""

    def __init__(self, voting_rule):
        self.voting_rule = voting_rule

    voting_rule = property_deleting_cache('_voting_rule')

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    @cached_property
    def d_ranking_share(self):
        """dict : Shares of rankings.
            E.g. ``'abc': 0.3`` means that a ratio 0.3 of the voters have ranking ``'abc'``.
        """
        raise NotImplementedError

    @cached_property
    def d_weak_order_share(self):
        """dict : Shares of weak orders.
            E.g. ``'a~b>c': 0.3`` means that a ratio 0.3 of the voters have weak order ``'a~b>c'``.
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
        ab = (self.abc + self.acb + self.cab - self.bac - self.bca - self.cba
              + self.d_weak_order_share['a>b~c'] - self.d_weak_order_share['b~c>a']
              + self.d_weak_order_share['a~c>b'] - self.d_weak_order_share['b>a~c'])
        ac = (self.abc + self.acb + self.bac - self.bca - self.cab - self.cba
              + self.d_weak_order_share['a>b~c'] - self.d_weak_order_share['b~c>a']
              + self.d_weak_order_share['a~b>c'] - self.d_weak_order_share['c>a~b'])
        bc = (self.abc + self.bac + self.bca - self.acb - self.cab - self.cba
              + self.d_weak_order_share['b>a~c'] - self.d_weak_order_share['a~c>b']
              + self.d_weak_order_share['a~b>c'] - self.d_weak_order_share['c>a~b'])
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
        return (self.abc + self.acb + self.d_weak_order_share['a>b~c'] > 0.5
                or self.bac + self.bca + self.d_weak_order_share['b>a~c'] > 0.5
                or self.cab + self.cba + self.d_weak_order_share['c>a~b'] > 0.5)

    @cached_property
    def has_majority_ranking(self):
        """bool : Whether there is a majority ranking (a ranking shared by strictly more than half of the voters)."""
        return max(self.d_ranking_share.values()) > 0.5

    # Single-peakedness
    @cached_property
    def is_single_peaked(self):
        """bool : Whether the profile is single-peaked."""
        return ((self.abc == 0 and self.bac == 0 and self.d_weak_order_share['a~b>c'] == 0
                 and self.d_weak_order_share['a>b~c'] == 0 and self.d_weak_order_share['b>a~c'] == 0)
                or (self.acb == 0 and self.cab == 0 and self.d_weak_order_share['a~c>b'] == 0
                    and self.d_weak_order_share['a>b~c'] == 0  and self.d_weak_order_share['c>a~b'] == 0)
                or (self.bca == 0 and self.cba == 0 and self.d_weak_order_share['b~c>a'] == 0
                    and self.d_weak_order_share['c>a~b'] == 0  and self.d_weak_order_share['b>a~c'] == 0))

    # Has full support
    @cached_property
    def support_in_rankings(self):
        """:class:`SetPrintingInOrder` of str : Support of the profile (in terms of rankings)."""
        return SetPrintingInOrder({key for key, val in self.d_ranking_share.items() if val > 0})

    @cached_property
    def is_generic_in_rankings(self):
        """bool : Whether the profile is generic in rankings (contains all rankings)."""
        return 0 not in self.d_ranking_share.values()

    @cached_property
    def contains_rankings(self):
        """bool : Whether the profile contains some rankings."""
        return len(self.support_in_rankings) > 0

    @cached_property
    def support_in_weak_orders(self):
        """:class:`SetPrintingInOrder` of str : Support of the profile (in terms of weak orders)."""
        return SetPrintingInOrder({key for key, val in self.d_weak_order_share.items() if val > 0})

    @cached_property
    def contains_weak_orders(self):
        """bool : Whether the profile contains some weak orders."""
        return len(self.support_in_weak_orders) > 0

    # Tau and strategy-related stuff

    def tau(self, strategy):
        """Tau-vector associated to this profile and a given strategy.

        Parameters
        ----------
        strategy : Strategy
            A strategy that specifies at least all the rankings that are present in the profile.

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `strategy`.
        """
        raise NotImplementedError

    # noinspection NonAsciiCharacters
    def τ(self, strategy):
        """Tau-vector (alternate notation).

        Parameters
        ----------
        strategy : Strategy
            A strategy that specifies at least all the rankings that are present in the profile.

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `strategy`.
        """
        return self.tau(strategy)

    @cached_property
    def d_ballot_share_weak_voters_fanatic(self):
        """dict : Ballot shares due to the weak orders if they vote fanatically

        Voters of the type ``'a>b~c'``:

        * In Approval or Plurality, they vote for `a`.
        * In Anti-plurality, half of them vote for `ab` (i.e. against `c`) and half of them vote for `ac` (i.e.
          against `b`).

        Voters of the type ``'a~b>c'``:

        * In Approval or Plurality, half of them vote for `a` and half of them vote for `b`.
        * In Anti-plurality, they vote for `ab` (i.e. against `c`).
        """
        d = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for weak_order, share in self.d_weak_order_share.items():
            if is_lover(weak_order):
                if self.voting_rule in {APPROVAL, PLURALITY}:
                    d[weak_order[0]] += share
                elif self.voting_rule == ANTI_PLURALITY:
                    d[sort_ballot(weak_order[0] + weak_order[2])] += my_division(share, 2)
                    d[sort_ballot(weak_order[0] + weak_order[4])] += my_division(share, 2)
                else:
                    raise NotImplementedError
            else:  # is_hater(weak_order)
                if self.voting_rule in {APPROVAL, PLURALITY}:
                    d[weak_order[0]] += my_division(share, 2)
                    d[weak_order[2]] += my_division(share, 2)
                elif self.voting_rule == ANTI_PLURALITY:
                    d[sort_ballot(weak_order[0] + weak_order[2])] += share
                else:
                    raise NotImplementedError
        return d

    @cached_property
    def d_ballot_share_weak_voters_sincere(self):
        """dict : Ballot shares due to the weak orders if they vote sincerely

        Voters of the type ``'a>b~c'``:

        * In Approval or Plurality, they vote for `a`.
        * In Anti-plurality, half of them vote for `ab` (i.e. against `c`) and half of them vote for `ac` (i.e.
          against `b`).

        Voters of the type ``'a~b>c'``:

        * In Approval or Anti-plurality, they vote for `ab` (i.e. against `c`).
        * In Plurality, half of them vote for `a` and half of them vote for `b`.
        """
        d = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for weak_order, share in self.d_weak_order_share.items():
            if is_lover(weak_order):
                if self.voting_rule in {APPROVAL, PLURALITY}:
                    d[weak_order[0]] += share
                elif self.voting_rule == ANTI_PLURALITY:
                    d[sort_ballot(weak_order[0] + weak_order[2])] += my_division(share, 2)
                    d[sort_ballot(weak_order[0] + weak_order[4])] += my_division(share, 2)
                else:
                    raise NotImplementedError
            else:  # is_hater(weak_order)
                if self.voting_rule == PLURALITY:
                    d[weak_order[0]] += my_division(share, 2)
                    d[weak_order[2]] += my_division(share, 2)
                elif self.voting_rule in {APPROVAL, ANTI_PLURALITY}:
                    d[sort_ballot(weak_order[0] + weak_order[2])] += share
                else:
                    raise NotImplementedError
        return d

    def is_equilibrium(self, strategy):
        """Whether a strategy is an equilibrium in this profile.

        Parameters
        ----------
        strategy : Strategy
            A strategy that specifies at least all the rankings that are present in the profile.

        Returns
        -------
        EquilibriumStatus
            Whether `strategy` is an equilibrium in this profile.
        """
        raise NotImplementedError

    def best_responses_to_strategy(self, d_ranking_best_response):
        """Convert best responses to a :class:`StrategyThreshold`.

        Parameters
        ----------
        d_ranking_best_response : dict
            Key: ranking. Value: :class:`BestResponseApproval`.

        Returns
        -------
        StrategyThreshold
            The conversion of the best responses into a strategy. Only the rankings present in this profile are
            mentioned in the strategy.
        """
        return StrategyThreshold({
            ranking: best_response.threshold_utility
            for ranking, best_response in d_ranking_best_response.items()
            if self.d_ranking_share[ranking] > 0
        }, profile=self, voting_rule=self.voting_rule)

    @cached_property
    def analyzed_strategies(self):
        """AnalyzedStrategies : Analyzed strategies of the profile.

        Not implemented for this class.
        """
        raise NotImplementedError

    @cached_property
    def winners_at_equilibrium(self):
        """Winners : The possible winners at equilibrium.

        This gives the winners in all `equilibria` of :meth:`analyzed_strategies` (without the utility-dependent
        equilibria, even in the classes of profile that may have some).

        For an example, cf. :meth:`ProfileOrdinal.analyzed_strategies`.
        """
        if not self.analyzed_strategies.equilibria:
            return Winners(set())
        else:
            return Winners(set.union(*[strategy.winners for strategy in self.analyzed_strategies.equilibria]))


def make_property_ranking_share(ranking, doc):
    def _f(self):
        return self.d_ranking_share[ranking]
    _f.__doc__ = doc
    return property(_f)


for my_ranking in RANKINGS:
    setattr(Profile, my_ranking, make_property_ranking_share(my_ranking, 'Number : Share of voters with this ranking.'))
