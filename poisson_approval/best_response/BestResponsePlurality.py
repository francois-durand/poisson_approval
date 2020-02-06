from fractions import Fraction
from poisson_approval.best_response.BestResponse import BestResponse
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import ballot_one, ballot_two
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

    @cached_property
    def results(self):
        assert self.tau_ij == self.tau_ik == self.tau_jk == 0
        if self.tau_i < self.tau_j and self.tau_i < self.tau_k:
            # The best response is `j`.
            threshold_utility = 0
        elif self.tau_i == self.tau_k < self.tau_j:
            threshold_utility = Fraction(1, 2)
        else:
            # The best response is `i`.
            threshold_utility = 1
        return threshold_utility, self.PLURALITY_ANALYSIS

    @cached_property
    def ballot(self):
        """str : This can be a valid ballot (e.g. ``'a'`` or ``'b'`` if `ranking` is ``'abc'``) or
        ``'utility-dependent'``.
        """
        if self.threshold_utility == 1:
            return ballot_one(self.ranking)
        elif self.threshold_utility == 0:
            return ballot_two(self.ranking)
        else:
            return UTILITY_DEPENDENT
