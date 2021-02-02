import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.constants.constants import RANKINGS
from poisson_approval.utils.Util import one_over_log_t_plus_one
from poisson_approval.utils.UtilPlot import plt_cdf


def plot_distribution_threshold_utilities(factory, n_samples,
                                          n_max_episodes, init='sincere',
                                          perception_update_ratio=one_over_log_t_plus_one,
                                          ballot_update_ratio=one_over_log_t_plus_one,
                                          statistics_update_ratio=one_over_log_t_plus_one,
                                          meth='fictitious_play',
                                          conditional_on_convergence=False,
                                          **kwargs):
    """
    Plot the distribution (CDF) of the threshold utility.

    Parameters
    ----------
    factory : callable
        A factory that returns a (random) profile. Cf. e.g. :class:`RandProfileHistogramUniform`, etc.
        The returned profile must have only strict orders.
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
    kwargs
        Other keyword arguments are passed to the function `step` of matplotlib.

    Returns
    -------
    threshold_utilities : list
        List of threshold utilities found in the computation.
    weights : list
        List of weights corresponding to each threshold utility (= share of voters with the relevant ranking).
    """
    # Compute the data
    threshold_utilities = []

    def f_threshold_utilities(strategy):
        return np.array([strategy.d_ranking_threshold[ranking] for ranking in RANKINGS])

    weights = []
    i_samples = 0
    i_failed_trials = 0
    while i_samples < n_samples:
        profile = factory()
        results = getattr(profile, meth)(init=init, n_max_episodes=n_max_episodes,
                                         perception_update_ratio=perception_update_ratio,
                                         ballot_update_ratio=ballot_update_ratio,
                                         other_statistics_update_ratio=statistics_update_ratio,
                                         other_statistics_strategy={'threshold_utilities': f_threshold_utilities})
        if conditional_on_convergence and not results['converges']:
            i_failed_trials += 1
            if i_failed_trials >= n_samples and i_samples == 0:
                raise ValueError("Emergency stop: out of %s samples, the process never converged." % n_samples)
            else:
                continue
        i_samples += 1
        threshold_utilities.extend(list(results['threshold_utilities']))
        weights.extend([profile.d_ranking_share[ranking] for ranking in RANKINGS])
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 4))
    plt_cdf(threshold_utilities, weights, n_samples, label='Utility', **kwargs)
    ax.grid(True)
    # ax.set_title('Threshold utility')
    ax.set_xlabel('Threshold utility')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))

    # Return the data
    return threshold_utilities, weights
