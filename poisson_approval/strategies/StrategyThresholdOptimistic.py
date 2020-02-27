from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.utils.DictPrintingInOrderIgnoringNone import DictPrintingInOrderIgnoringNone
from poisson_approval.utils.Util import ballot_one, ballot_two, ballot_one_two, ballot_one_three


# noinspection PyUnresolvedReferences
class StrategyThresholdOptimistic(StrategyThreshold):
    """An optimistic threshold strategy.

    This is a particular case of :class:`StrategyThreshold` where, for any ranking, the ratio of optimistic voters
    is equal to 1.

    Parameters
    ----------
    d_ranking_threshold : dict
        Keys are rankings and values are utility thresholds. E.g. ``'abc': 0.4`` means that a voter ``abc`` vote for
        ``ab`` if her utility for ``b`` is strictly greater than 0.4, and for ``a`` otherwise. A threshold can be
        ``None``, meaning that the behavior of these voters is not specified in the strategy.
    profile : Profile, optional
        The "context" in which the strategy is used.
    voting_rule : str
        The voting rule. Possible values are ``APPROVAL``, ``PLURALITY`` and ``ANTI_PLURALITY``. Default: the same
        voting rule as `profile` if a profile is specified, ``APPROVAL`` otherwise.

    Examples
    --------
        >>> strategy = StrategyThresholdOptimistic({'abc': 0.4, 'bac': 0.51, 'cab': 1})
        >>> strategy
        StrategyThresholdOptimistic({'abc': 0.4, 'bac': 0.51, 'cab': 1})
        >>> print(strategy)
        <abc: utility-dependent (0.4), bac: utility-dependent (0.51), cab: c>
        >>> strategy.abc
        'utility-dependent'
        >>> strategy.a_bc
        'a'
        >>> strategy.ab_c
        'ab'
        >>> strategy.d_ranking_threshold['abc']
        0.4
    """

    def __init__(self, d_ranking_threshold, profile=None, voting_rule=None):
        voting_rule = self._get_voting_rule_(profile, voting_rule)
        super().__init__(d_ranking_threshold, ratio_optimistic=1, profile=profile, voting_rule=voting_rule)

    def __repr__(self):
        arguments = repr(self.d_ranking_threshold)
        if self.voting_rule != APPROVAL:
            arguments += ', voting_rule=%r' % self.voting_rule
        return 'StrategyThresholdOptimistic(%s)' % arguments

    def __str__(self):
        result = '<' + ', '.join([
            '%s: %s' % (ranking, self.d_ranking_ballot[ranking])
            + (' (%s)' % self.d_ranking_threshold[ranking]
               if self.d_ranking_ballot[ranking] == UTILITY_DEPENDENT else '')
            for ranking in sorted(self.d_ranking_ballot) if self.d_ranking_ballot[ranking]
        ]) + '>'
        if self.profile is not None:
            result += ' ==> ' + str(self.winners)
        if self.voting_rule != APPROVAL:
            result += ' (%s)' % self.voting_rule
        return result

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')
