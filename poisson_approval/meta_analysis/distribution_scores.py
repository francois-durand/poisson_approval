import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.utils.Util import one_over_log_t_plus_one
from poisson_approval.utils.UtilPlot import plt_cdf


def plot_distribution_scores(factory, n_samples,
                             n_max_episodes, init='sincere',
                             perception_update_ratio=one_over_log_t_plus_one,
                             ballot_update_ratio=one_over_log_t_plus_one,
                             statistics_update_ratio=one_over_log_t_plus_one,
                             meth='fictitious_play',
                             conditional_on_convergence=False,
                             **kwargs):  # pragma: no cover
    """
    Plot the distribution (CDF) of the scores for the winner, the challenger and the loser.

    Parameters
    ----------
    factory : callable
        A factory that returns a (random) profile. Cf. e.g. :class:`RandProfileHistogramUniform`, etc.
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
    scores_winner, scores_second, scores_loser : list
        List of scores of the winner (resp. second, loser) found in the computation.
    """
    # Compute the data
    scores_winner = []
    scores_second = []
    scores_loser = []

    def decreasing_scores(tau):
        return np.array(sorted(tau.scores, reverse=True))

    i_samples = 0
    i_failed_trials = 0
    while i_samples < n_samples:
        profile = factory()
        results = getattr(profile, meth)(init=init, n_max_episodes=n_max_episodes,
                                         perception_update_ratio=perception_update_ratio,
                                         ballot_update_ratio=ballot_update_ratio,
                                         other_statistics_update_ratio=statistics_update_ratio,
                                         other_statistics_strategy={'decreasing_scores': decreasing_scores})
        if conditional_on_convergence and not results['converges']:
            i_failed_trials += 1
            if i_failed_trials >= n_samples and i_samples == 0:
                raise ValueError("Emergency stop: out of %s samples, the process never converged." % n_samples)
            else:
                continue
        i_samples += 1
        decreasing_scores = results['decreasing_scores']
        scores_winner.append(decreasing_scores[0])
        scores_second.append(decreasing_scores[1])
        scores_loser.append(decreasing_scores[2])
    weights = np.ones(n_samples) / n_samples

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 4))
    plt_cdf(scores_winner, weights, n_samples, label='Winner', **kwargs)
    plt_cdf(scores_second, weights, n_samples, label='Challenger', **kwargs)
    plt_cdf(scores_loser, weights, n_samples, label='Loser', **kwargs)
    ax.grid(True)
    ax.legend()
    # ax.set_title('Score of the candidates')
    ax.set_xlabel('Score')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))

    # Return the data
    return scores_winner, scores_second, scores_loser
