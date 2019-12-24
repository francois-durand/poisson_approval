from math import isclose
from poisson_approval.utils.Util import isnan, ballot_one, ballot_one_two
from poisson_approval.constants.constants import *


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

    Attributes
    ----------
    ballot : str
        This can be a valid ballot (e.g. ``'a'`` or ``'ab'`` if `ranking` is ``'abc'``) or ``'utility-dependent'``.
        Historically, it could also be ``'inconclusive'``, but this value is not used anymore in the current version
        of the algorithm.
    threshold_utility : Number
        The threshold value of the utility for the second candidate (where the optimal ballot changes). If 1, then
        always vote for the first candidate. If 0, then always vote for the two most-liked candidates.
    justification : str
        How the program made its decision. Nowadays, possible values are ``'Asymptotic method'``,
        ``'Simplified asymptotic method'``, ``'Easy vs difficult pivot'``, ``'Difficult vs easy pivot'``,
        ``'Offset method'``.

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
        # -------------
        # Preliminaries
        # -------------
        self.ranking = ranking
        self.pivot_tij = pivot_tij
        self.pivot_tjk = pivot_tjk
        self.trio_1t = trio_1t
        self.trio_2t = trio_2t
        self.trio = trio
        # -----------
        # Actual work
        # -----------
        self.threshold_utility = ((
            pivot_tij.asymptotic * (1 / 2)
            + trio_1t.asymptotic * (1 / 3) + trio_2t.asymptotic * (1 / 6)
        ) / (
            pivot_tij.asymptotic * (1 / 2) + pivot_tjk.asymptotic * (1 / 2)
            + trio_1t.asymptotic * (2 / 3) + trio_2t.asymptotic * (1 / 3)
        )).limit
        self.justification = self.ASYMPTOTIC
        if isnan(self.threshold_utility):
            phi_i = getattr(trio, 'phi_' + ranking[0])
            if isnan(phi_i):
                phi_i = (getattr(trio, 'phi_' + ranking[0] + ranking[1])
                         * getattr(trio, 'phi_' + ranking[0] + ranking[2]))
            phi_j = getattr(trio, 'phi_' + ranking[1])
            if isnan(phi_j):
                phi_j = (getattr(trio, 'phi_' + ranking[1] + ranking[0])
                         * getattr(trio, 'phi_' + ranking[1] + ranking[2]))
            phi_k = getattr(trio, 'phi_' + ranking[2])
            if isnan(phi_k):
                phi_k = (getattr(trio, 'phi_' + ranking[2] + ranking[0])
                         * getattr(trio, 'phi_' + ranking[2] + ranking[1]))
            phi_ij = getattr(trio, 'phi_' + ranking[0] + ranking[1])
            if isnan(phi_ij):
                phi_ij = getattr(trio, 'phi_' + ranking[0]) * getattr(trio, 'phi_' + ranking[1])
            phi_ik = getattr(trio, 'phi_' + ranking[0] + ranking[2])
            if isnan(phi_ik):
                phi_ik = getattr(trio, 'phi_' + ranking[0]) * getattr(trio, 'phi_' + ranking[2])
            phi_i_ge_1 = (isclose(phi_i, 1) or phi_i >= 1)
            phi_k_ge_1 = (isclose(phi_k, 1) or phi_k >= 1)
            if phi_i_ge_1 and phi_k_ge_1:
                # Both pivots are easy: we can forget the trios
                self.threshold_utility = ((
                    pivot_tij.asymptotic * (1 / 2)
                ) / (
                    pivot_tij.asymptotic * (1 / 2) + pivot_tjk.asymptotic * (1 / 2)
                )).limit
                self.justification = self.ASYMPTOTIC_SIMPLIFIED
            elif phi_i_ge_1:
                # Pivot jk is difficult, pivot ij is easy
                self.threshold_utility = 0
                self.justification = self.EASY_VS_DIFFICULT
            elif phi_k_ge_1:
                # Pivot ij is difficult, pivot jk is easy
                self.threshold_utility = 1
                self.justification = self.DIFFICULT_VS_EASY
            else:
                # Both pivots are difficult -> General case of the offset method
                pij = (1 + phi_ik) / (1 - phi_k)
                pjk = (1 + phi_j) * phi_i**2 / (1 - phi_i)
                p1t = phi_i
                p2t = phi_ij
                self.threshold_utility = (pij / 2 + p1t / 3 + p2t / 6) / (pij / 2 + pjk / 2 + p1t * 2 / 3 + p2t / 3)
                self.justification = self.OFFSET_METHOD
        if isnan(self.threshold_utility):
            self.ballot = INCONCLUSIVE
            raise ValueError('Unable to compute threshold utility')
        elif isclose(self.threshold_utility, 1):
            self.ballot = ballot_one(ranking)
        elif isclose(self.threshold_utility, 0):
            self.ballot = ballot_one_two(ranking)
        else:
            self.ballot = UTILITY_DEPENDENT

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
