from poisson_approval import StrategyTwelve, PLURALITY, ANTI_PLURALITY, UTILITY_DEPENDENT


def test_strategy_twelve_plurality():
    """
        >>> strategy = StrategyTwelve({'abc': UTILITY_DEPENDENT, 'cba': 'b'}, voting_rule=PLURALITY)
        >>> strategy
        StrategyTwelve({'abc': 'utility-dependent', 'cba': 'b'}, voting_rule='Plurality')
        >>> print(strategy)
        <abc: utility-dependent, cba: b> (Plurality)
        >>> strategy.a_bc
        'a'
        >>> strategy.ab_c
        'b'
    """
    pass


def test_strategy_twelve_anti_plurality():
    """
        >>> strategy = StrategyTwelve({'abc': UTILITY_DEPENDENT, 'cba': 'bc'}, voting_rule=ANTI_PLURALITY)
        >>> strategy
        StrategyTwelve({'abc': 'utility-dependent', 'cba': 'bc'}, voting_rule='Anti-plurality')
        >>> print(strategy)
        <abc: utility-dependent, cba: bc> (Anti-plurality)
        >>> strategy.a_bc
        'ac'
        >>> strategy.ab_c
        'ab'
    """
    pass
