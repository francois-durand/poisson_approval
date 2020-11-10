import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.utils.Util import one_over_log_t_plus_one


def plot_distribution_scores(factory, n_samples,
                             n_max_episodes, init='sincere',
                             perception_update_ratio=one_over_log_t_plus_one,
                             ballot_update_ratio=one_over_log_t_plus_one,
                             winning_frequency_update_ratio=one_over_log_t_plus_one,
                             meth='fictitious_play', **kwargs):  # pragma: no cover
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
    perception_update_ratio, ballot_update_ratio, winning_frequency_update_ratio : callable or Number
        Cf. :meth:`Profile.fictitious_play` or :meth:`Profile.iterated_voting`.
    meth : str
        The name of the method (``'fictitious_play'`` or ``'iterated_voting'``).
    kwargs
        Other keyword arguments are passed to the function `step` of matplotlib.
    """
    # Compute the data
    scores_winner = []
    scores_second = []
    scores_loser = []
    i_samples = 0
    i_failed_trials = 0
    while i_samples < n_samples:
        profile = factory()
        results = getattr(profile, meth)(init=init, n_max_episodes=n_max_episodes,
                                         perception_update_ratio=perception_update_ratio,
                                         ballot_update_ratio=ballot_update_ratio,
                                         winning_frequency_update_ratio=winning_frequency_update_ratio)
        if results['tau'] is None:
            i_failed_trials += 1
            if i_failed_trials >= n_samples and i_samples == 0:
                raise ValueError("Emergency stop: out of %s samples, the process never converged." % n_samples)
            else:
                continue
        i_samples += 1
        scores = results['tau'].scores
        scores_sorted = sorted(scores.values())
        scores_winner.append(scores_sorted[2])
        scores_second.append(scores_sorted[1])
        scores_loser.append(scores_sorted[0])

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 4))
    _plot_cdf(scores_winner, label='Winner', **kwargs)
    _plot_cdf(scores_second, label='Challenger', **kwargs)
    _plot_cdf(scores_loser, label='Loser', **kwargs)
    ax.grid(True)
    ax.legend()
    ax.set_title('Score of the candidates')
    ax.set_xlabel('Score')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))


def _plot_cdf(data, **kwargs):  # pragma: no cover
    sorted_data = np.sort(data)
    plt.step([0] + list(sorted_data) + [1], [0] + list(np.arange(sorted_data.size) / sorted_data.size) + [1],
             **kwargs)
