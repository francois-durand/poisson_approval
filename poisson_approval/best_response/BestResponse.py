from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.utils.Util import isnan, ballot_one, ballot_one_two
from poisson_approval.utils.UtilCache import cached_property


class BestResponse:
    """Best response for a given ordinal type of voter.

    Parameters
    ----------
    ranking : str
        Voter's ranking, e.g. ``'abc'``.
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

    Examples
    --------
        >>> from poisson_approval import EventPivotTij, EventPivotTjk, EventTrio1t, EventTrio2t, EventTrio
        >>> tau = {'tau_a': 9/15, 'tau_b': 4/15, 'tau_ac': 1/15, 'tau_bc': 1/15}
        >>> pivot_tij = EventPivotTij(candidate_x='a', candidate_y='b', candidate_z='c', **tau)
        >>> pivot_tjk = EventPivotTjk(candidate_x='c', candidate_y='b', candidate_z='a', **tau)
        >>> trio_1t = EventTrio1t(candidate_x='a', candidate_y='b', candidate_z='c', **tau)
        >>> trio_2t = EventTrio2t(candidate_x='a', candidate_y='b', candidate_z='c', **tau)
        >>> trio = EventTrio(candidate_x='a', candidate_y='b', candidate_z='c', **tau)
        >>> best_response = BestResponse('abc', pivot_tij, pivot_tjk, trio_1t, trio_2t, trio)
        >>> best_response.ballot
        'a'
        >>> best_response.threshold_utility
        1.0
    """

    ASYMPTOTIC = 'Asymptotic method'
    ASYMPTOTIC_SIMPLIFIED = 'Simplified asymptotic method'
    EASY_VS_DIFFICULT = 'Easy vs difficult pivot'
    DIFFICULT_VS_EASY = 'Difficult vs easy pivot'
    OFFSET_METHOD = 'Offset method'

    def __init__(self, ranking, pivot_tij, pivot_tjk, trio_1t, trio_2t, trio):
        self.ranking = ranking
        self.pivot_tij = pivot_tij
        self.pivot_tjk = pivot_tjk
        self.trio_1t = trio_1t
        self.trio_2t = trio_2t
        self.trio = trio

    @cached_property
    def results_asymptotic_method(self):
        """tuple (threshold_utility, justification)

        Results according to the asymptotic method. Cf. :attr:`threshold_utility` and :attr:`justification`.
        The threshold utility may be NaN, because the asymptotic method is not always sufficient.
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

        "Pseudo-offset" for ballot `i`. Is equal to the vanilla ``phi_i`` if it exists, and ``phi_ij * phi_ik``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_i = getattr(self.trio, 'phi_' + self.ranking[0])
        if isnan(phi_i):
            phi_i = (getattr(self.trio, 'phi_' + self.ranking[0] + self.ranking[1])
                     * getattr(self.trio, 'phi_' + self.ranking[0] + self.ranking[2]))
        return phi_i

    @cached_property
    def psi_j(self):
        """Number or NaN

        "Pseudo-offset" for ballot `j`. Is equal to the vanilla ``phi_j`` if it exists, and ``phi_ij * phi_jk``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_j = getattr(self.trio, 'phi_' + self.ranking[1])
        if isnan(phi_j):
            phi_j = (getattr(self.trio, 'phi_' + self.ranking[1] + self.ranking[0])
                     * getattr(self.trio, 'phi_' + self.ranking[1] + self.ranking[2]))
        return phi_j

    @cached_property
    def psi_k(self):
        """Number or NaN

        "Pseudo-offset" for ballot `k`. Is equal to the vanilla ``phi_k`` if it exists, and ``phi_ik * phi_jk``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_k = getattr(self.trio, 'phi_' + self.ranking[2])
        if isnan(phi_k):
            phi_k = (getattr(self.trio, 'phi_' + self.ranking[2] + self.ranking[0])
                     * getattr(self.trio, 'phi_' + self.ranking[2] + self.ranking[1]))
        return phi_k

    @cached_property
    def psi_ij(self):
        """Number or NaN

        "Pseudo-offset" for ballot `ij`. Is equal to the vanilla ``phi_ij`` if it exists, and ``phi_i * phi_j``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_ij = getattr(self.trio, 'phi_' + self.ranking[0] + self.ranking[1])
        if isnan(phi_ij):
            phi_ij = getattr(self.trio, 'phi_' + self.ranking[0]) * getattr(self.trio, 'phi_' + self.ranking[1])
        return phi_ij

    @cached_property
    def psi_ik(self):
        """Number or NaN

        "Pseudo-offset" for ballot `ik`. Is equal to the vanilla ``phi_ik`` if it exists, and ``phi_i * phi_k``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_ik = getattr(self.trio, 'phi_' + self.ranking[0] + self.ranking[2])
        if isnan(phi_ik):
            phi_ik = getattr(self.trio, 'phi_' + self.ranking[0]) * getattr(self.trio, 'phi_' + self.ranking[2])
        return phi_ik

    @cached_property
    def psi_jk(self):
        """Number or NaN

        "Pseudo-offset" for ballot `jk`. Is equal to the vanilla ``phi_jk`` if it exists, and ``phi_j * phi_k``
        otherwise. In particular, it is guaranteed to exist when there are not two consecutive holes in the "compass
        diagram".
        """
        phi_jk = getattr(self.trio, 'phi_' + self.ranking[1] + self.ranking[2])
        if isnan(phi_jk):
            phi_jk = getattr(self.trio, 'phi_' + self.ranking[1]) * getattr(self.trio, 'phi_' + self.ranking[2])
        return phi_jk

    @cached_property
    def results_limit_pivot_theorem(self):
        """tuple (threshold_utility, justification)

        Results according to the limit pivot theorem. Cf. :attr:`threshold_utility` and :attr:`justification`.
        The threshold utility may be NaN, because this method is not always sufficient. It is proved to compute the
        threshold utility when there are not two consecutive holes in the "compass diagram".
        """
        psi_i_ge_1 = (isclose(self.psi_i, 1) or self.psi_i >= 1)
        psi_k_ge_1 = (isclose(self.psi_k, 1) or self.psi_k >= 1)
        if psi_i_ge_1 and psi_k_ge_1:
            # Both pivots are easy: we can forget the trios
            threshold_utility = ((
                self.pivot_tij.asymptotic * (1 / 2)
            ) / (
                self.pivot_tij.asymptotic * (1 / 2) + self.pivot_tjk.asymptotic * (1 / 2)
            )).limit
            justification = self.ASYMPTOTIC_SIMPLIFIED
        elif psi_i_ge_1:
            # Pivot jk is difficult, pivot ij is easy
            threshold_utility = 0
            justification = self.EASY_VS_DIFFICULT
        elif psi_k_ge_1:
            # Pivot ij is difficult, pivot jk is easy
            threshold_utility = 1
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
