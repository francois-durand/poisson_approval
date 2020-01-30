from poisson_approval import ProfileOrdinal


def test_normalization():
    profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1})
    assert profile.abc == 0.5
