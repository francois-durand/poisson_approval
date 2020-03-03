from poisson_approval.best_response.BestResponse import BestResponse
from poisson_approval.constants.constants import *
from poisson_approval.utils.UtilCache import cached_property


class BestResponsePlurality(BestResponse):
    """Best response for a given ordinal type of voter in Plurality.

    The main objective of this class is to compute :attr:`threshold_utility`.

    For the sake of consistency with :class:`BestResponseApproval`, it provides the string :attr:`justification`,
    indicating which sub-algorithm was used. But since there are no actual sub-algorithms for plurality, the
    justification is always the same: 'Plurality analysis'.

    Parameters
    ----------
    Cf. :class:`BestResponse`.

    Attributes
    ----------
    Cf. :class:`BestResponse`
    """

    PLURALITY_ANALYSIS = 'Plurality analysis'
    voting_rule = PLURALITY

    @cached_property
    def results(self):
        assert self.tau.voting_rule == PLURALITY
        if self.tau_i < self.tau_j and self.tau_i < self.tau_k:
            # The best response is `j`.
            threshold_utility = self.ce.S(0)
        elif 0 < self.tau_i == self.tau_k < self.tau_j:
            threshold_utility = self.ce.Rational(1, 2)
        else:
            # The best response is `i`.
            threshold_utility = self.ce.S(1)
        return threshold_utility, self.PLURALITY_ANALYSIS
