from poisson_approval.profiles.ProfileCardinal import ProfileCardinal
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold


# noinspection PyAbstractClass
class ProfileCardinalContinuous(ProfileCardinal):
    """A cardinal profile of preference with no atom (abstract class).

    Parameters
    ----------
    Cf. :class:`ProfileCardinal`.
    """

    is_continuous = True

    def have_ranking_with_utility_u(self, ranking, u):
        """Share of voters who have a given ranking and a given utility for their middle candidate.

        Since it is a continuous profile, this method always returns 0.
        """
        return 0

    def best_responses_to_strategy(self, d_ranking_best_response):
        """Convert best responses to a :class:`StrategyThreshold`.

        Parameters
        ----------
        d_ranking_best_response : dict
            Key: ranking. Value: :class:`BestResponse`.

        Returns
        -------
        StrategyThreshold
            The conversion of the best responses into a strategy. Only the rankings present in this profile are
            mentioned in the strategy.
        """
        # The only difference with parent class is that ratio_optimistic is not specified because we don't care.
        return StrategyThreshold({
            ranking: best_response.threshold_utility
            for ranking, best_response in d_ranking_best_response.items()
            if self.d_ranking_share[ranking] > 0
        }, profile=self, voting_rule=self.voting_rule)
