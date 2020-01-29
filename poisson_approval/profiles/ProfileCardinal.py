from math import isclose
from copy import deepcopy
from fractions import Fraction
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import ballot_one, ballot_one_two, barycenter, to_callable
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
            A strategy that specifies at least all the rankings that are present in the profile.

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
            A strategy that specifies at least all the rankings that are present in the profile.

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
            best_response = d_ranking_best_response[ranking]
            if best_response.ballot == INCONCLUSIVE:  # pragma: no cover
                return EquilibriumStatus.INCONCLUSIVE
            d_ranking_threshold[ranking] = best_response.threshold_utility
        tau_response = self.tau(StrategyThreshold(d_ranking_threshold))
        if tau_response.isclose(this_tau):
            return EquilibriumStatus.EQUILIBRIUM
        else:
            return EquilibriumStatus.NOT_EQUILIBRIUM

    def iterated_voting(self, strategy_ini, n_max_episodes,
                        perception_update_ratio=1, ballot_update_ratio=1, verbose=False):
        """Seek for convergence by iterated voting.

        Parameters
        ----------
        strategy_ini : an argument accepted by :meth:`tau`, i.e. by :meth:`tau_strategic`
            The initial strategy.
        n_max_episodes : int
            Maximal number of iterations.
        perception_update_ratio : Number in [0, 1]
            The coefficient when updating the perceived tau:
            ``tau_perceived = (1 - perception_update_ratio) * tau_perceived + perception_update_ratio * tau_actual``.
        ballot_update_ratio : Number in [0, 1]
            The ratio of voters who update their ballot:
            ``tau_actual = (1 - ballot_update_ratio) * tau_actual + ballot_update_ratio * tau_response``.
        verbose : bool
            If True, print all intermediate steps.

        Returns
        -------
        dict
            * Key ``cycle_taus_perceived``: list of :class:`TauVector`. The limit cycle of perceived tau-vectors.
              ``cycle_taus_perceived[t]`` is a barycenter of ``cycle_taus_perceived[t - 1]`` with
              ``cycle_taus_actual[t - 1]``, parametrized by `perception_update_ratio`.
            * Key ``cycle_strategies``: list of :class:`StrategyThreshold`. The limit cycle of strategies.
              ``cycle_strategies[t]`` is the best response to ``cycle_taus_perceived[t]``.
            * Key ``cycle_taus_actual``: list of :class:`TauVector`. The limit cycle of actual tau-vectors.
              ``cycle_taus_actual[t]`` is a barycenter of ``cycle_taus_actual[t - 1]`` and the tau-vector resulting
              from ``strategies[t]``, parametrized by `ballot_update_ratio`.
            * Key ``n_episodes``: the number of episodes until convergence. If the process did not converge, by
              convention, this value is `n_max_episodes`.

            `cycle_taus_perceived`, `cycle_strategies` and `cycle_taus_actual` have the same length. If it is 1, the
            process converges to this limit. If it is greater than 1, the process reaches a periodical orbit. If it
            is 0, by convention, it means that the process does not converge and does not reach a periodical orbit.

        Notes
        -----
        Comparison between :meth:`iterated_voting` and :meth:`fictitious_play`:

        * :meth:`iterated_voting` can detect cycles (whereas :meth:`fictitious_play` only looks for a limit).
        * :meth:`fictitious_play` accepts update ratios that are functions of the time (whereas
          :meth:`iterated_voting` only accepts constants).
        * :meth:`fictitious_play` is faster and uses less memory, because it only looks for a limit and not for a cycle.

        In general, you should use :meth:`iterated_voting` only if you care about cycles, with the constraint
        that it implies having constant update ratios.
        """
        strategy = strategy_ini.deepcopy_with_attached_profile(self)
        tau_actual = strategy.tau
        tau_perceived = tau_actual
        strategies = [strategy]
        taus_actual = [tau_actual]
        taus_perceived = [tau_perceived]
        if verbose:
            print('t = %s' % 0)
            print('strategy: %s' % strategy)
            print('tau_actual: %s' % tau_actual)
        n_episodes = n_max_episodes
        for t in range(1, n_max_episodes + 1):
            tau_perceived = TauVector({
                ballot: _my_round(barycenter(a=tau_perceived.d_ballot_share[ballot],
                                             b=tau_actual.d_ballot_share[ballot],
                                             ratio_b=perception_update_ratio))
                for ballot in BALLOTS_WITHOUT_INVERSIONS
            })
            strategy = self.best_responses_to_strategy(tau_perceived.d_ranking_best_response)
            tau_full_response = strategy.tau
            tau_actual = TauVector({
                ballot: _my_round(barycenter(a=tau_actual.d_ballot_share[ballot],
                                             b=tau_full_response.d_ballot_share[ballot],
                                             ratio_b=ballot_update_ratio))
                for ballot in BALLOTS_WITHOUT_INVERSIONS
            }, normalization_warning=False)
            if verbose:
                print('t = %s' % t)
                print('tau_perceived: %s' % tau_perceived)
                print('strategy: %s' % strategy)
                print('tau_full_response: %s' % tau_full_response)
                print('tau_actual: %s' % tau_actual)
            # If there is an exact cycle, it is useless to continue looping.
            break_ = (tau_actual, tau_perceived) in zip(taus_actual, taus_perceived)

            taus_actual.append(tau_actual)
            taus_perceived.append(tau_perceived)
            strategies.append(strategy)
            if break_:
                n_episodes = t
                break
        try:
            end = len(taus_actual) - 1
            begin = next(begin
                         for begin in range(end - 1, -1, -1)
                         if taus_actual[begin].isclose(taus_actual[end], abs_tol=1E-9)
                         and taus_perceived[begin].isclose(taus_perceived[end], abs_tol=1E-9))
            cycle_taus_actual = taus_actual[begin + 1:end + 1]
            cycle_taus_perceived = taus_perceived[begin + 1:end + 1]
            cycle_strategies = strategies[begin + 1:end + 1]
        except StopIteration:
            cycle_taus_actual = []
            cycle_taus_perceived = []
            cycle_strategies = []
        return {'cycle_taus_perceived': cycle_taus_perceived,
                'cycle_strategies': cycle_strategies,
                'cycle_taus_actual': cycle_taus_actual,
                'n_episodes': n_episodes}

    def fictitious_play(self, strategy_ini, n_max_episodes,
                        perception_update_ratio=None, ballot_update_ratio=1, verbose=False):
        """Seek for convergence by fictitious play.

        Parameters
        ----------
        strategy_ini : an argument accepted by :meth:`tau`, i.e. by :meth:`tau_strategic`
            The initial strategy.
        n_max_episodes : int
            Maximal number of iterations.
        perception_update_ratio : callable or Number
            The coefficient when updating the perceived tau:
            ``tau_perceived = (1 - perception_update_ratio(t)) * tau_perceived + perception_update_ratio(t) *
            tau_actual``. For any ``t`` from 1 to `n_max_episodes` included, the update ratio must be in [0, 1]. The
            default function is ``1 / (t + 1)``, which leads to an arithmetic average. If `perception_update_ratio` is
            a Number, it is considered as a constant function.
        ballot_update_ratio : callable or Number
            The ratio of voters who update their ballot:
            ``tau_actual = (1 - ballot_update_ratio(t)) * tau_actual + ballot_update_ratio(t) * tau_response``.
            For any ``t`` from 1 to `n_max_episodes` included, the update ratio must be in [0, 1]. The default function
            is the constant 1, which corresponds to a full update. If `ballot_update_ratio` is a Number, it is
            considered as a constant function.
        verbose : bool
            If True, print all intermediate steps.

        Returns
        -------
        dict
            * Key ``tau``: :class:`TauVector` or None. The limit tau-vector. If None, it means that the process did not
              converge.
            * Key ``strategy``: :class:`StrategyThreshold` or None. The limit strategy. If None, it means that the
              process did not converge.
            * Key ``n_episodes``: the number of episodes until convergence. If the process did not converge, by
              convention, this value is `n_max_episodes`.

        Notes
        -----
        Comparison between :meth:`iterated_voting` and :meth:`fictitious_play`:

        * :meth:`iterated_voting` can detect cycles (whereas :meth:`fictitious_play` only looks for a limit).
        * :meth:`fictitious_play` accepts update ratios that are functions of the time (whereas
          :meth:`iterated_voting` only accepts constants).
        * :meth:`fictitious_play` is faster and uses less memory, because it only looks for a limit and not for a cycle.

        In general, you should use :meth:`iterated_voting` only if you care about cycles, with the constraint
        that it implies having constant update ratios.
        """
        if perception_update_ratio is None:
            def perception_update_ratio(_t): return Fraction(1, _t + 1)
        perception_update_ratio = to_callable(perception_update_ratio)
        ballot_update_ratio = to_callable(ballot_update_ratio)

        strategy = strategy_ini.deepcopy_with_attached_profile(self)
        tau_actual = strategy.tau
        tau_perceived = tau_actual
        if verbose:
            print('t = %s' % 0)
            print('strategy: %s' % strategy)
            print('tau_actual: %s' % tau_actual)
            print('tau_perceived: %s' % tau_perceived)

        for t in range(1, n_max_episodes + 1):
            tau_perceived = TauVector({
                ballot: _my_round(barycenter(a=tau_perceived.d_ballot_share[ballot],
                                             b=tau_actual.d_ballot_share[ballot],
                                             ratio_b=perception_update_ratio(t)))
                for ballot in BALLOTS_WITHOUT_INVERSIONS
            })
            strategy = self.best_responses_to_strategy(tau_perceived.d_ranking_best_response)
            tau_full_response = strategy.tau
            tau_actual = TauVector({
                ballot: _my_round(barycenter(a=tau_actual.d_ballot_share[ballot],
                                             b=tau_full_response.d_ballot_share[ballot],
                                             ratio_b=ballot_update_ratio(t)))
                for ballot in BALLOTS_WITHOUT_INVERSIONS
            }, normalization_warning=False)
            if verbose:
                print('t = %s' % t)
                print('tau_perceived: %s' % tau_perceived)
                print('strategy: %s' % strategy)
                print('tau_full_response: %s' % tau_full_response)
                print('tau_actual: %s' % tau_actual)
            if tau_full_response.isclose(tau_perceived, abs_tol=1E-9) and tau_actual.isclose(
                    tau_full_response, abs_tol=1E-9):
                return {'tau': tau_full_response, 'strategy': strategy, 'n_episodes': t}
        return {'tau': None, 'strategy': None, 'n_episodes': n_max_episodes}


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
