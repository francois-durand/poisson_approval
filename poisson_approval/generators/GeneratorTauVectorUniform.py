from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, rand_simplex
from poisson_approval.tau_vector.TauVector import TauVector


class GeneratorTauVectorUniform:
    """A generator of tau-vectors (:class:`TauVector`) following the uniform distribution.

    Parameters
    ----------
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`TauVector`.

    Notes
    -----
    The tau-vector is drawn uniformly on the simplex.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorTauVectorUniform()
        >>> tau = generator()
        >>> print(tau)
        <a: 0.4236547993389047, ab: 0.05394987214431912, ac: 0.1124259903007756, b: 0.12122838365799216, \
bc: 0.2848106336275805, c: 0.0039303209304278885> ==> a
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        TauVector
            A tau-vector.
        """
        x = rand_simplex(d=6)
        return TauVector({ballot: x[i] for i, ballot in enumerate(BALLOTS_WITHOUT_INVERSIONS)}, **self.kwargs)
