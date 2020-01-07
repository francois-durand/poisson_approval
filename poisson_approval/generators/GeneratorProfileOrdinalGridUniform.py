from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex_grid
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class GeneratorProfileOrdinalGridUniform:
    """A generator of ordinal profiles (:class:`ProfileOrdinal`), uniform on a grid.

    Parameters
    ----------
    denominator : int
        The coefficients of the profile will be fractions with this denominator.
    well_informed_voters : bool
        Cf. the corresponding parameter in :class:`ProfileOrdinal`.

    Notes
    -----
    The profile is drawn uniformly on the points of the simplex whose coordinates are fractions with the given
    denominator.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileOrdinalGridUniform(denominator=100)
        >>> profile = generator()
        >>> print(profile)
        <abc: 1/50, acb: 23/100, bac: 17/50, cab: 11/50, cba: 19/100>
    """

    def __init__(self, denominator, well_informed_voters=True):
        self.denominator = denominator
        self.well_informed_voters = well_informed_voters

    def __call__(self):
        """
        Returns
        -------
        ProfileOrdinal
            A profile.
        """
        x = rand_simplex_grid(d=6, denominator=self.denominator)
        return ProfileOrdinal({ranking: x[i] for i, ranking in enumerate(RANKINGS)},
                              well_informed_voters=self.well_informed_voters)
