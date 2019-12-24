import warnings
from math import isclose
import numpy as np
from poisson_approval.constants.constants import *
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold
from poisson_approval.profiles.ProfileCardinal import ProfileCardinal
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.utils.UtilCache import cached_property


class ProfileHistogram(ProfileCardinal):
    """A profile of preference with histogram distributions of utility.

    Parameters
    ----------
    d_ranking_share : dict
        E.g. ``{'abc': 0.4, 'cab': 0.6}``. ``d_ranking_share['abc']`` is the probability that a voter prefers candidate
        ``a``, then candidate ``b``, then candidate ``c``.
    d_ranking_histogram : dict
        Each key is a ranking, e.g. ``'abc'``. Each value is a list that represents a piecewise constant probability
        density function (PDF) of having a utility `u` for the middle candidate, e.g. ``b``. By convention, the list
        sums to 1 (contrary to the usual convention where the integral of the function would sum to 1).

        For example, if the list is ``[0.4, 0.3, 0.2, 0.1]``, it means that a fraction 0.4 of voters ``'abc'`` have a
        utility for ``b`` that is in the first quarter, i.e. between 0 and 0.25. These voters are uniformly distributed
        in this segment.
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.

    Notes
    -----
    If the input distribution is not normalized, the profile will be normalized anyway and a warning is
    issued (unless `normalization_warning` is False).

    Examples
    --------
        >>> from fractions import Fraction
        >>> r = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
        >>> r  # doctest: +NORMALIZE_WHITESPACE
        ProfileHistogram({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)}, {'abc': array([1]), \
'bac': array([1, 0]), 'cab': array([Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)],
            dtype=object)})
        >>> print(r)
        <abc: 1/10 [1], bac: 3/5 [1 0], cab: 3/10 [Fraction(2, 3) 0 0 0 0 0 0 0 0 Fraction(1, 3)]> (Condorcet winner: b)
        >>> r.abc
        Fraction(1, 10)
        >>> r.d_ranking_share['abc']  # Alternate syntax for r.abc
        Fraction(1, 10)
        >>> r.weighted_maj_graph
        array([[0, Fraction(-1, 5), Fraction(2, 5)],
               [Fraction(1, 5), 0, Fraction(2, 5)],
               [Fraction(-2, 5), Fraction(-2, 5), 0]], dtype=object)
        >>> r.condorcet_winners
        Winners({'b'})
        >>> r.is_profile_condorcet
        1.0
        >>> r.has_majority_favorite  # Is one candidate 'top' in a majority of ballots?
        True
        >>> r.has_majority_ranking  # Does one ranking represent a majority of ballots?
        True
        >>> r.is_single_peaked  # Is the profile single-peaked?
        True
        >>> r.support_in_rankings
        {'abc', 'bac', 'cab'}
        >>> r.is_generic_in_rankings  # Are all rankings there?
        False
        >>> sigma = StrategyThreshold({'abc': 0, 'bac': 1, 'cab': Fraction(1, 2)}, profile=r)
        >>> print(r.tau(sigma))
        <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> r.is_equilibrium(sigma)
        EquilibriumStatus.EQUILIBRIUM
        >>> cycle = r.iterated_voting(StrategyThreshold({'abc': .5, 'bac': .5, 'cab': .5}),  100)
        >>> len(cycle)
        1
        >>> print(cycle[0])
        <abc: ab, bac: utility-dependent (0.7199316142046179), cab: utility-dependent (0.2800683857953819)> ==> b
    """

    def __init__(self, d_ranking_share, d_ranking_histogram, normalization_warning=True):
        super().__init__()
        # Populate the dictionary and check for typos in the input
        self._d_ranking_share = DictPrintingInOrderIgnoringZeros()
        self.d_ranking_histogram = DictPrintingInOrderIgnoringZeros()
        for ranking, share in d_ranking_share.items():
            if ranking in RANKINGS:
                self._d_ranking_share[ranking] = share
            else:
                raise ValueError('Unknown key: ' + ranking)
        for ranking, histogram in d_ranking_histogram.items():
            if ranking in RANKINGS:
                self.d_ranking_histogram[ranking] = np.array(histogram)
            else:
                raise ValueError('Unknown key: ' + ranking)
        for ranking in RANKINGS:
            if ranking not in self._d_ranking_share:
                self._d_ranking_share[ranking] = 0
            if ranking not in self.d_ranking_histogram:
                self.d_ranking_histogram[ranking] = np.array([])
        # Normalize if necessary
        total = sum(self._d_ranking_share.values())
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: profile is not normalized, I will normalize it.")
            for ranking in self._d_ranking_share.keys():
                self._d_ranking_share[ranking] = self._d_ranking_share[ranking] / total
        for ranking, histogram in self.d_ranking_histogram.items():
            if len(histogram) == 0:
                continue
            total = np.sum(histogram)
            if not isclose(total, 1.):
                if normalization_warning:
                    warnings.warn("Warning: profile is not normalized, I will normalize it.")
                histogram /= total

    @cached_property
    def d_ranking_share(self):
        return self._d_ranking_share

    def have_ranking_with_utility_above_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly above a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_above_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            >>> r.have_ranking_with_utility_above_u(ranking='cab', u=0)
            Fraction(3, 10)
            >>> r.have_ranking_with_utility_above_u(ranking='cab', u=Fraction(1, 100))
            Fraction(7, 25)
            >>> r.have_ranking_with_utility_above_u(ranking='cab', u=Fraction(99, 100))
            Fraction(1, 100)
            >>> r.have_ranking_with_utility_above_u(ranking='cab', u=1)
            Fraction(0, 1)
        """
        return self.d_ranking_share[ranking] - self.have_ranking_with_utility_below_u(ranking, u)

    def have_ranking_with_utility_u(self, ranking, u):
        """Share of voters who have a given ranking and a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            >>> r.have_ranking_with_utility_u(ranking='cab', u=Fraction(1, 100))
            0
        """
        return 0

    def have_ranking_with_utility_below_u(self, ranking, u):
        """Share of voters who have a given ranking and strictly below a given utility for their middle candidate.

        Cf. :meth:`ProfileCardinal.have_ranking_with_utility_below_u`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            >>> r.have_ranking_with_utility_below_u(ranking='cab', u=0)
            Fraction(0, 1)
            >>> r.have_ranking_with_utility_below_u(ranking='cab', u=Fraction(1, 100))
            Fraction(1, 50)
            >>> r.have_ranking_with_utility_below_u(ranking='cab', u=Fraction(99, 100))
            Fraction(29, 100)
            >>> r.have_ranking_with_utility_below_u(ranking='cab', u=1)
            Fraction(3, 10)
        """
        share_ranking = self.d_ranking_share[ranking]
        if share_ranking == 0:
            return 0
        if u == 1:
            return share_ranking
        histogram = self.d_ranking_histogram[ranking]
        n_bins = len(histogram)
        k = int(u * n_bins)
        if histogram[k] == 0:
            # Not really an exception, but handles fractions more nicely.
            return share_ranking * np.sum(histogram[0:k])
        else:
            return share_ranking * (np.sum(histogram[0:k]) + histogram[k] * (u * n_bins - k))

    def __repr__(self):
        return 'ProfileHistogram(%r, %r)' % (self.d_ranking_share, self.d_ranking_histogram)

    def __str__(self):
        result = '<' + ', '.join([
            '%s: %s %s' % (ranking, self.d_ranking_share[ranking], self.d_ranking_histogram[ranking])
            for ranking in sorted(self.d_ranking_share)
            if self.d_ranking_share[ranking] > 0 or len(self.d_ranking_histogram[ranking]) > 0
        ]) + '>'
        if self.is_profile_condorcet:
            result += ' (Condorcet winner: %s)' % self.condorcet_winners
        return result

    def _repr_pretty_(self, p, cycle):
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    def __eq__(self, other):
        """Equality test.

        Parameters
        ----------
        other : Object

        Returns
        -------
        bool
            True iff this profile is equal to `other`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> r = ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            >>> r == ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            True
        """
        return (isinstance(other, ProfileHistogram)
                and self.d_ranking_share == other.d_ranking_share
                and self.d_ranking_histogram == self.d_ranking_histogram)

    # Standardized version of the profile (makes it unique, up to permutations)

    @cached_property
    def standardized_version(self):
        """ProfileTwelve : Standardized version of the profile (makes it unique, up to permutations of the candidates).

         Examples
         --------
            >>> from fractions import Fraction
            >>> r = ProfileHistogram(
            ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
            ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]})
            >>> print(r.standardized_version)
            <abc: 3/5 [1 0], bac: 1/10 [1], cba: 3/10 [Fraction(2, 3) 0 0 0 0 0 0 0 0 Fraction(1, 3)]> \
(Condorcet winner: a)
            >>> r.is_standardized
            False
        """
        def translate(s, permute):
            return s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])

        best_d_ranking_share = {}
        best_d_ranking_histogram = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_ranking_share_test = {translate(ranking, perm): share
                                    for ranking, share in self.d_ranking_share.items()}
            d_ranking_histogram_test = {translate(ranking, perm): histogram
                                        for ranking, histogram in self.d_ranking_histogram.items()}
            signature_test = [d_ranking_share_test[ranking] for ranking in XYZ_RANKINGS]
            for ranking in XYZ_RANKINGS:
                signature_test.extend(d_ranking_histogram_test[ranking])
            if signature_test > best_signature:
                best_signature = signature_test
                best_d_ranking_share = d_ranking_share_test
                best_d_ranking_histogram = d_ranking_histogram_test
        return ProfileHistogram(
            d_ranking_share={ranking: best_d_ranking_share[xyz_ranking]
                             for ranking, xyz_ranking in zip(RANKINGS, XYZ_RANKINGS)},
            d_ranking_histogram={ranking: best_d_ranking_histogram[xyz_ranking]
                                 for ranking, xyz_ranking in zip(RANKINGS, XYZ_RANKINGS)}
        )
