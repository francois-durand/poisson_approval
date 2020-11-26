from poisson_approval.best_response.BestResponse import BestResponse
from poisson_approval.constants.constants import *
from poisson_approval.utils.UtilCache import cached_property


class BestResponseAntiPlurality(BestResponse):
    """Best response for a given ordinal type of voter in Anti-plurality.

    The main objective of this class is to compute :attr:`threshold_utility`.

    For the sake of consistency with :class:`BestResponseApproval`, it provides the string :attr:`justification`,
    indicating which sub-algorithm was used. But since there are no actual sub-algorithms for anti-plurality, the
    justification is always the same: 'Anti-plurality analysis'.

    Parameters
    ----------
    Cf. :class:`BestResponse`.

    Attributes
    ----------
    Cf. :class:`BestResponse`
    """

    ANTI_PLURALITY_ANALYSIS = 'Anti-plurality analysis'
    voting_rule = ANTI_PLURALITY

    @cached_property
    def results(self):
        assert self.tau.voting_rule == ANTI_PLURALITY
        tau_minus_i = self.tau_jk
        tau_minus_j = self.tau_ik
        tau_minus_k = self.tau_ij
        if tau_minus_k > tau_minus_i and tau_minus_k > tau_minus_j:
            # The best response is `- j`, i.e. `ik`
            threshold_utility = self.ce.S(1)
        elif tau_minus_i == tau_minus_k > tau_minus_j:
            threshold_utility = self.ce.Rational(1, 2)
        else:
            # The best response is `- k`, i.e. `ij`
            threshold_utility = self.ce.S(0)
        return threshold_utility, self.ANTI_PLURALITY_ANALYSIS
