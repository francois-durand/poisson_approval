import numpy as np
from math import isclose
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
    pivot_tij : EventPivotTij
        `Personalized pivot` between her first and second candidate.
    pivot_tjk : EventPivotTjk
        `Personalized pivot` between her second and third candidate.
    trio_1t : EventTrio1t
        First `personalized trio`.
    trio_2t : EventTrio2t
        Second `personalized trio`.
    trio : EventTrio
        3-candidate tie.
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
        self.tau_i = getattr(tau, self.i)
        self.tau_j = getattr(tau, self.j)
        self.tau_k = getattr(tau, self.k)
        self.tau_ij = getattr(tau, self.i + self.j)
        self.tau_ik = getattr(tau, self.i + self.k)
        self.tau_jk = getattr(tau, self.j + self.k)
        self.duo_ij = getattr(tau, 'duo_' + self.i + self.j)
        self.duo_ik = getattr(tau, 'duo_' + self.i + self.k)
        self.duo_jk = getattr(tau, 'duo_' + self.j + self.k)
        self.pivot_tij = getattr(tau, 'pivot_tij_' + ranking)
        self.pivot_tjk = getattr(tau, 'pivot_tjk_' + ranking)
        self.trio_1t = getattr(tau, 'trio_1t_' + self.i)
        self.trio_2t = getattr(tau, 'trio_2t_' + self.i + self.j)
        self.trio = getattr(tau, 'trio')
        self.tau_has_two_consecutive_zeros = tau.has_two_consecutive_zeros

    @cached_property
    def results_asymptotic_method(self):
        """tuple (threshold_utility, justification)

        Results according to the asymptotic method. Cf. :attr:`threshold_utility` and :attr:`justification`.
        The threshold utility may be NaN, because this method is not always sufficient.
        """
        threshold_utility = ((
            self.pivot_tij.asymptotic * (1 / 2)
            + self.trio_1t.asymptotic * (1 / 3) + self.trio_2t.asymptotic * (1 / 6)
        ) / (
            self.pivot_tij.asymptotic * (1 / 2) + self.pivot_tjk.asymptotic * (1 / 2)
            + self.trio_1t.asymptotic * (2 / 3) + self.trio_2t.asymptotic * (1 / 3)
        )).limit
        justification = self.ASYMPTOTIC
        return threshold_utility, justification

    @cached_property
    def psi_i(self):
        """Number or NaN

        "Pseudo-offset" for ballot `i`. Is equal to ``phi_i`` if it exists, and ``phi_ij * phi_ik``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_i = getattr(self.trio, 'phi_' + self.i)
        if isnan(phi_i):
            phi_i = (getattr(self.trio, 'phi_' + self.i + self.j)
                     * getattr(self.trio, 'phi_' + self.i + self.k))
        return phi_i

    @cached_property
    def psi_j(self):
        """Number or NaN

        "Pseudo-offset" for ballot `j`. Is equal to ``phi_j`` if it exists, and ``phi_ij * phi_jk``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_j = getattr(self.trio, 'phi_' + self.j)
        if isnan(phi_j):
            phi_j = (getattr(self.trio, 'phi_' + self.j + self.i)
                     * getattr(self.trio, 'phi_' + self.j + self.k))
        return phi_j

    @cached_property
    def psi_k(self):
        """Number or NaN

        "Pseudo-offset" for ballot `k`. Is equal to ``phi_k`` if it exists, and ``phi_ik * phi_jk``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_k = getattr(self.trio, 'phi_' + self.k)
        if isnan(phi_k):
            phi_k = (getattr(self.trio, 'phi_' + self.k + self.i)
                     * getattr(self.trio, 'phi_' + self.k + self.j))
        return phi_k

    @cached_property
    def psi_ij(self):
        """Number or NaN

        "Pseudo-offset" for ballot `ij`. Is equal to ``phi_ij`` if it exists, and ``phi_i * phi_j``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_ij = getattr(self.trio, 'phi_' + self.i + self.j)
        if isnan(phi_ij):
            phi_ij = getattr(self.trio, 'phi_' + self.i) * getattr(self.trio, 'phi_' + self.j)
        return phi_ij

    @cached_property
    def psi_ik(self):
        """Number or NaN

        "Pseudo-offset" for ballot `ik`. Is equal to ``phi_ik`` if it exists, and ``phi_i * phi_k``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_ik = getattr(self.trio, 'phi_' + self.i + self.k)
        if isnan(phi_ik):
            phi_ik = getattr(self.trio, 'phi_' + self.i) * getattr(self.trio, 'phi_' + self.k)
        return phi_ik

    @cached_property
    def psi_jk(self):
        """Number or NaN

        "Pseudo-offset" for ballot `jk`. Is equal to ``phi_jk`` if it exists, and ``phi_j * phi_k``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_jk = getattr(self.trio, 'phi_' + self.j + self.k)
        if isnan(phi_jk):
            phi_jk = getattr(self.trio, 'phi_' + self.j) * getattr(self.trio, 'phi_' + self.k)
        return phi_jk

    @cached_property
    def results_limit_pivot_theorem(self):
        """tuple (threshold_utility, justification)

        Results according to the limit pivot theorem. Cf. :attr:`threshold_utility` and :attr:`justification`.
        If :attr:`self.tau_has_two_consecutive_zeros` is True, the theorem does not apply and this method returns
        ``nan, ''``.
        """
        # print('Entering results_limit_pivot_theorem...')
        # print('ranking=%s' % self.ranking)
        if self.tau_has_two_consecutive_zeros:
            return np.nan, ''

        def multiply(tau_something, phi_something):
            return 0 if tau_something == 0 else tau_something * phi_something

        # Pivot ij
        # --------
        score_ij_in_duo_ij = (multiply(self.tau_i, getattr(self.duo_ij, 'phi_' + self.i))
                              + multiply(self.tau_ij, getattr(self.duo_ij, 'phi_' + self.i + self.j))
                              + multiply(self.tau_ik, getattr(self.duo_ij, 'phi_' + self.i + self.k)))
        # BEGIN TODO: Remove the check with *_alt
        score_ij_in_duo_ij_alt = (multiply(self.tau_j, getattr(self.duo_ij, 'phi_' + self.j))
                                  + multiply(self.tau_ij, getattr(self.duo_ij, 'phi_' + self.i + self.j))
                                  + multiply(self.tau_jk, getattr(self.duo_ij, 'phi_' + self.j + self.k)))
        # print('score_ij_in_duo_ij')
        # print(score_ij_in_duo_ij)
        # print(score_ij_in_duo_ij_alt)
        assert isclose(score_ij_in_duo_ij, score_ij_in_duo_ij_alt)
        # END TODO
        score_k_in_duo_ij = (multiply(self.tau_k, getattr(self.duo_ij, 'phi_' + self.k))
                             + multiply(self.tau_ik, getattr(self.duo_ij, 'phi_' + self.i + self.k))
                             + multiply(self.tau_jk, getattr(self.duo_ij, 'phi_' + self.j + self.k)))
        # print('score_k_in_duo_ij')
        # print(score_k_in_duo_ij)
        pivot_ij_easy = score_ij_in_duo_ij > score_k_in_duo_ij
        pivot_ij_tight = isclose(score_ij_in_duo_ij, score_k_in_duo_ij)
        pivot_ij_easy_or_tight = pivot_ij_easy or pivot_ij_tight
        # Pivot jk
        # --------
        score_jk_in_duo_jk = (multiply(self.tau_j, getattr(self.duo_jk, 'phi_' + self.j))
                              + multiply(self.tau_ij, getattr(self.duo_jk, 'phi_' + self.i + self.j))
                              + multiply(self.tau_jk, getattr(self.duo_jk, 'phi_' + self.j + self.k)))
        # BEGIN TODO: Remove the check with *_alt
        score_jk_in_duo_jk_alt = (multiply(self.tau_k, getattr(self.duo_jk, 'phi_' + self.k))
                                  + multiply(self.tau_ik, getattr(self.duo_jk, 'phi_' + self.i + self.k))
                                  + multiply(self.tau_jk, getattr(self.duo_jk, 'phi_' + self.j + self.k)))
        # print('score_jk_in_duo_jk')
        # print(score_jk_in_duo_jk)
        # print(score_jk_in_duo_jk_alt)
        assert isclose(score_jk_in_duo_jk, score_jk_in_duo_jk_alt)
        # END TODO
        score_i_in_duo_jk = (multiply(self.tau_i, getattr(self.duo_jk, 'phi_' + self.i))
                             + multiply(self.tau_ij, getattr(self.duo_jk, 'phi_' + self.i + self.j))
                             + multiply(self.tau_ik, getattr(self.duo_jk, 'phi_' + self.i + self.k)))
        # print('score_i_in_duo_jk')
        # print(score_i_in_duo_jk)
        pivot_jk_easy = score_jk_in_duo_jk > score_i_in_duo_jk
        pivot_jk_tight = isclose(score_jk_in_duo_jk, score_i_in_duo_jk)
        pivot_jk_easy_or_tight = pivot_jk_easy or pivot_jk_tight
        # Case distinction of the theorem
        # -------------------------------
        if pivot_ij_easy_or_tight and pivot_jk_easy_or_tight:
            # Both pivots are easy: we can forget the trios
            threshold_utility = ((
                self.pivot_tij.asymptotic * (1 / 2)
            ) / (
                self.pivot_tij.asymptotic * (1 / 2) + self.pivot_tjk.asymptotic * (1 / 2)
            )).limit
            justification = self.ASYMPTOTIC_SIMPLIFIED
        elif pivot_ij_easy_or_tight:
            # Pivot ij is easy or tight, pivot jk is difficult
            threshold_utility = 1
            justification = self.EASY_VS_DIFFICULT
        elif pivot_jk_easy_or_tight:
            # Pivot jk is easy or tight, pivot ij is difficult
            threshold_utility = 0
            justification = self.DIFFICULT_VS_EASY
        else:
            # Both pivots are difficult -> General case of the offset method
            pij = (1 + self.psi_ik) / (1 - self.psi_k)
            pjk = (1 + self.psi_j) * self.psi_i ** 2 / (1 - self.psi_i)
            p1t = self.psi_i
            p2t = self.psi_ij
            threshold_utility = (pij / 2 + p1t / 3 + p2t / 6) / (pij / 2 + pjk / 2 + p1t * 2 / 3 + p2t / 3)
            justification = self.OFFSET_METHOD
        return threshold_utility, justification

    @cached_property
    def results(self):
        """tuple (threshold_utility, justification)

        Cf. :attr:`threshold_utility` and :attr:`justification`. Results that use the asymptotic method if possible
        (better numerical approximation, but does not always provide the threshold utility), and the limit pivot
        theorem otherwise. The limit pivot theorem may not give a result when there are two consecutive holes in the
        "compass diagram", but this kind of case is covered by the asymptotic method.
        """
        threshold_utility, justification = self.results_asymptotic_method
        if isnan(threshold_utility):
            threshold_utility, justification = self.results_limit_pivot_theorem
        return threshold_utility, justification

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
        Historically, it could also be ``'inconclusive'``, but this value is not used anymore in the current version
        of the algorithm.
        """
        if isnan(self.threshold_utility):
            ballot = INCONCLUSIVE  # pragma: no cover
            raise ValueError('Unable to compute threshold utility')  # pragma: no cover
        elif isclose(self.threshold_utility, 1):
            ballot = ballot_one(self.ranking)
        elif isclose(self.threshold_utility, 0, abs_tol=1E-9):
            ballot = ballot_one_two(self.ranking)
        else:
            ballot = UTILITY_DEPENDENT
        return ballot

    def __repr__(self):
        return '<' + ', '.join([
            'ballot = %s' % self.ballot,
            'threshold_utility = {:.6g}'.format(self.threshold_utility),
            'justification = %s' % self.justification,
            'pivot_tij = %s' % self.pivot_tij.asymptotic,
            'pivot_tjk = %s' % self.pivot_tjk.asymptotic,
            'trio_1t = %s' % self.trio_1t.asymptotic,
            'trio_2t = %s' % self.trio_2t.asymptotic,
            'trio = %s' % self.trio.asymptotic,
        ]) + '>'
