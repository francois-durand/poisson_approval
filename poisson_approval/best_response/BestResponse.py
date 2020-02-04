import numpy as np
from math import isclose
from fractions import Fraction
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import isnan, ballot_one, ballot_one_two
from poisson_approval.utils.UtilCache import cached_property


class BestResponse:
    """Best response for a given ordinal type of voter.

    Parameters
    ----------
    tau : TauVector
        A tau-vector.
    ranking : str
        Voter's ranking, e.g. ``'abc'``.

    Attributes
    ----------
    i, j, k : str
        The first (resp. second, third) candidate in `ranking`. E.g. ``a``.
    ij, ik, jk : str
        The ballots with two candidates. E.g. ``ab``.
    tau_i, tau_j, tau_k, tau_ij, tau_ik, tau_jk : Number
        The values of the tau-vector.
    """

    ASYMPTOTIC = 'Asymptotic method'
    ASYMPTOTIC_SIMPLIFIED = 'Simplified asymptotic method'
    EASY_VS_DIFFICULT = 'Easy vs difficult pivot'
    DIFFICULT_VS_EASY = 'Difficult vs easy pivot'
    OFFSET_METHOD = 'Offset method'

    def __init__(self, tau, ranking):
        self.tau = tau
        self.ranking = ranking
        self.i = ranking[0]
        self.j = ranking[1]
        self.k = ranking[2]
        self.ij = self.i + self.j
        self.ik = self.i + self.k
        self.jk = self.j + self.k
        self.tau_i = getattr(tau, self.i)
        self.tau_j = getattr(tau, self.j)
        self.tau_k = getattr(tau, self.k)
        self.tau_ij = getattr(tau, self.ij)
        self.tau_ik = getattr(tau, self.ik)
        self.tau_jk = getattr(tau, self.jk)

    # ================================
    # Shortcuts for some events of tau
    # ================================

    @cached_property
    def duo_ij(self):
        """EventDuo : the duo ij."""
        return getattr(self.tau, 'duo_' + self.ij)

    @cached_property
    def duo_ik(self):
        """EventDuo : the duo ik."""
        return getattr(self.tau, 'duo_' + self.ik)

    @cached_property
    def duo_jk(self):
        """EventDuo : the duo jk."""
        return getattr(self.tau, 'duo_' + self.jk)

    @cached_property
    def pivot_tij(self):
        """EventPivotTij : the `personalized pivot` between candidates i and j."""
        return getattr(self.tau, 'pivot_tij_' + self.ranking)

    @cached_property
    def pivot_tjk(self):
        """EventPivotTjk : the `personalized pivot` between candidates j and k."""
        return getattr(self.tau, 'pivot_tjk_' + self.ranking)

    @cached_property
    def trio_1t(self):
        """EventTrio1t : the first `personalized trio`."""
        return getattr(self.tau, 'trio_1t_' + self.i)

    @cached_property
    def trio_2t(self):
        """EventTrio1t : the second `personalized trio`."""
        return getattr(self.tau, 'trio_2t_' + self.ij)

    @cached_property
    def trio(self):
        """EventTrio : the 3-candidate tie."""
        return getattr(self.tau, 'trio')

    # =======
    # Results
    # =======

    @cached_property
    def results_asymptotic_method(self):
        """tuple (threshold_utility, justification)

        Results according to the asymptotic method. Cf. :attr:`threshold_utility` and :attr:`justification`.
        The threshold utility may be NaN, because this method is not always sufficient.
        """
        threshold_utility = ((
            self.pivot_tij.asymptotic * Fraction(1, 2)
            + self.trio_1t.asymptotic * Fraction(1, 3) + self.trio_2t.asymptotic * Fraction(1, 6)
        ) / (
            self.pivot_tij.asymptotic * Fraction(1, 2) + self.pivot_tjk.asymptotic * Fraction(1, 2)
            + self.trio_1t.asymptotic * Fraction(2, 3) + self.trio_2t.asymptotic * Fraction(1, 3)
        )).limit
        justification = self.ASYMPTOTIC
        return threshold_utility, justification

    @cached_property
    def results_limit_pivot_theorem(self):
        """tuple (threshold_utility, justification)

        Results according to the limit pivot theorem. Cf. :attr:`threshold_utility` and :attr:`justification`.
        If the tau-vector has two consecutive zeros, the theorem does not apply and this method returns
        ``nan, ''``.
        """
        if self.tau.has_two_consecutive_zeros:
            return np.nan, ''

        def multiply(tau_something, phi_something):
            return 0 if tau_something == 0 else tau_something * phi_something

        # Pivot ij
        # --------
        score_ij_in_duo_ij = (multiply(self.tau_i, self.duo_ij.phi[self.i])
                              + multiply(self.tau_ij, self.duo_ij.phi[self.ij])
                              + multiply(self.tau_ik, self.duo_ij.phi[self.ik]))
        score_k_in_duo_ij = (multiply(self.tau_k, self.duo_ij.phi[self.k])
                             + multiply(self.tau_ik, self.duo_ij.phi[self.ik])
                             + multiply(self.tau_jk, self.duo_ij.phi[self.jk]))
        pivot_ij_easy = score_ij_in_duo_ij > score_k_in_duo_ij
        pivot_ij_tight = isclose(score_ij_in_duo_ij, score_k_in_duo_ij)
        pivot_ij_easy_or_tight = pivot_ij_easy or pivot_ij_tight
        # TODO: remove the following verification later
        psi_k = self.trio.psi[self.k]
        assert pivot_ij_easy_or_tight == (isclose(psi_k, 1) or psi_k >= 1)
        # Pivot jk
        # --------
        score_jk_in_duo_jk = (multiply(self.tau_j, self.duo_jk.phi[self.j])
                              + multiply(self.tau_ij, self.duo_jk.phi[self.ij])
                              + multiply(self.tau_jk, self.duo_jk.phi[self.jk]))
        score_i_in_duo_jk = (multiply(self.tau_i, self.duo_jk.phi[self.i])
                             + multiply(self.tau_ij, self.duo_jk.phi[self.ij])
                             + multiply(self.tau_ik, self.duo_jk.phi[self.ik]))
        pivot_jk_easy = score_jk_in_duo_jk > score_i_in_duo_jk
        pivot_jk_tight = isclose(score_jk_in_duo_jk, score_i_in_duo_jk)
        pivot_jk_easy_or_tight = pivot_jk_easy or pivot_jk_tight
        # TODO: remove the following verification later
        psi_i = self.trio.psi[self.i]
        assert pivot_jk_easy_or_tight == (isclose(psi_i, 1) or psi_i >= 1)
        # Case distinction of the theorem
        # -------------------------------
        if pivot_ij_easy_or_tight and pivot_jk_easy_or_tight:
            # Both pivots are easy => We can forget the trios.
            threshold_utility = ((
                self.pivot_tij.asymptotic * Fraction(1, 2)
            ) / (
                self.pivot_tij.asymptotic * Fraction(1, 2) + self.pivot_tjk.asymptotic * Fraction(1, 2)
            )).limit
            justification = self.ASYMPTOTIC_SIMPLIFIED
        elif pivot_ij_easy_or_tight:
            # ... but pivot jk is difficult.
            threshold_utility = 1
            justification = self.EASY_VS_DIFFICULT
        elif pivot_jk_easy_or_tight:
            # ... but pivot ij is difficult.
            threshold_utility = 0
            justification = self.DIFFICULT_VS_EASY
        else:
            # Both pivots are difficult => General case of the offset method.
            pij = (1 + self.trio.psi[self.ik]) / (1 - self.trio.psi[self.k])
            pjk = (1 + self.trio.psi[self.j]) * self.trio.psi[self.i] ** 2 / (1 - self.trio.psi[self.i])
            p1t = self.trio.psi[self.i]
            p2t = self.trio.psi[self.ij]
            threshold_utility = (pij / 2 + p1t / 3 + p2t / 6) / (pij / 2 + pjk / 2 + p1t * 2 / 3 + p2t / 3)
            justification = self.OFFSET_METHOD
        return threshold_utility, justification

    @cached_property
    def results(self):
        """tuple (threshold_utility, justification)

        Cf. :attr:`threshold_utility` and :attr:`justification`. These results use:

        * The asymptotic method if there are two consecutive zeros in the "compass diagram" of the tau-vector,
        * The limit pivot theorem otherwise.
        """
        if self.tau.has_two_consecutive_zeros:
            return self.results_asymptotic_method
        else:
            return self.results_limit_pivot_theorem

    @cached_property
    def threshold_utility(self):
        """Number

        The threshold value of the utility for the second candidate (where the optimal ballot changes). If 1, then
        always vote for the first candidate. If 0, then always vote for the two most-liked candidates.
        """
        return self.results[0]

    @cached_property
    def justification(self):
        """str

        How the program computed the utility threshold. Nowadays, possible values are ``'Asymptotic method'``,
        ``'Simplified asymptotic method'``, ``'Easy vs difficult pivot'``, ``'Difficult vs easy pivot'``,
        ``'Offset method'``.
        """
        return self.results[1]

    @cached_property
    def ballot(self):
        """str

        This can be a valid ballot (e.g. ``'a'`` or ``'ab'`` if `ranking` is ``'abc'``) or ``'utility-dependent'``.
        """
        if isnan(self.threshold_utility):
            raise ValueError('Unable to compute threshold utility')  # pragma: no cover
        elif isclose(self.threshold_utility, 1):
            return ballot_one(self.ranking)
        elif isclose(self.threshold_utility, 0, abs_tol=1E-9):
            return ballot_one_two(self.ranking)
        else:
            return UTILITY_DEPENDENT

    def __repr__(self):
        return '<' + ', '.join([
            'ballot = %s' % self.ballot,
            'threshold_utility = {:.6g}'.format(self.threshold_utility),
            'justification = %s' % self.justification,
        ]) + '>'
