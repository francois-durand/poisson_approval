from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold
from poisson_approval.utils.DictPrintingInOrderIgnoringNone import DictPrintingInOrderIgnoringNone
from poisson_approval.utils.UtilCache import cached_property


# noinspection PyUnresolvedReferences
class StrategyThresholdMixed(StrategyThreshold):
    """A mixed threshold strategy (for a profile that may have atoms).

    For each ranking, there is a ``threshold`` and a ``ratio_optimistic``. E.g. assume that for ranking ``abc``,
    the threshold is 0.4 and the ratio is 0.2. It means that:

    * A voter ``abc`` votes for `ab` if their utility for `b` is strictly greater than 0.4,
    * A voter ``abc`` votes for `a` if their utility for `b` is strictly lower than 0.4,
    * Voters ``abc`` whose utility for `b` is equal to 0.4 are split: a ratio 0.2 are optimistic, they vote only for
      `a` (they behave as if the pivot `ab` was very likely); and a ratio 0.8 are pessimistic, they vote for `ab`
      (they behave as if the pivot `bc` was very likely).

    Parameters
    ----------
    d : dict
        Cf. examples below for the different types of input syntax.
    ratio_optimistic : Number
        Cf. examples below for the different types of input syntax.
    profile : Profile, optional
        The "context" in which the strategy is used.
    voting_rule : str
        The voting rule. Possible values are ``APPROVAL``, ``PLURALITY`` and ``ANTI_PLURALITY``. Default: the same
        voting rule as `profile` if a profile is specified, ``APPROVAL`` otherwise.

    Examples
    --------
    The two following examples illustrate different ways to define the same profile. The first possible type of input
    syntax is a dict that maps a ranking to a tuple (``threshold``, ``ratio_optimistic``). It corresponds exactly to
    the attribute :attr:`d_ranking_t_threshold_ratio_optimistic`:

        >>> strategy = StrategyThresholdMixed({'abc': (0.4, 0.2), 'bac': (0.51, 0.2), 'cab': (1, 0.2)})
        >>> print(strategy)
        <abc: utility-dependent (0.4, 0.2), bac: utility-dependent (0.51, 0.2), cab: c>

    The second  possible type of input syntax is a dict that maps a ranking to a threshold. All rankings have the same
    ratio, given by the parameter `ratio_optimistic`:

        >>> strategy = StrategyThresholdMixed({'abc': 0.4, 'bac': 0.51, 'cab': 1}, ratio_optimistic=0.2)
        >>> print(strategy)
        <abc: utility-dependent (0.4, 0.2), bac: utility-dependent (0.51, 0.2), cab: c>

    Some operations on the strategy:

        >>> strategy
        StrategyThresholdMixed({'abc': (0.4, 0.2), 'bac': (0.51, 0.2), 'cab': (1, 0.2)})
        >>> strategy.abc
        'utility-dependent'
        >>> strategy.a_bc
        'a'
        >>> strategy.ab_c
        'ab'
        >>> strategy.d_ranking_threshold['abc']
        0.4
    """

    def __init__(self, d, ratio_optimistic=None, profile=None, voting_rule=None):
        voting_rule = self._get_voting_rule_(profile, voting_rule)
        # Prepare the dictionary of thresholds
        d_ranking_threshold = DictPrintingInOrderIgnoringNone({ranking: None for ranking in RANKINGS})
        self.d_ranking_ratio_optimistic = DictPrintingInOrderIgnoringNone({ranking: None for ranking in RANKINGS})
        for ranking, value in d.items():
            if isinstance(value, tuple):
                d_ranking_threshold[ranking], self.d_ranking_ratio_optimistic[ranking] = value
            else:
                d_ranking_threshold[ranking] = value
                self.d_ranking_ratio_optimistic[ranking] = ratio_optimistic
        # Call parent class
        super().__init__(d_ranking_threshold=d_ranking_threshold, profile=profile, voting_rule=voting_rule)

    @cached_property
    def d_ranking_t_threshold_ratio_optimistic(self):
        """dict : Thresholds and ratios of optimistic voters.

        Key : ranking, e.g. ``'abc'``. Value: tuple (``threshold``, ``ratio_optimistic``).
        """
        return DictPrintingInOrderIgnoringNone({
            ranking: (self.d_ranking_threshold[ranking], self.d_ranking_ratio_optimistic[ranking])
            for ranking in RANKINGS
        })

    def __eq__(self, other):
        """Equality test.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            True if this strategy is equal to `other`.

        Examples
        --------
            >>> strategy = StrategyThresholdMixed({'abc': (0.4, 0.2), 'bac': (0.51, 0.2), 'cab': (1, 0.2)})
            >>> strategy == StrategyThresholdMixed({'abc': (0.4, 0.2), 'bac': (0.51, 0.2), 'cab': (1, 0.2)})
            True
        """
        return (isinstance(other, StrategyThresholdMixed)
                and self.d_ranking_threshold == other.d_ranking_threshold
                and self.d_ranking_ratio_optimistic == other.d_ranking_ratio_optimistic
                and self.voting_rule == other.voting_rule)

    def isclose(self, other, *args, **kwargs):
        """Test near-equality.

        Parameters
        ----------
        other : Object
        *args
            Cf. :func:`math.isclose`.
        **kwargs
            Cf. :func:`math.isclose`.

        Returns
        -------
        isclose : bool
            True if this strategy is approximately equal to `other`.

        Examples
        --------
            >>> strategy = StrategyThresholdMixed({'abc': (0.4, 0.2), 'bac': (0.51, 0.2), 'cab': (1, 0.2)})
            >>> strategy.isclose(StrategyThresholdMixed({
            ...     'abc': (0.4, 0.2), 'bac': (0.51, 0.1999999999999), 'cab': (0.999999999999, 0.2)}))
            True
        """
        return isinstance(other, StrategyThresholdMixed) and all([
            (threshold is None and other.d_ranking_threshold[ranking] is None)
            or isclose(threshold, other.d_ranking_threshold[ranking], *args, **kwargs)
            for ranking, threshold in self.d_ranking_threshold.items()
        ]) and all([
            (ratio_optimistic is None and other.d_ranking_ratio_optimistic[ranking] is None)
            or isclose(ratio_optimistic, other.d_ranking_ratio_optimistic[ranking], *args, **kwargs)
            for ranking, ratio_optimistic in self.d_ranking_ratio_optimistic.items()
        ])

    def __repr__(self):
        arguments = repr(self.d_ranking_t_threshold_ratio_optimistic)
        if self.voting_rule != APPROVAL:
            arguments += ', voting_rule=%r' % self.voting_rule
        return 'StrategyThresholdMixed(%s)' % arguments

    def __str__(self):
        result = '<' + ', '.join([
            '%s: %s' % (ranking, self.d_ranking_ballot[ranking])
            + (' (%s, %s)' % tuple(self.d_ranking_t_threshold_ratio_optimistic[ranking])
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
