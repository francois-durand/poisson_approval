from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.generators.GeneratorSimplexGridUniform import GeneratorSimplexGridUniform
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal


class GeneratorProfileOrdinalGridUniform(GeneratorSimplexGridUniform):
    """A generator of ordinal profiles (:class:`ProfileOrdinal`), uniform on a grid.

    Parameters
    ----------
    denominator : int
        The coefficients of the profile will be fractions with this denominator.
    orders : list, optional
        A list of orders, e.g. ``'abc'`` or ``'a>b~c'``. These orders will have a variable share, drawn at random.
        Default: all strict orders.
    d_order_fixed_share : dict, optional.
        Key: order. Value: a share of voters. These shares are fixed.
    kwargs : keyword arguments
        These additional arguments will be passed directly to :class:`ProfileOrdinal`.

    Notes
    -----
    Cf. :class:`GeneratorSimplexGridUniform`.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> generator = GeneratorProfileOrdinalGridUniform(denominator=100, well_informed_voters=False)
        >>> profile = generator()
        >>> print(profile)
        <abc: 1/50, acb: 23/100, bac: 17/50, cab: 11/50, cba: 19/100> (badly informed voters)
        >>> profile.well_informed_voters
        False

        >>> from fractions import Fraction
        >>> generator = GeneratorProfileOrdinalGridUniform(
        ...     denominator=70, orders=['abc', 'acb'],
        ...     d_order_fixed_share={'bac': Fraction(17, 100), 'a~b>c': Fraction(13, 100)})
        >>> profile = generator()
        >>> print(profile)
        <abc: 33/50, acb: 1/25, bac: 17/100, a~b>c: 13/100> (Condorcet winner: a)
    """

    def __init__(self, denominator, orders=None, d_order_fixed_share=None, **kwargs):
        if orders is None:
            orders = RANKINGS
        super().__init__(cls=ProfileOrdinal, denominator=denominator, keys=orders,
                         d_key_fixed_share=d_order_fixed_share, **kwargs)
