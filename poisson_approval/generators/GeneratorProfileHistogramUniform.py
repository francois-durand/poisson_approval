from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex
from poisson_approval.profiles.ProfileHistogram import ProfileHistogram


class GeneratorProfileHistogramUniform:
    """A generator of histogram-profiles (:class:`ProfileHistogram`) following the uniform distribution.

    Parameters
    ----------
    n_bins : int
        The numbers of bins for each histogram.

    Notes
    -----
    The ordinal profile is drawn uniformly on the simplex. Then each histogram is drawn uniformly on the simplex.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileHistogramUniform(n_bins=3)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.4236547993389047 [0.43758721 0.2083069  0.35410589], \
acb: 0.12122838365799216 [0.891773   0.07188976 0.03633724], \
bac: 0.0039303209304278885 [0.38344152 0.40828352 0.20827496], \
bca: 0.05394987214431912 [0.52889492 0.03914964 0.43195544], \
cab: 0.1124259903007756 [0.07103606 0.85456058 0.07440336], \
cba: 0.2848106336275805 [0.0202184 0.0669109 0.9128707]> (Condorcet winner: a)
    """

    def __init__(self, n_bins):
        self.n_bins = n_bins

    def __call__(self):
        """
        :return: a profile.
        """
        x = rand_simplex(d=6)
        return ProfileHistogram({ranking: x[i] for i, ranking in enumerate(RANKINGS)},
                                {ranking: rand_simplex(d=self.n_bins) for ranking in RANKINGS})
