from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import ballot_one, ballot_one_two
from poisson_approval.profiles.Profile import Profile
from poisson_approval.tau_vector.TauVector import TauVector
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.constants.EquilibriumStatus import EquilibriumStatus
from poisson_approval.utils.UtilCache import cached_property
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold


# noinspection PyUnresolvedReferences
class ProfileCardinal(Profile):
    """A cardinal profile of preference (abstract class)."""

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

    def tau(self, sigma):
        """Tau-vector associated to a strategy.

        Parameters
        ----------
        sigma : StrategyThreshold

        Returns
        -------
        TauVector
            Tau-vector associated to this profile and strategy `sigma`.
        """
        t = {ballot: 0 for ballot in BALLOTS_WITHOUT_INVERSIONS}
        for ranking, threshold in sigma.d_ranking_threshold.items():
            if self.d_ranking_share[ranking] == 0:
                continue
            t[ballot_one(ranking)] += (self.have_ranking_with_utility_u(ranking, u=threshold)
                                       + self.have_ranking_with_utility_below_u(ranking, u=threshold))
            t[ballot_one_two(ranking)] += self.have_ranking_with_utility_above_u(ranking, u=threshold)
        return TauVector(t)

    def is_equilibrium(self, sigma):
        """Whether a strategy is an equilibrium.

        Parameters
        ----------
        sigma : StrategyThreshold

        Returns
        -------
        EquilibriumStatus
            Whether `sigma` is an equilibrium in this profile.
        """
        d_ranking_best_response = self.tau(sigma).d_ranking_best_response
        status = EquilibriumStatus.EQUILIBRIUM
        for ranking, share in self.d_ranking_share.items():
            if share == 0:
                continue
            best_response = d_ranking_best_response[ranking]
            if sigma.d_ranking_threshold[ranking] is None:
                status = min(status, EquilibriumStatus.INCONCLUSIVE)
            elif best_response.ballot == INCONCLUSIVE:
                status = min(status, EquilibriumStatus.INCONCLUSIVE)
            else:
                should_vote_12 = self.have_ranking_with_utility_above_u(ranking, u=best_response.threshold_utility)
                do_vote_12 = self.have_ranking_with_utility_above_u(ranking, u=sigma.d_ranking_threshold[ranking])
                if not isclose(should_vote_12, do_vote_12):
                    return EquilibriumStatus.NOT_EQUILIBRIUM
        return status

    def iterated_voting(self, sigma_ini, n_max_episodes, verbose=False):
        """Seek for convergence by iterated voting.

        Parameters
        ----------
        sigma_ini : StrategyThreshold
            Initial strategy.
        n_max_episodes : int
            Maximal number of iterations.
        verbose : bool
            If True, print all intermediate strategies.

        Returns
        -------
        list of :class:`StrategyThreshold`
            If length 1, the process converges to this strategy. If length > 1, the process reaches a periodical orbit
            between these strategies. If length = 0, by convention, it means that the process does not converge and
            does not reach a periodical orbit.
        """
        sigma = StrategyThreshold({
            ranking: threshold for ranking, threshold in sigma_ini.d_ranking_threshold.items()
            if self.d_ranking_share[ranking] > 0
        }, profile=self)
        sigmas = [sigma]
        if verbose:
            print(-1)
            print(sigma)
        for i in range(n_max_episodes):
            sigma = StrategyThreshold(
                {ranking: best_response.threshold_utility
                 for ranking, best_response in sigma.d_ranking_best_response.items()
                 if self.d_ranking_share[ranking] > 0},
                profile=self)
            if verbose:
                print(i)
                print(sigma)
            if sigma in sigmas:
                # If there is an exact cycle, it is useless to continue looping.
                sigmas.append(sigma)
                break
            else:
                sigmas.append(sigma)
        try:
            begin, end = next((begin, end)
                              for end in range(len(sigmas) - 1, 0, -1)
                              for begin in range(end - 1, -1, -1)
                              if sigmas[begin].isclose(sigmas[end]))
            return sigmas[begin:end]
        except StopIteration:
            return []
