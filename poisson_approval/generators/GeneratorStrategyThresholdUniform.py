import numpy as np
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold


class GeneratorStrategyThresholdUniform:
    """A generator of threshold strategies (:class:`StrategyThreshold`) following the uniform distribution.

    Parameters
    ----------
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`StrategyThreshold`.

    Notes
    -----
    Each threshold is drawn uniformly in the interval [0, 1].

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorStrategyThresholdUniform()
        >>> strategy = generator()
        >>> print(strategy)
        <abc: utility-dependent (0.5488135039273248), acb: utility-dependent (0.7151893663724195), \
bac: utility-dependent (0.6027633760716439), bca: utility-dependent (0.5448831829968969), \
cab: utility-dependent (0.4236547993389047), cba: utility-dependent (0.6458941130666561)>
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        StrategyThreshold
            A strategy.
        """
        return StrategyThreshold({ranking: np.random.rand() for ranking in RANKINGS}, **self.kwargs)
