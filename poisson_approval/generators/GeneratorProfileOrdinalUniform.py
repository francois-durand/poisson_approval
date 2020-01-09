from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class GeneratorProfileOrdinalUniform:
    """A generator of ordinal profiles (:class:`ProfileOrdinal`) following the uniform distribution.

    Parameters
    ----------
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`ProfileOrdinal`.

    Notes
    -----
    The profile is drawn uniformly on the simplex.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileOrdinalUniform(well_informed_voters=True)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.4236547993389047, acb: 0.12122838365799216, bac: 0.0039303209304278885, bca: 0.05394987214431912, \
cab: 0.1124259903007756, cba: 0.2848106336275805> (Condorcet winner: a)
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        ProfileOrdinal
            A profile.
        """
        x = rand_simplex(d=6)
        return ProfileOrdinal({ranking: x[i] for i, ranking in enumerate(RANKINGS)},
                              **self.kwargs)
