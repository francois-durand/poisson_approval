from poisson_approval import ProfileDiscrete


def test_main_init():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, symbolic=True)
        >>> print(profile)
        <abc 3/10: 13/50, abc 4/5: 53/100, bac 1/10: 21/100> (Condorcet winner: a)

        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     'abc': {Fraction(3, 10): Fraction(26, 100), Fraction(8, 10): Fraction(53, 100)},
        ...     'bac': {Fraction(1, 10): Fraction(21, 100)}
        ... }, symbolic=True)
        >>> print(profile)
        <abc 3/10: 13/50, abc 4/5: 53/100, bac 1/10: 21/100> (Condorcet winner: a)
    """
    pass


def test_main_operations():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, symbolic=True)
        >>> profile
        ProfileDiscrete({'abc': {Fraction(3, 10): Fraction(13, 50), Fraction(4, 5): Fraction(53, 100)}, \
'bac': {Fraction(1, 10): Fraction(21, 100)}})
        >>> profile.d_ranking_share
        {'abc': Fraction(79, 100), 'bac': Fraction(21, 100)}
        >>> profile.abc
        Fraction(79, 100)
        >>> profile.have_ranking_with_utility_above_u('abc', Fraction(1, 2))
        Fraction(53, 100)
        >>> profile.have_ranking_with_utility_below_u('abc', Fraction(1, 2))
        Fraction(13, 50)
        >>> profile.have_ranking_with_utility_u('abc', Fraction(3, 10))
        Fraction(13, 50)
        >>> profile.analyzed_strategies_pure
        Equilibrium:
        <abc: a, bac: b> ==> a (FF)
        <BLANKLINE>
        Non-equilibria:
        <abc: ab, bac: ab> ==> a, b (FF)
        <abc: ab, bac: b> ==> b (FF)
        <abc: utility-dependent (11/20), bac: ab> ==> a (FF)
        <abc: utility-dependent (11/20), bac: b> ==> a (FF)
        <abc: a, bac: ab> ==> a (FF)
        >>> print(profile.analyzed_strategies_pure.winners_at_equilibrium)
        a
    """
    pass


def test_main_weak_orders():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({('abc', Fraction(3, 10)): Fraction(26, 100), ('bac', Fraction(1, 10)): Fraction(21, 100)},
        ...                           d_weak_order_share={'a~b>c': Fraction(53, 100)}, symbolic=True)
        >>> profile
        ProfileDiscrete({'abc': {Fraction(3, 10): Fraction(13, 50)}, 'bac': {Fraction(1, 10): Fraction(21, 100)}}, \
d_weak_order_share={'a~b>c': Fraction(53, 100)})
        >>> print(profile)
        <abc 3/10: 13/50, bac 1/10: 21/100, a~b>c: 53/100> (Condorcet winner: a)
    """
    pass


def test_repr():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10), symbolic=True)
        >>> profile
        ProfileDiscrete({'abc': {Fraction(3, 10): Fraction(13, 50), Fraction(4, 5): Fraction(53, 100)}, \
'bac': {Fraction(1, 10): Fraction(21, 100)}}, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5))
    """
    pass


def test_str():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10), symbolic=True)
        >>> print(profile)
        <abc 3/10: 13/50, abc 4/5: 53/100, bac 1/10: 21/100> (Condorcet winner: a) (ratio_sincere: 1/10) \
(ratio_fanatic: 1/5)
    """
    pass


def test_eq():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, symbolic=True)
        >>> profile == ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, symbolic=True)
        True
    """
    pass


def test_standardized_version():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileDiscrete({
        ...     ('abc', Fraction(3, 10)): Fraction(26, 100),
        ...     ('abc', Fraction(8, 10)): Fraction(53, 100),
        ...     ('bac', Fraction(1, 10)): Fraction(21, 100)
        ... }, symbolic=True)
        >>> print(profile.standardized_version)
        <abc 3/10: 13/50, abc 4/5: 53/100, bac 1/10: 21/100> (Condorcet winner: a)
        >>> profile.is_standardized
        True
    """
    pass
