from poisson_approval import NiceStatsProfileOrdinal, initialize_random_seeds, ProfileOrdinal


def test():
    # Test when rejection is indeed necessary.
    initialize_random_seeds()
    nice_stats = NiceStatsProfileOrdinal(
        tests_profile=[
            (lambda profile: any([strategy for strategy in profile.analyzed_strategies_ordinal.equilibria
                                  if strategy.profile.condorcet_winners == strategy.winners]),
             'There exists a true equilibrium electing the CW'),
        ],
        conditional_on=lambda profile: profile.has_majority_ranking)
    nice_stats.run(n_samples=2)
    profile = nice_stats.find_example(0, False)
    assert isinstance(profile, ProfileOrdinal)
