from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.strategies.StrategyTwelve import StrategyTwelve
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros


# noinspection PyUnresolvedReferences
class StrategyThreshold(StrategyTwelve):
    """A strategy profile for a cardinal profile.

    Parameters
    ----------
    d_ranking_threshold : dict
        Keys are rankings and values are utility thresholds. E.g. ``'abc': 0.4`` means that a voter ``abc`` vote for
        ``ab`` if her utility for ``b`` is strictly greater than 0.4, and for ``a`` otherwise. A threshold can be
        ``None``, meaning that the behavior of these voters is not specified in the strategy.
    profile : Profile, optional
        The "context" in which the strategy is used.

    Examples
    --------
        >>> sigma = StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 1})
        >>> sigma
        StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 1})
        >>> print(sigma)
        <abc: utility-dependent (0.4), bac: utility-dependent (0.51), cab: c>
        >>> sigma.abc
        'utility-dependent'
        >>> sigma.a_bc
        'a'
        >>> sigma.ab_c
        'ab'
        >>> sigma.d_ranking_threshold['abc']
        0.4
    """

    def __init__(self, d_ranking_threshold=None, profile=None):
        # Populate the dictionary of thresholds
        if d_ranking_threshold is None:
            d_ranking_threshold = dict()
        self.d_ranking_threshold = DictPrintingInOrderIgnoringZeros(d_ranking_threshold)
        for ranking in RANKINGS:
            if ranking not in self.d_ranking_threshold:
                self.d_ranking_threshold[ranking] = None
        # Prepare the dictionary of ballots
        d_ranking_ballot = DictPrintingInOrderIgnoringZeros()
        for ranking, threshold in self.d_ranking_threshold.items():
            if threshold is None:
                d_ranking_ballot[ranking] = ''
            elif threshold == 1:
                d_ranking_ballot[ranking] = ranking[0]
            elif threshold == 0:
                d_ranking_ballot[ranking] = ranking[:2]
            else:
                d_ranking_ballot[ranking] = UTILITY_DEPENDENT
        # Call parent class
        super().__init__(d_ranking_ballot=d_ranking_ballot, profile=profile)

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
            >>> sigma = StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 1})
            >>> sigma == StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 1})
            True
        """
        return isinstance(other, StrategyThreshold) and self.d_ranking_threshold == other.d_ranking_threshold

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
            >>> sigma = StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 1})
            >>> sigma.isclose(StrategyThreshold({'abc': 0.4, 'bac': 0.51, 'cab': 0.999999999999999999999999}))
            True
        """
        return isinstance(other, StrategyThreshold) and all([
            (threshold is None and other.d_ranking_threshold[ranking] is None)
            or isclose(threshold, other.d_ranking_threshold[ranking], *args, **kwargs)
            for ranking, threshold in self.d_ranking_threshold.items()
        ])

    def __repr__(self):
        return 'StrategyThreshold(%r)' % self.d_ranking_threshold

    def __str__(self):
        result = '<' + ', '.join([
            '%s: %s' % (ranking, self.d_ranking_ballot[ranking])
            + (' (%s)' % self.d_ranking_threshold[ranking]
               if self.d_ranking_ballot[ranking] == UTILITY_DEPENDENT else '')
            for ranking in sorted(self.d_ranking_ballot) if self.d_ranking_ballot[ranking]
        ]) + '>'
        if self.profile is not None:
            result += ' ==> ' + str(self.winners)
        return result

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')
