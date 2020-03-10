from poisson_approval.constants.constants import *
from poisson_approval.iterators.IterableSimplexGrid import IterableSimplexGrid
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class IterableProfileOrdinalGrid:
    """

    Parameters
    ----------
    denominator
    orders
    d_order_fixed_share
    standardized
    test
    kwargs

    Returns
    -------

    Examples
    --------
        >>> for profile in IterableProfileOrdinalGrid(denominator=3):
        ...     print(profile)
        <abc: 1> (Condorcet winner: a)
        <abc: 2/3, acb: 1/3> (Condorcet winner: a)
        <abc: 2/3, bac: 1/3> (Condorcet winner: a)
        <abc: 2/3, bca: 1/3> (Condorcet winner: a)
        <abc: 2/3, cab: 1/3> (Condorcet winner: a)
        <abc: 2/3, cba: 1/3> (Condorcet winner: a)
        <abc: 1/3, acb: 1/3, bac: 1/3> (Condorcet winner: a)
        <abc: 1/3, acb: 1/3, bca: 1/3> (Condorcet winner: a)
        <abc: 1/3, bac: 1/3, cab: 1/3> (Condorcet winner: a)
        <abc: 1/3, bca: 1/3, cab: 1/3>

        >>> def test_not_condorcet(profile):
        ...     return profile.is_profile_condorcet == 0.0
        >>> for profile in IterableProfileOrdinalGrid(denominator=3, test=test_not_condorcet):
        ...     print(profile)
        <abc: 1/3, bca: 1/3, cab: 1/3>
    """
    def __init__(self, denominator, orders=None, d_order_fixed_share=None, standardized=True, test=None, **kwargs):
        if orders is None:
            orders = RANKINGS
        self.standardized = standardized
        self._base_iterator = IterableSimplexGrid(cls=ProfileOrdinal, denominator=denominator, keys=orders,
                                                  d_key_fixed_share=d_order_fixed_share, test=test, **kwargs)

    def __iter__(self):
        return (profile for profile in self._base_iterator
                if not self.standardized or profile.is_standardized)
