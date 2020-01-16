from poisson_approval import ProfileOrdinal, StrategyOrdinal, EquilibriumStatus


def test():
    profile = ProfileOrdinal({'abc': 0.5, 'acb': 0.5})
    strategy = StrategyOrdinal({'abc': 'a'})
    assert profile.is_equilibrium(strategy) == EquilibriumStatus.INCONCLUSIVE
