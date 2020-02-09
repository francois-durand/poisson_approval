from random import randint
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex
from poisson_approval.profiles.ProfileHistogram import ProfileHistogram


class GeneratorProfileHistogramSinglePeakedUniform:
    """A generator of single-peaked histogram-profiles (:class:`ProfileHistogram`) following the uniform distribution.

    Parameters
    ----------
    n_bins : int
        The numbers of bins for each histogram.
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`ProfileHistogram`.

    Notes
    -----
    A candidate at random is chosen to be in the middle of the political axis. Then the ordinal profile is drawn
    uniformly on the simplex of the four possible rankings. Then each histogram is drawn uniformly on the simplex.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileHistogramSinglePeakedUniform(n_bins=3)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.5488135039273248 [0.4236548  0.12122838 0.45511682], \
bac: 0.05394987214431912 [0.43758721 0.2083069  0.35410589], \
bca: 0.1124259903007756 [0.891773   0.07188976 0.03633724], \
cba: 0.2848106336275805 [0.38344152 0.40828352 0.20827496]> (Condorcet winner: a)
    """

    def __init__(self, n_bins, **kwargs):
        self.n_bins = n_bins
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        ProfileHistogram
            A profile.
        """
        d_i_rankings = {
            0: ['abc', 'acb', 'bac', 'cab'],
            1: ['abc', 'bac', 'bca', 'cba'],
            2: ['acb', 'bca', 'cab', 'cba']
        }
        rankings = d_i_rankings[randint(0, 2)]
        x = rand_simplex(d=4)
        return ProfileHistogram({ranking: x[i] for i, ranking in enumerate(rankings)},
                                {ranking: rand_simplex(d=self.n_bins) for ranking in rankings},
                                **self.kwargs)
