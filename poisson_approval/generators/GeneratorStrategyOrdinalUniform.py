import random
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds, ballot_one, ballot_one_two
from poisson_approval.strategies.StrategyOrdinal import StrategyOrdinal


class GeneratorStrategyOrdinalUniform:
    """A generator of ordinal strategies (:class:`StrategyOrdinal`) following the uniform distribution.

    Notes
    -----
    Each ballot is chosen at random: either the top candidate or the two top candidates.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorStrategyOrdinalUniform()
        >>> strategy = generator()
        >>> print(strategy)
        <abc: ab, acb: ac, bac: b, bca: bc, cab: ac, cba: bc>
    """

    def __call__(self):
        """
        Returns
        -------
        StrategyOrdinal
            A strategy.
        """
        return StrategyOrdinal(d_ranking_ballot={
            ranking: random.choice([ballot_one(ranking), ballot_one_two(ranking)])
            for ranking in RANKINGS})
