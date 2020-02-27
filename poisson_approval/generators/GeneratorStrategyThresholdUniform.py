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
    Each threshold and each ratio of optimistic voters is drawn uniformly in the interval [0, 1].

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorStrategyThresholdUniform()
        >>> strategy = generator()
        >>> print(strategy)
        <abc: utility-dependent (0.5488135039273248, 0.7151893663724195), \
acb: utility-dependent (0.6027633760716439, 0.5448831829968969), \
bac: utility-dependent (0.4236547993389047, 0.6458941130666561), \
bca: utility-dependent (0.4375872112626925, 0.8917730007820798), \
cab: utility-dependent (0.9636627605010293, 0.3834415188257777), \
cba: utility-dependent (0.7917250380826646, 0.5288949197529045)>
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
        return StrategyThreshold({ranking: (np.random.rand(), np.random.rand())
                                  for ranking in RANKINGS}, **self.kwargs)
