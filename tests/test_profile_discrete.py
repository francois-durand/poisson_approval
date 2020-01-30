from poisson_approval import ProfileDiscrete


def test_normalization():
    profile = ProfileDiscrete({('abc', 0.2): 1, ('acb', 0.4): 1})
    assert profile.abc == 0.5
