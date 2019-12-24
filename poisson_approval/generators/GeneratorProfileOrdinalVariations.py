from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal
import random


class GeneratorProfileOrdinalVariations:
    """A generator of ordinal profiles (:class:`ProfileOrdinal`) describing variations of a given base profile.

    Parameters
    ----------
    base_profile : ProfileOrdinal
        The base profile.
    epsilon : Number
        The noise.
    well_informed_voters : bool
        Cf. the corresponding parameter in :class:`ProfileOrdinal`.

    Notes
    -----
    We add ``epsilon * random()`` to each component of the base profile. Then we normalize to have a sum of 1.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> base_profile = ProfileOrdinal({'abc': 0.25, 'bac': 0.75})
        >>> generator = GeneratorProfileOrdinalVariations(base_profile, epsilon=0.01)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.25043511946419417, acb: 0.007344656519664636, bac: 0.7308331353826986, bca: 0.002508930076416972, \
cab: 0.004954304904190167, cba: 0.003923853652835374> (Condorcet winner: b)
    """

    def __init__(self, base_profile, epsilon, well_informed_voters=True):
        self.well_informed_voters = well_informed_voters
        self.base_profile = base_profile
        self.epsilon = epsilon

    def __call__(self):
        """
        :return: a profile
        """
        return ProfileOrdinal({ranking: self.base_profile.d_ranking_share[ranking] + self.epsilon * random.random()
                               for ranking in RANKINGS},
                              normalization_warning=False,
                              well_informed_voters=self.well_informed_voters)
