from poisson_approval.utils.Util import sort_ballot
from poisson_approval.constants.constants import *
from poisson_approval.strategies.Strategy import Strategy
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros


# noinspection PyUnresolvedReferences
class StrategyTwelve(Strategy):
    """A strategy profile for a 12-type profile.

    Parameters
    ----------
    d_ranking_ballot : dict
        Keys are rankings and values are strategies, e.g. ``'abc': 'ab'``. A strategy can be a valid ballot
        (e.g. ``'a'`` or ``'ab'`` when the ranking is ``'abc'``), ``UTILITY_DEPENDENT`` or ``''`` if the behavior
        of these voters is not specified in the strategy. Cf. :class:`ProfileTwelve`.
    profile : Profile, optional
        The "context" in which the strategy is used.

    Examples
    --------
        >>> sigma = StrategyTwelve({'abc': 'utility-dependent', 'bac': 'b'})
        >>> sigma
        StrategyTwelve({'abc': 'utility-dependent', 'bac': 'b'})
        >>> print(sigma)
        <abc: utility-dependent, bac: b>
        >>> sigma.abc
        'utility-dependent'
        >>> sigma.a_bc
        'a'
        >>> sigma.ab_c
        'ab'
    """

    def __init__(self, d_ranking_ballot=None, profile=None):
        # Populate the dictionary and check for typos in the input
        if d_ranking_ballot is None:
            d_ranking_ballot = dict()
        self.d_ranking_ballot = DictPrintingInOrderIgnoringZeros()
        for ranking, ballot in d_ranking_ballot.items():
            if ranking not in RANKINGS:
                raise ValueError('Unknown key: ' + ranking)
            strategy_1 = ranking[0]
            strategy_12 = ranking[:2]
            strategy_21 = ranking[1::-1]
            if ballot not in ['', strategy_1, strategy_12, strategy_21, UTILITY_DEPENDENT]:
                raise ValueError('Unknown strategy: ' + ballot)
            if ballot == UTILITY_DEPENDENT:
                self.d_ranking_ballot[ranking] = ballot
            else:
                self.d_ranking_ballot[ranking] = ''.join(sorted(ballot))
        for ranking in RANKINGS:
            if ranking not in self.d_ranking_ballot:
                self.d_ranking_ballot[ranking] = ''
        # Call parent class
        super().__init__(profile=profile)

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
            >>> sigma = StrategyTwelve({'abc': 'utility-dependent', 'bac': 'b'})
            >>> sigma == StrategyTwelve({'abc': 'utility-dependent', 'bac': 'b'})
            True
        """
        return isinstance(other, StrategyTwelve) and self.d_ranking_ballot == other.d_ranking_ballot

    # Representation

    def __repr__(self):
        return 'StrategyTwelve(%r)' % self.d_ranking_ballot

    def __str__(self):
        result = '<%s>' % str(self.d_ranking_ballot)[1:-1]
        if self.profile is not None:
            result += ' ==> ' + str(self.winners)
        return result

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')


def make_property_ranking_ballot(ranking, doc):
    def _f(self):
        return self.d_ranking_ballot[ranking]
    _f.__doc__ = doc
    return property(_f)


for my_ranking in RANKINGS:
    setattr(StrategyTwelve, my_ranking, make_property_ranking_ballot(my_ranking,
                                                                     'str : Ballot of ranking ``%s``.' % my_ranking))


def make_property_ranking_low_u_ballot(ranking, doc):
    def _f(self):
        return ranking[0] if getattr(self, ranking) == UTILITY_DEPENDENT else getattr(self, ranking)
    _f.__doc__ = doc
    return property(_f)


for my_ranking in RANKINGS:
    my_t = my_ranking[0] + '_' + my_ranking[1:]
    setattr(StrategyTwelve, my_t, make_property_ranking_low_u_ballot(my_ranking,
                                                                     'str : Ballot of type ``%s``.' % my_t))


def make_property_ranking_high_u_ballot(ranking, doc):
    def _f(self):
        return sort_ballot(ranking[:2]) if getattr(self, ranking) == UTILITY_DEPENDENT else getattr(self, ranking)
    _f.__doc__ = doc
    return property(_f)


for my_ranking in RANKINGS:
    my_t = my_ranking[:2] + '_' + my_ranking[2]
    setattr(StrategyTwelve, my_t, make_property_ranking_high_u_ballot(my_ranking,
                                                                      'str : Ballot of type ``%s``.' % my_t))
