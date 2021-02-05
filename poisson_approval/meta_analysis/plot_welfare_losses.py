import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.utils.UtilPlot import plt_cdf


def plot_welfare_losses(results, criterion):
    """
    Plot the distribution (CDF) of the welfare losses, for each voting rule.

    Parameters
    ----------
    results : dict
        Results of :func:`monte_carlo_fictitious_play`, with at least the setting ``MCS_WELFARE_LOSSES``.
    kwargs
        Other keyword arguments are passed to the function `step` of matplotlib.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    voting_rules = results.keys()
    for voting_rule in voting_rules:
        n_samples = results[voting_rule]['n_samples']
        welfare_losses = np.array(results[voting_rule][criterion]).flatten()
        weights = np.array(results[voting_rule]['candidate_winning_frequencies']).flatten() / n_samples
        plt_cdf(welfare_losses, weights, n_samples, label=voting_rule)
    ax.grid(True)
    ax.legend()
    ax.set_xlabel('Loss of absolute welfare')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))
