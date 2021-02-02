from poisson_approval.random_factories.RandProfileHistogramUniform import RandProfileHistogramUniform
from poisson_approval.utils.Util import one_over_log_t_plus_one, initialize_random_seeds


def ballot_statistics(factory, n_samples,
                      n_max_episodes, init='sincere',
                      perception_update_ratio=one_over_log_t_plus_one,
                      ballot_update_ratio=one_over_log_t_plus_one,
                      statistics_update_ratio=one_over_log_t_plus_one,
                      meth='fictitious_play',
                      conditional_on_convergence=False):
    """
    Ballot statistics.

    Parameters
    ----------
    factory : callable
        A factory that returns a (random) profile. Cf. e.g. :class:`RandProfileHistogramUniform`, etc. Each
        returned profile must have a unique Condorcet winner.
    n_samples : int
        The number of profiles drawn.
    n_max_episodes : int
        Maximum number of episodes for the fictitious play / iterated voting.
    init : Strategy or TauVector or str
        Cf. :meth:`Profile.fictitious_play` or :meth:`Profile.iterated_voting`.
    perception_update_ratio, ballot_update_ratio, statistics_update_ratio : callable or Number
        Cf. :meth:`Profile.fictitious_play` or :meth:`Profile.iterated_voting`.
    meth : str
        The name of the method (``'fictitious_play'`` or ``'iterated_voting'``).
    conditional_on_convergence : bool
        If True, then profiles that do not converge (within ``n_max_episodes``) are rejected from the sample.

    Returns
    -------
    ratio_single_votes : float
        The ratio of single votes.
    ratio_double_votes : float
        The ratio of double votes.
    ratio_sincere_votes : float
        The ratio of sincere votes.
    ratio_insincere_votes : float
        The ratio of insincere votes.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> rand_profile = RandProfileHistogramUniform(n_bins=1)
        >>> results = ballot_statistics(factory=rand_profile, n_samples=10, n_max_episodes=10)
        >>> ratio_single_votes, ratio_double_votes, ratio_sincere_votes, ratio_insincere_votes = results
        >>> ratio_single_votes
        0.6832229534288994
        >>> ratio_double_votes
        0.3167770465711006
        >>> ratio_sincere_votes
        0.5996763226642906
        >>> ratio_insincere_votes
        0.4003236773357094
    """
    ratio_single_votes = 0
    ratio_sincere_votes = 0
    i_samples = 0
    i_failed_trials = 0
    while i_samples < n_samples:
        profile = factory()
        results = getattr(profile, meth)(init=init, n_max_episodes=n_max_episodes,
                                         perception_update_ratio=perception_update_ratio,
                                         ballot_update_ratio=ballot_update_ratio,
                                         other_statistics_update_ratio=statistics_update_ratio,
                                         other_statistics_strategy={
                                             'share_single_votes': (lambda strategy: strategy.share_single_votes),
                                             'share_sincere': (lambda strategy: strategy.share_sincere)
                                         })
        if conditional_on_convergence and not results['converges']:
            i_failed_trials += 1
            if i_failed_trials >= n_samples and i_samples == 0:
                raise ValueError("Emergency stop: out of %s samples, the process never converged." % n_samples)
            else:
                continue
        i_samples += 1
        ratio_single_votes += results['share_single_votes']
        ratio_sincere_votes += results['share_sincere']
    ratio_single_votes /= n_samples
    ratio_double_votes = 1 - ratio_single_votes
    ratio_sincere_votes /= n_samples
    ratio_insincere_votes = 1 - ratio_sincere_votes
    return ratio_single_votes, ratio_double_votes, ratio_sincere_votes, ratio_insincere_votes
