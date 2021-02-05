from poisson_approval import monte_carlo_fictitious_play, RandProfileHistogramUniform


def test_no_mcs():
    """
        >>> meta_results = monte_carlo_fictitious_play(
        ...     factory=RandProfileHistogramUniform(n_bins=1),
        ...     n_samples=1,
        ...     n_max_episodes=10,
        ... )
        >>> meta_results
        {'': {'n_samples': 1}}
    """
    pass


def test_with_save_file():
    """
        >>> import pickle
        >>> file_save = 'zzz_test_monte_carlo_with_save_file.sav'
        >>> _ = monte_carlo_fictitious_play(
        ...     factory=RandProfileHistogramUniform(n_bins=1),
        ...     n_samples=1,
        ...     n_max_episodes=10,
        ...     file_save=file_save,
        ... )
        >>> with open(file_save, "rb") as f:
        ...     meta_results = pickle.load(f)
        >>> meta_results
        {'': {'n_samples': 1}}
    """
    pass
