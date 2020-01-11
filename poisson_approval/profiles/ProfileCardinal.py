from math import isclose
from fractions import Fraction
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import ballot_one, ballot_one_two, barycenter
from poisson_approval.profiles.Profile import Profile
from poisson_approval.tau_vector.TauVector import TauVector
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.constants.EquilibriumStatus import EquilibriumStatus
from poisson_approval.utils.UtilCache import cached_property
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold


# noinspection PyUnresolvedReferences
class ProfileCardinal(Profile):
    """A cardinal profile of preference (abstract class).

    Parameters
    ----------
    ratio_sincere : Number
        The ratio of sincere voters, in the interval [0, 1]. This is used for :meth:`tau`.
    """

    def __init__(self, ratio_sincere=0):
        super().__init__()
        self.ratio_sincere = ratio_sincere

    def have_ranking_with_utility_above_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly above a given utility for their middle candidate.

        Parameters
        ----------
        ranking : str
            A ranking, e.g. ``'abc'``.
        u : Number
            A utility between 0 and 1 (included).

        Returns
        -------
        Number
            The share of voters who have ranking `ranking` and a utility for their middle candidate strictly greater
            than `u`.
        """
        raise NotImplementedError

    def have_ranking_with_utility_u(self, ranking, u):
        """Share of voters who have a given ranking and a given utility for their middle candidate.

        Parameters
        ----------
        ranking : str
            A ranking, e.g. ``'abc'``.
        u : Number
            A utility between 0 and 1 (included).

        Returns
        -------
        Number
            The share of voters who have ranking `ranking` and a utility for their middle candidate equal to `u`.
        """
        raise NotImplementedError

    def have_ranking_with_utility_below_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly below a given utility for their middle candidate.

        Parameters
        ----------
        ranking : str
            A ranking, e.g. ``'abc'``.
        u : Number
            A utility between 0 and 1 (included).

        Returns
        -------
        Number
            The share of voters who have ranking `ranking` and a utility for their middle candidate strictly lower
            than `u`.
        """
        raise NotImplementedError

    @cached_property
    def d_ranking_share(self):
        return DictPrintingInOrderIgnoringZeros({
            ranking: self.have_ranking_with_utility_above_u(ranking, 0) + self.have_ranking_with_utility_u(ranking, 0)
            for ranking in RANKINGS
        })

    def __eq__(self, other):
        raise NotImplementedError

    @cached_property
    def standardized_version(self):
        raise NotImplementedError

    # Tau and strategy-related stuff

    def tau(self, strategy):
        """Tau-vector associated to a strategy, with partial sincere voting.

        Parameters
        ----------
        strategy : an argument accepted by :meth:`tau_strategic`

        Returns
        -------
        TauVector
            A share :attr:`ratio_sincere` of the voters vote sincerely (in the sense of :attr:`tau_sincere`) and the
            rest of them vote strategically (in the sense of :meth:`tau_strategic`). In other words, this tau-vector
            is the barycenter of ``tau_sincere`` and ``tau_strategic(strategy)``, with respective weights
            ``self.ratio_sincere`` and ``1 - self.ratio_sincere``.
        """
        tau_sincere = self.tau_sincere
        tau_strategic = self.tau_strategic(strategy)
        t = {ballot: barycenter(a=tau_strategic.d_ballot_share[ballot],
                                b=tau_sincere.d_ballot_share[ballot],
                                ratio_b=self.ratio_sincere)
             for ballot in BALLOTS_WITHOUT_INVERSIONS}
        return TauVector(t)

    @cached_property
    def tau_sincere(self):
        """Tau-vector associated to sincere voting.

        Returns
        -------
        TauVector
            All voters approve of their top candidate. Voters approve of their middle candidate if and only if
            their utility for her is strictly greater than 0.5.
        """
        t = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for ranking in RANKINGS:
            share_vote_one_two = self.have_ranking_with_utility_above_u(ranking, Fraction(1, 2))
            share_vote_one = self.d_ranking_share[ranking] - share_vote_one_two
            t[ballot_one(ranking)] += share_vote_one
            t[ballot_one_two(ranking)] += share_vote_one_two
        return TauVector(t)

    def tau_strategic(self, strategy):
        """Tau-vector associated to a strategy (fully strategic voting).

        Parameters
        ----------
        strategy : StrategyThreshold

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `strategy`.
        """
        t = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for ranking, threshold in strategy.d_ranking_threshold.items():
            if self.d_ranking_share[ranking] == 0:
                continue
            t[ballot_one(ranking)] += (self.have_ranking_with_utility_u(ranking, u=threshold)
                                       + self.have_ranking_with_utility_below_u(ranking, u=threshold))
            t[ballot_one_two(ranking)] += self.have_ranking_with_utility_above_u(ranking, u=threshold)
        return TauVector(t)

    def is_equilibrium(self, strategy):
        """Whether a strategy is an equilibrium.

        Parameters
        ----------
        strategy : StrategyThreshold

        Returns
        -------
        EquilibriumStatus
            Whether `strategy` is an equilibrium in this profile. This is based on the assumption that:

            * A proportion :attr:`ratio_sincere` of voters cast their ballot sincerely (in the sense of
              :attr:`tau_sincere`),
            * And the rest of the voters use `strategy`.
        """
        this_tau = self.tau(strategy)
        d_ranking_best_response = this_tau.d_ranking_best_response
        d_ranking_threshold = dict()
        for ranking, share in self.d_ranking_share.items():
            if share == 0:
                continue
            if strategy.d_ranking_threshold[ranking] is None:
                return EquilibriumStatus.INCONCLUSIVE
            best_response = d_ranking_best_response[ranking]
            if best_response.ballot == INCONCLUSIVE:
                return EquilibriumStatus.INCONCLUSIVE
            d_ranking_threshold[ranking] = best_response.threshold_utility
        tau_response = self.tau(StrategyThreshold(d_ranking_threshold))
        if tau_response.isclose(this_tau):
            return EquilibriumStatus.EQUILIBRIUM
        else:
            return EquilibriumStatus.NOT_EQUILIBRIUM

    def iterated_voting_strategies(self, strategy_ini, n_max_episodes, update_ratio=1, verbose=False):
        """Seek for convergence by iterated voting (strategy update).

        Parameters
        ----------
        strategy_ini : StrategyThreshold
            Initial strategy.
        n_max_episodes : int
            Maximal number of iterations.
        update_ratio : Number
            The speed at which the utility threshold of the strategy being used moves toward the utility threshold of
            the best response. For example, for voters `abc`, if the current threshold of their strategy is `t` and the
            threshold of their best response is `u`, then the threshold of their updated strategy will be
            ``(1 - update_ratio) * t + update_ratio * u``.
        verbose : bool
            If True, print all intermediate strategies.

        Returns
        -------
        dict
            * Key ``cycle``: a list of :class:`TauVector`. The limit cycle of tau-vectors. If its length is 1, the
              process converges to this tau-vector. If its length is greater than 1, the process reaches a periodical
              orbit between these tau-vectors. If its length is 0, by convention, it means that the process does not
              converge and does not reach a periodical orbit.
            * Key ``responses``: a list of :class:`StrategyThreshold`. Its length is the same as ``cycle``. Each
              element represent the strategy that is the best response to the corresponding tau-vector. For example,
              if ``update_ratio == 1``, it is the strategy that all strategic voters use at the following step of the
              cycle.
        """
        strategy = StrategyThreshold({
            ranking: threshold for ranking, threshold in strategy_ini.d_ranking_threshold.items()
            if self.d_ranking_share[ranking] > 0
        }, profile=self)
        tau = strategy.tau
        taus = [tau]
        if verbose:
            print(-1)
            print(strategy)
        for i in range(n_max_episodes):
            strategy = StrategyThreshold(
                {ranking: _my_round(barycenter(a=strategy.d_ranking_threshold[ranking],
                                               b=strategy.d_ranking_best_response[ranking].threshold_utility,
                                               ratio_b=update_ratio))
                 for ranking in RANKINGS if self.d_ranking_share[ranking] > 0},
                profile=self)
            tau = strategy.tau
            if verbose:
                print(i)
                print(strategy)
            if tau in taus:
                # If there is an exact cycle, it is useless to continue looping.
                taus.append(tau)
                break
            else:
                taus.append(tau)
        try:
            end = len(taus) - 1
            begin = next(begin
                         for begin in range(end - 1, -1, -1)
                         if taus[begin].isclose(taus[end]))
            cycle_taus = taus[begin:end]
        except StopIteration:
            cycle_taus = []
        responses = [self.best_responses_to_strategy(tau.d_ranking_best_response) for tau in cycle_taus]
        return {'cycle_taus': cycle_taus, 'responses': responses}

    def iterated_voting_taus(self, strategy_ini, n_max_episodes, update_ratio=1, verbose=False):
        """Seek for convergence by iterated voting (tau update).

        Parameters
        ----------
        strategy_ini : StrategyThreshold
            Initial strategy.
        n_max_episodes : int
            Maximal number of iterations.
        update_ratio : Number
            The ratio of voters that update their ballot. At each iteration, this ratio of voters update their response
            (they continue voting sincerely if they are sincere voters, they update their strategical ballot otherwise).
            In other words, the updated tau-vector is a barycenter of the former tau-vector with weight
            ``1 - update_ratio`` and the response tau-vector (as computed by :meth:``tau``) with weight
            ``update_ratio``.
        verbose : bool
            If True, print all intermediate tau-vectors.

        Returns
        -------
        dict
            * Key ``cycle``: a list of :class:`TauVector`. The limit cycle of tau-vectors. If its length is 1, the
              process converges to this tau-vector. If its length is greater than 1, the process reaches a periodical
              orbit between these tau-vectors. If its length is 0, by convention, it means that the process does not
              converge and does not reach a periodical orbit.
            * Key ``responses``: a list of :class:`StrategyThreshold`. Its length is the same as ``cycle``. Each
              element represent the strategy that is the best response to the corresponding tau-vector. For example,
              if ``update_ratio == 1``, it is the strategy that all strategic voters use at the following step of the
              cycle.
        """

        strategy = StrategyThreshold({
            ranking: threshold for ranking, threshold in strategy_ini.d_ranking_threshold.items()
            if self.d_ranking_share[ranking] > 0
        }, profile=self)
        tau = strategy.tau
        taus = [tau]
        if verbose:
            print(-1)
            print(tau)
        for i in range(n_max_episodes):
            strategy = StrategyThreshold(
                {ranking: tau.d_ranking_best_response[ranking].threshold_utility
                 for ranking in RANKINGS if self.d_ranking_share[ranking] > 0},
                profile=self)
            tau_full_response = strategy.tau
            tau = TauVector({
                ballot: _my_round(barycenter(a=tau.d_ballot_share[ballot],
                                             b=tau_full_response.d_ballot_share[ballot],
                                             ratio_b=update_ratio))
                for ballot in BALLOTS_WITHOUT_INVERSIONS
            }, normalization_warning=False)
            if verbose:
                print(i)
                print(tau)
            if tau in taus:
                # If there is an exact cycle, it is useless to continue looping.
                taus.append(tau)
                break
            else:
                taus.append(tau)
        try:
            end = len(taus) - 1
            begin = next(begin
                         for begin in range(end - 1, -1, -1)
                         if taus[begin].isclose(taus[end]))
            cycle_taus = taus[begin:end]
        except StopIteration:
            cycle_taus = []
        responses = [self.best_responses_to_strategy(tau.d_ranking_best_response) for tau in cycle_taus]
        return {'cycle_taus': cycle_taus, 'responses': responses}


def _my_round(x):
    """Round to 0 or 1 if the number is close enough.

    Parameters
    ----------
    x : Number

    Returns
    -------
    Number
        Generally, return `x`. If `x` is close enough to 0 or 1, then return 0 or 1 respectively.

    Examples
    --------

        >>> _my_round(1E-10)
        0
        >>> _my_round(0.999999999999999999)
        1
        >>> _my_round(0.123456789)
        0.123456789
    """
    if isclose(x, 1):
        return 1
    if isclose(x, 0, abs_tol=1E-9):
        return 0
    return x
