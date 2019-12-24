import numpy as np
import matplotlib.pyplot as plt
from poisson_approval.utils.Util import initialize_random_seeds
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal
from poisson_approval.generators.GeneratorProfileOrdinalUniform import GeneratorProfileOrdinalUniform


# noinspection PyUnresolvedReferences
class NiceStatsProfileOrdinal:
    """Compute nice stats on ordinal profiles.

    Parameters
    ----------
    tests_r : list
        A list of pairs ``(test, name)``. ``test`` is a function ``ProfileOrdinal -> bool``. ``name`` is a
        string.
    tests_sigma : list
        A list of pairs ``(test, name)``. ``test`` is a function ``StrategyOrdinal -> bool``. ``name`` is a string.
        For these tests, we compute only the probability that a equilibrium meeting the test exists.
    tests_sigma_dist : list
        A list of pairs ``(test, name)``. ``test`` is a function ``StrategyOrdinal -> bool``. ``name`` is a string.
        For these tests, we compute the distribution of numbers of equilibria meeting the test.
    tests_sigma_winners : list
        A list of pairs ``(test, name)``. ``test`` is a function ``StrategyOrdinal -> bool``. ``name`` is a string.
        For these tests, we compute the distribution of numbers of winners in equilibria meeting the test.
    conditional_on : callable
        A function ``ProfileOrdinal -> bool``.
    generator_profiles : callable
        A callable that inputs nothing and outputs a profile. Default: ``GeneratorProfileOrdinalUniform()``.

    Notes
    -----
    The tests in `tests_r` concern the profile: what proportions of profiles meet the condition?

    The tests in `tests_sigma` concern the strategies, in the cases where they are equilibrium. For each
    ordinal profile, we compute the probability (for a uniform distribution of utilities) that at least one sigma
    is an equilibrium and meet the given condition. This is used to draw plots `à la Antonin`.

    The tests in `tests_sigma_dist` or `tests_sigma_winners` concern also the strategies, in the cases where
    they are equilibrium.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> nice_stats = NiceStatsProfileOrdinal(
        ...     tests_r=[
        ...         (lambda r: any([sigma for sigma in r.analyzed_strategies.equilibria
        ...                         if sigma.profile.condorcet_winners == sigma.winners]),
        ...          'There exists a true equilibrium electing the CW'),
        ...     ],
        ...     tests_sigma=[
        ...         (lambda sigma: sigma.profile.condorcet_winners == sigma.winners,
        ...          'There exists an equilibrium that elects the CW')
        ...     ],
        ...     tests_sigma_dist=[
        ...         (lambda sigma: sigma.profile.condorcet_winners == sigma.winners,
        ...          'There exists an equilibrium that elects the CW')
        ...     ],
        ...     conditional_on=lambda r: r.is_profile_condorcet == 1.
        ... )
        >>> nice_stats.run(n_samples=10)
        >>> profile = nice_stats.find_example('There exists a true equilibrium electing the CW', False)
        >>> print(profile)
        <abc: 0.4236547993389047, acb: 0.12122838365799216, bac: 0.0039303209304278885, bca: 0.05394987214431912, \
cab: 0.1124259903007756, cba: 0.2848106336275805> (Condorcet winner: a)
    """

    def __init__(self, tests_r=None, tests_sigma=None, tests_sigma_dist=None, tests_sigma_winners=None,
                 conditional_on=None, generator_profiles=None):
        self.tests_r = [] if tests_r is None else tests_r
        self.tests_sigma = [] if tests_sigma is None else tests_sigma
        self.tests_sigma_dist = [] if tests_sigma_dist is None else tests_sigma_dist
        self.tests_sigma_winners = [] if tests_sigma_winners is None else tests_sigma_winners
        self.conditional_on = (lambda r: True) if conditional_on is None else conditional_on
        self.generator_profiles = GeneratorProfileOrdinalUniform() if generator_profiles is None else generator_profiles
        # Computed variables
        self.n_samples = None
        self.profiles = None
        self.results_r = None
        self.results_sigma = None
        self.results_sigma_dist = None
        self.results_sigma_winners = None

    def run(self, n_samples):
        """Run the simulations and store the results.

        Parameters
        ----------
        n_samples : int
            Number of profiles meeting the precondition `conditional_on`.
        """
        self.n_samples = n_samples
        i_sample = 0
        self.profiles = []
        self.results_r = [[] for _ in range(len(self.tests_r))]
        self.results_sigma = [[] for _ in range(len(self.tests_sigma))]
        self.results_sigma_dist = [np.zeros(2**6) for _ in range(len(self.tests_sigma_dist))]
        self.results_sigma_winners = [np.zeros(4) for _ in range(len(self.tests_sigma_winners))]
        while i_sample < n_samples:
            r = self.generator_profiles()
            if self.conditional_on(r):
                i_sample += 1
            else:
                continue
            self.profiles.append(r.d_ranking_share)
            for i, (test, _) in enumerate(self.tests_r):
                self.results_r[i].append(test(r))
            for i, (test, _) in enumerate(self.tests_sigma):
                self.results_sigma[i].append(r.proba_equilibrium(test=test))
            for i, (test, _) in enumerate(self.tests_sigma_dist):
                histogram = r.distribution_equilibria(test=test)
                self.results_sigma_dist[i][:len(histogram)] += histogram
            for i, (test, _) in enumerate(self.tests_sigma_winners):
                histogram = r.distribution_winners(test=test)
                self.results_sigma_winners[i][:len(histogram)] += histogram
        for histogram in self.results_sigma_dist:
            histogram /= n_samples
        for histogram in self.results_sigma_winners:
            histogram /= n_samples

    def plot_test_sigma(self, test, ylabel=True, legend=False, replacement_name=None, style=''):
        """Plot a test on sigma.

        Parameters
        ----------
        test : str or int
            Name or index of a test in `tests_sigma`.
        ylabel : bool
            If True, the name is used in the y-label. Otherwise, the label is `P` (probability).
        legend : bool
            If True, the legend is displayed.
        replacement_name : str, optional
            If specified, it will be used instead of the test name in the plot.
        style : str
            Cf. :meth:`matplotlib.pyplot.plot`.
        """
        if isinstance(test, str):
            i = [name for _, name in self.tests_sigma].index(test)
        else:
            i = test
        (_, name) = self.tests_sigma[i]
        if replacement_name is not None:
            name = replacement_name
        plt.plot(np.arange(0, 1, 1 / self.n_samples), sorted(self.results_sigma[i]), style, label=name)
        plt.ylim(-0.05, 1.05)
        plt.xlabel('Cumulative share of ordinal preference profiles')
        if ylabel:
            plt.ylabel('$\mathbb{P}$(%s)' % name)
        else:
            plt.ylabel('$\mathbb{P}$')
        if legend:
            plt.legend()

    def plot_cutoff(self, test, left='', right='', style=''):
        """Plot the cutoff of a test on the profile.

        Parameters
        ----------
        test : str or int
            Name or index of a test in `tests_r`.
        left : str
            Text to be written on the left.
        right : str
            Text to be written on the right.
        style : str
            Cf. :meth:`matplotlib.pyplot.plot`.
        """
        if isinstance(test, str):
            i = [name for _, name in self.tests_r].index(test)
        else:
            i = test
        (_, name) = self.tests_r[i]
        x = np.sum(self.results_r[i]) / self.n_samples
        plt.plot([1 - x, 1 - x], [0., 1.], style)
        plt.text((1 - x) / 2, 0.1, left)
        plt.text(1 - x / 2, 0.1, right)

    def display_results(self):
        """Display the results."""
        for i, (_, name) in enumerate(self.tests_r):
            print('P(%s) = %s' % (name, np.sum(self.results_r[i]) / self.n_samples))
        for i, (_, name) in enumerate(self.tests_sigma):
            self.plot_test_sigma(test=i)
            plt.show()
        for i, (_, name) in enumerate(self.tests_sigma_dist):
            print('P(%s) :' % name)
            true_dim = np.max(np.flatnonzero(self.results_sigma_dist[i])) + 1
            print({k: self.results_sigma_dist[i][k] for k in range(true_dim)})
            plt.bar(range(true_dim), self.results_sigma_dist[i][:true_dim])
            plt.xticks(range(true_dim))
            plt.xlabel(name)
            plt.ylabel('$\mathbb{P}$')
            plt.ylim(0, 1)
            plt.show()
        for i, (_, name) in enumerate(self.tests_sigma_winners):
            print('%s :' % name)
            true_dim = 4
            print({k: self.results_sigma_winners[i][k] for k in range(true_dim)})
            plt.bar(range(true_dim), self.results_sigma_winners[i][:true_dim])
            plt.xticks(range(true_dim))
            plt.xlabel(name)
            plt.ylabel('$\mathbb{P}$')
            plt.ylim(0, 1)
            plt.show()

    def find_example(self, test, value=True):
        """Find an example profile.

        Parameters
        ----------
        test : str or int
            Name or index of a test in `tests_r`.
        value : bool
            Whether we want an example (True) or a counter-example (False).

        Returns
        -------
        ProfileOrdinal
            A profile for which the test returned `value` in the simulation.
        """
        if isinstance(test, str):
            i_test = [name for _, name in self.tests_r].index(test)
        else:
            i_test = test
        i_profile = self.results_r[i_test].index(value)
        return ProfileOrdinal(self.profiles[i_profile])
