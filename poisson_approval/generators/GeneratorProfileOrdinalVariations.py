from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal
import random


class GeneratorProfileOrdinalVariations:
    """A generator of ordinal profiles describing variations of a given base profile.

    :param base_profile: a :class:``ProfileOrdinal``.
    :param epsilon: the noise.
    :param well_informed_voters: cf. :class:`ProfileOrdinal`.

    We add ``epsilon * random()`` to each component of the base profile. Then we normalize to have a sum of 1.

        >>> initialize_random_seeds()
        >>> base_profile = ProfileOrdinal({'abc': 0.25, 'bac': 0.75})
        >>> generator = GeneratorProfileOrdinalVariations(base_profile, epsilon=0.01)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.25043511946419417, acb: 0.004075382095746225, bac: 0.7341024098066171, bca: 0.002508930076416973, \
cab: 0.004954304904190168, cba: 0.003923853652835375> (Condorcet winner: b)
    """

    def __init__(self, base_profile, epsilon, well_informed_voters=True):
        self.well_informed_voters = well_informed_voters
        self.base_profile = base_profile
        self.epsilon = epsilon

    def __call__(self):
        """
        :return: a profile
        """
        return ProfileOrdinal({ranking: share + self.epsilon * random.random()
                               for ranking, share in self.base_profile.d_ranking_share.items()},
                              normalization_warning=False,
                              well_informed_voters=self.well_informed_voters)
