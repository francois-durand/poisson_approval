from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex_grid
from poisson_approval.tau_vector.TauVector import TauVector


class GeneratorTauVectorGridUniform:
    """A generator of tau-vectors (:class:`TauVector`), uniform on a grid.

    Parameters
    ----------
    denominator : int
        The coefficients of the tau-vector will be fractions with this denominator.
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`TauVector`.

    Notes
    -----
    The tau-vector is drawn uniformly on the points of the simplex whose coordinates are fractions with the given
    denominator.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorTauVectorGridUniform(denominator=100)
        >>> tau = generator()
        >>> print(tau)
        <a: 1/50, ac: 11/50, b: 23/100, bc: 19/100, c: 17/50> ==> c
    """

    def __init__(self, denominator, **kwargs):
        self.denominator = denominator
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        TauVector
            A tau-vector.
        """
        x = rand_simplex_grid(d=6, denominator=self.denominator)
        return TauVector({ballot: x[i] for i, ballot in enumerate(BALLOTS_WITHOUT_INVERSIONS)}, **self.kwargs)
