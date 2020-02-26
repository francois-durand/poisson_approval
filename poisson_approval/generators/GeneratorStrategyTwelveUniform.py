import random
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, ballot_one, ballot_one_two
from poisson_approval.strategies.StrategyTwelve import StrategyTwelve


class GeneratorStrategyTwelveUniform:
    """A generator of strategies for twelve types (:class:`StrategyTwelve`) following the uniform distribution.

    Parameters
    ----------
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`StrategyTwelve`.

    Notes
    -----
    Each ballot is chosen at random: either the top candidate, or the two top candidates, or utility-dependent.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorStrategyTwelveUniform()
        >>> strategy = generator()
        >>> print(strategy)
        <abc: ab, acb: ac, bac: b, bca: bc, cab: utility-dependent, cba: bc>
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self):
        """
        Returns
        -------
        StrategyTwelve
            A strategy.
        """
        return StrategyTwelve(d_ranking_ballot={
            ranking: random.choice([ballot_one(ranking), ballot_one_two(ranking), UTILITY_DEPENDENT])
            for ranking in RANKINGS}, **self.kwargs)
