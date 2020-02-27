from poisson_approval import StrategyThresholdOptimistic, PLURALITY, ANTI_PLURALITY, UTILITY_DEPENDENT


def test_strategy_threshold_plurality():
    """
        >>> strategy = StrategyThresholdOptimistic({'abc': 0.7, 'bac': 1, 'cba': 0}, voting_rule=PLURALITY)
        >>> strategy
        StrategyThresholdOptimistic({'abc': 0.7, 'bac': 1, 'cba': 0}, voting_rule='Plurality')
        >>> print(strategy)
        <abc: utility-dependent (0.7), bac: b, cba: b> (Plurality)
        >>> strategy.a_bc
        'a'
        >>> strategy.ab_c
        'b'
    """
    pass


def test_strategy_threshold_anti_plurality():
    """
        >>> strategy = StrategyThresholdOptimistic({'abc': 0.7, 'bac': 1, 'cba': 0}, voting_rule=ANTI_PLURALITY)
        >>> strategy
        StrategyThresholdOptimistic({'abc': 0.7, 'bac': 1, 'cba': 0}, voting_rule='Anti-plurality')
        >>> print(strategy)
        <abc: utility-dependent (0.7), bac: bc, cba: bc> (Anti-plurality)
        >>> strategy.a_bc
        'ac'
        >>> strategy.ab_c
        'ab'
    """
    pass
