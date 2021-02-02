from poisson_approval.random_factories.RandProfileHistogramUniform import RandProfileHistogramUniform
from poisson_approval.utils.Util import one_over_log_t_plus_one, initialize_random_seeds


def frequency_cw_wins(factory, n_samples,
                      n_max_episodes, init='sincere',
                      perception_update_ratio=one_over_log_t_plus_one,
                      ballot_update_ratio=one_over_log_t_plus_one,
                      winning_frequency_update_ratio=one_over_log_t_plus_one,
                      meth='fictitious_play',
                      conditional_on_convergence=False):
    """
    Frequency of victory for the Condorcet winner.

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
    perception_update_ratio, ballot_update_ratio, winning_frequency_update_ratio : callable or Number
        Cf. :meth:`Profile.fictitious_play` or :meth:`Profile.iterated_voting`.
    meth : str
        The name of the method (``'fictitious_play'`` or ``'iterated_voting'``).
    conditional_on_convergence : bool
        If True, then profiles that do not converge (within ``n_max_episodes``) are rejected from the sample.

    Returns
    -------
    float
        The frequency of victory for the Condorcet winner.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> rand_profile = RandProfileHistogramUniform(n_bins=1)
        >>> frequency_cw_wins(factory=rand_profile, n_samples=1, n_max_episodes=10)
        1.0
    """
    total = 0
    i_samples = 0
    i_failed_trials = 0
    while i_samples < n_samples:
        profile = factory()
        if len(profile.condorcet_winners) != 1:  # pragma: no cover
            raise ValueError('The profile does not have one Condorcet winner: %s' % profile)
        results = getattr(profile, meth)(init=init, n_max_episodes=n_max_episodes,
                                         perception_update_ratio=perception_update_ratio,
                                         ballot_update_ratio=ballot_update_ratio,
                                         winning_frequency_update_ratio=winning_frequency_update_ratio)
        if conditional_on_convergence and not results['converges']:
            i_failed_trials += 1
            if i_failed_trials >= n_samples and i_samples == 0:
                raise ValueError("Emergency stop: out of %s samples, the process never converged." % n_samples)
            else:
                continue
        i_samples += 1
        condorcet_winner = list(profile.condorcet_winners)[0]
        total += results['d_candidate_winning_frequency'][condorcet_winner]
    return float(total / n_samples)