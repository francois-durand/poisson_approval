from poisson_approval import ProfileDiscrete, PLURALITY, ANTI_PLURALITY


def test_normalization():
    profile = ProfileDiscrete({('abc', 0.2): 1, ('acb', 0.4): 1})
    assert profile.abc == 0.5


def test_plurality():
    """
        >>> profile = ProfileDiscrete({('abc', 0.2): 1, ('acb', 0.4): 1}, voting_rule=PLURALITY)
        >>> profile
        ProfileDiscrete({'abc': {0.2: 0.5}, 'acb': {0.4: 0.5}}, voting_rule='Plurality')
        >>> print(profile)
        <abc 0.2: 0.5, acb 0.4: 0.5> (Condorcet winner: a) (Plurality)
    """
    pass


def test_anti_plurality():
    """
        >>> profile = ProfileDiscrete({('abc', 0.2): 1, ('acb', 0.4): 1}, voting_rule=ANTI_PLURALITY)
        >>> profile
        ProfileDiscrete({'abc': {0.2: 0.5}, 'acb': {0.4: 0.5}}, voting_rule='Anti-plurality')
        >>> print(profile)
        <abc 0.2: 0.5, acb 0.4: 0.5> (Condorcet winner: a) (Anti-plurality)
    """
    pass
