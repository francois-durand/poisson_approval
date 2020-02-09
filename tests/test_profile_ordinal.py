from poisson_approval import ProfileOrdinal, PLURALITY, ANTI_PLURALITY


def test_normalization():
    profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1})
    assert profile.abc == 0.5


def test_plurality():
    """
        >>> profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1}, voting_rule=PLURALITY)
        >>> profile
        ProfileOrdinal({'abc': 0.5, 'acb': 0.5}, voting_rule='Plurality')
        >>> print(profile)
        <abc: 0.5, acb: 0.5> (Condorcet winner: a) (Plurality)
        >>> profile.tau_fanatic
        TauVector({'a': 1.0}, voting_rule='Plurality')
    """
    pass


def test_anti_plurality():
    """
        >>> profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1}, voting_rule=ANTI_PLURALITY)
        >>> profile
        ProfileOrdinal({'abc': 0.5, 'acb': 0.5}, voting_rule='Anti-plurality')
        >>> print(profile)
        <abc: 0.5, acb: 0.5> (Condorcet winner: a) (Anti-plurality)
        >>> profile.tau_fanatic
        TauVector({'ab': 0.5, 'ac': 0.5}, voting_rule='Anti-plurality')
    """
    pass
