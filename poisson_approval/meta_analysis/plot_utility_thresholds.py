import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.utils.UtilPlot import plt_cdf


def plot_utility_thresholds(results, voting_rule, **kwargs):
    """
    Plot the distribution (CDF) of the threshold utility.

    Parameters
    ----------
    results : dict
        Results of :func:`monte_carlo_fictitious_play`, with at least the setting ``MCS_UTILITY_THRESHOLDS``.
    voting_rule : str
        The voting rule (or None if this parameter was not given to :func:`monte_carlo_fictitious_play`).
    kwargs
        Other keyword arguments are passed to the function `step` of matplotlib.
    """
    n_samples = results[voting_rule]['n_samples']
    threshold_utilities = np.array(results[voting_rule]['threshold_utilities']).flatten()
    weights = np.array(results[voting_rule]['weights_rankings']).flatten() / n_samples
    fig, ax = plt.subplots(figsize=(8, 4))
    plt_cdf(threshold_utilities, weights, n_samples, label='Utility', **kwargs)
    ax.grid(True)
    # ax.set_title('Threshold utility')
    ax.set_xlabel('Threshold utility')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))
