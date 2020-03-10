from poisson_approval.constants.constants import *
from poisson_approval.iterables.IterableSimplexGrid import IterableSimplexGrid
from poisson_approval.tau_vector.TauVector import TauVector


class IterableTauVectorGrid:
    """Iterate over tau-vectors (:class:`TauVector`) defined on a grid.

    Parameters
    ----------
    denominator : int or iterable
        The grain(s) of the grid.
    ballots : iterable, optional
        These ballots (e.g. ``'a'``, ``'ab'``) will have a variable share. Default: all ballots.
    d_ballot_fixed_share : dict, optional
        A dictionary. For each entry ``ballot: fixed_share``, this ballot will have at least this fixed share. The total
        must be lower or equal to 1.
    standardized : bool, optional
        If True, then only standardized tau-vectors are given. Cf. :meth:`TauVector.is_standardized`. You should
        probably use this option if the arguments `ballots`, `d_ballot_fixed_share` and `test` treat the candidates
        symmetrically.
    test : callable, optional
        A function ``TauVector -> bool``. Only tau-vector meeting this test are given.
    kwargs
        Additional parameters are passed to `TauVector` when creating the tau-vector.

    Examples
    --------
    Basic usage:

        >>> for tau in IterableTauVectorGrid(denominator=2, standardized=True):
        ...     print(tau)
        <a: 1> ==> a
        <a: 1/2, b: 1/2> ==> a, b
        <a: 1/2, ab: 1/2> ==> a
        <a: 1/2, bc: 1/2> ==> a, b, c
        <ab: 1> ==> a, b
        <ab: 1/2, ac: 1/2> ==> a

    For more examples, cf. :class:`IterableSimplexGrid`.
    """
    def __init__(self, denominator, ballots=None, d_ballot_fixed_share=None, standardized=False, test=None, **kwargs):
        if ballots is None:
            ballots = BALLOTS_WITHOUT_INVERSIONS
        self.standardized = standardized
        self._base_iterator = IterableSimplexGrid(cls=TauVector, denominator=denominator, keys=ballots,
                                                  d_key_fixed_share=d_ballot_fixed_share, test=test, **kwargs)

    def __iter__(self):
        return (profile for profile in self._base_iterator
                if not self.standardized or profile.is_standardized)
