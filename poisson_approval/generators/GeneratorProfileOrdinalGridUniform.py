from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex_grid
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class GeneratorProfileOrdinalGridUniform:
    """A generator of ordinal profiles (:class:`ProfileOrdinal`), uniform on a grid.

    Parameters
    ----------
    denominator : int
        The coefficients of the profile will be fractions with this denominator.
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`ProfileOrdinal`.

    Notes
    -----
    The profile is drawn uniformly on the points of the simplex whose coordinates are fractions with the given
    denominator.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileOrdinalGridUniform(denominator=100, well_informed_voters=False)
        >>> profile = generator()
        >>> print(profile)
        <abc: 1/50, acb: 23/100, bac: 17/50, cab: 11/50, cba: 19/100> (badly informed voters)
        >>> profile.well_informed_voters
        False
    """

    def __init__(self, denominator, **kwargs):
        self.denominator = denominator
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        ProfileOrdinal
            A profile.
        """
        x = rand_simplex_grid(d=6, denominator=self.denominator)
        return ProfileOrdinal({ranking: x[i] for i, ranking in enumerate(RANKINGS)},
                              **self.kwargs)
