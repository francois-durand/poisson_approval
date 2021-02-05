import numpy as np
from matplotlib import pyplot as plt
from poisson_approval.utils.UtilPlot import plt_cdf


def plot_distribution_scores(results, voting_rule=None, **kwargs):
    """
    Plot the distribution (CDF) of the scores for the winner, the challenger and the loser.

    Parameters
    ----------
    results : dict
        Results of :func:`monte_carlo_fictitious_play`, with at least the setting ``MCS_DECREASING_SCORES``.
    voting_rule : str
        The voting rule (or None if this parameter was not given to :func:`monte_carlo_fictitious_play`).
    kwargs
        Other keyword arguments are passed to the function `step` of matplotlib.
    """
    if voting_rule is None:
        voting_rule = ''
    n_samples = results[voting_rule]['n_samples']
    weights = np.ones(n_samples) / n_samples
    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 4))
    plt_cdf(results[voting_rule]['score_winner'], weights, n_samples, label='Winner', **kwargs)
    plt_cdf(results[voting_rule]['score_second'], weights, n_samples, label='Challenger', **kwargs)
    plt_cdf(results[voting_rule]['score_loser'], weights, n_samples, label='Loser', **kwargs)
    ax.grid(True)
    ax.legend()
    # ax.set_title('Score of the candidates')
    ax.set_xlabel('Score')
    ax.set_ylabel('Cumulative likelihood of occurrence')
    plt.xlim(0, 1)
    plt.xticks(np.arange(0, 1.1, 0.1))
