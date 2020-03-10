from poisson_approval.constants.constants import *
from poisson_approval.generators.GeneratorSimplexUniform import GeneratorSimplexUniform
from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class GeneratorProfileOrdinalUniform(GeneratorSimplexUniform):
    """A generator of ordinal profiles (:class:`ProfileOrdinal`) following the uniform distribution.

    Parameters
    ----------
    orders : list, optional
        A list of orders, e.g. ``'abc'`` or ``'a>b~c'``. These orders will have a variable share, drawn at random.
        Default: all strict orders.
    d_order_fixed_share : dict, optional.
        Key: order. Value: a share of voters. These shares are fixed.
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`ProfileOrdinal`.

    Notes
    -----
    Cf. :class:`GeneratorSimplexUniform`.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileOrdinalUniform(well_informed_voters=True)
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.4236547993389047, acb: 0.12122838365799216, bac: 0.0039303209304278885, bca: 0.05394987214431912, \
cab: 0.1124259903007756, cba: 0.2848106336275805> (Condorcet winner: a)

        >>> generator = GeneratorProfileOrdinalUniform(
        ...     orders=['abc', 'acb'], d_order_fixed_share={'acb': 0.8, 'a~b>c': 0.1})
        >>> profile = generator()
        >>> print(profile)
        <abc: 0.0645894113066656, acb: 0.8354105886933344, a~b>c: 0.1> (Condorcet winner: a)
    """

    def __init__(self, orders=None, d_order_fixed_share=None, **kwargs):
        if orders is None:
            orders = RANKINGS
        super().__init__(cls=ProfileOrdinal, keys=orders, d_key_fixed_share=d_order_fixed_share, **kwargs)
