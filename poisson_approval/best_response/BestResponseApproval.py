from poisson_approval.best_response.BestResponse import BestResponse
from poisson_approval.constants.constants import *
from poisson_approval.utils.UtilCache import cached_property


class BestResponseApproval(BestResponse):
    """Best response for a given ordinal type of voter in Approval voting.

    The main objective of this class is to compute :attr:`threshold_utility`.

    It also provides the string :attr:`justification`, indicating which sub-algorithm was used. Nowadays, possible
    values are ``'Asymptotic method'``, ``'Simplified asymptotic method'``, ``'Easy vs difficult pivot'``,
    ``'Difficult vs easy pivot'``, ``'Offset method'``, ``'Offset method with trio approximation correction'``.

    Parameters
    ----------
    Cf. :class:`BestResponse`.

    Attributes
    ----------
    Cf. :class:`BestResponse`
    """

    ASYMPTOTIC = 'Asymptotic method'
    ASYMPTOTIC_SIMPLIFIED = 'Simplified asymptotic method'
    EASY_VS_DIFFICULT = 'Easy vs difficult pivot'
    DIFFICULT_VS_EASY = 'Difficult vs easy pivot'
    OFFSET_METHOD = 'Offset method'
    OFFSET_METHOD_WITH_TRIO_APPROXIMATION_CORRECTION = 'Offset method with trio approximation correction'

    voting_rule = APPROVAL

    # =======
    # Results
    # =======

    @cached_property
    def results_asymptotic_method(self):
        """tuple (threshold_utility, justification) : Results according to the asymptotic method. Cf.
        :attr:`threshold_utility` and :attr:`justification`. The threshold utility may be NaN, because this method is
        not always sufficient.
        """
        threshold_utility = self.ce.simplify(((
            self.pivot_tij.asymptotic * self.ce.Rational(1, 2)
            + self.trio_1t.asymptotic * self.ce.Rational(1, 3)
            + self.trio_2t.asymptotic * self.ce.Rational(1, 6)
        ) / (
            self.pivot_tij.asymptotic * self.ce.Rational(1, 2)
            + self.pivot_tjk.asymptotic * self.ce.Rational(1, 2)
            + self.trio_1t.asymptotic * self.ce.Rational(2, 3)
            + self.trio_2t.asymptotic * self.ce.Rational(1, 3)
        )).limit)
        justification = self.ASYMPTOTIC
        return threshold_utility, justification

    @cached_property
    def results_limit_pivot_theorem(self):
        """tuple (threshold_utility, justification) : Results according to the limit pivot theorem.
        Cf. :attr:`threshold_utility` and :attr:`justification`. If the tau-vector has two consecutive zeros, the
        theorem does not apply and this method returns ``nan, ''``.
        """
        if self.tau.has_two_consecutive_zeros:
            return self.ce.nan, ''
        if self.pivot_ij_easy_or_tight and self.pivot_jk_easy_or_tight:
            # Both pivots are easy => We can forget the trios.
            threshold_utility = self.ce.simplify(((
                self.pivot_tij.asymptotic * self.ce.Rational(1, 2)
            ) / (
                self.pivot_tij.asymptotic * self.ce.Rational(1, 2)
                + self.pivot_tjk.asymptotic * self.ce.Rational(1, 2)
            )).limit)
            justification = self.ASYMPTOTIC_SIMPLIFIED
        elif self.pivot_ij_easy_or_tight:
            # ... but pivot jk is difficult.
            threshold_utility = self.ce.S(1)
            justification = self.EASY_VS_DIFFICULT
        elif self.pivot_jk_easy_or_tight:
            # ... but pivot ij is difficult.
            threshold_utility = self.ce.S(0)
            justification = self.DIFFICULT_VS_EASY
        else:
            # Both pivots are difficult => offset method.
            # Due to approximations in trio event, psi_k and psi_i may exceptionally be greater than 1 (whereas
            # in difficult pivots, we know that they must be strictly lower than 1). In that case, the formulas
            # for the offset method will fail, so we must be cautious.
            # EDIT: since release 0.23.0, this should not happen, because EventTrio is safer. But the following
            # precautions don't hurt...
            psi_k_greater_but_close_to_one = False
            if self.trio.psi[self.k] >= 1:  # pragma: no cover
                if self.ce.look_equal(self.trio.psi[self.k], 1, rel_tol=1e-1):
                    psi_k_greater_but_close_to_one = True
                else:  # pragma: no cover
                    raise AssertionError('Unexpected: self.trio.psi[self.k] = %s > 1' % self.trio.psi[self.k])
            psi_i_greater_but_close_to_one = False
            if self.trio.psi[self.i] >= 1:  # pragma: no cover
                if self.ce.look_equal(self.trio.psi[self.i], 1, rel_tol=1e-1):
                    psi_i_greater_but_close_to_one = True
                else:  # pragma: no cover
                    raise AssertionError('Unexpected: self.trio.psi[self.i] = %s > 1' % self.trio.psi[self.i])
            if psi_i_greater_but_close_to_one and psi_k_greater_but_close_to_one:  # pragma: no cover
                raise AssertionError('Unexpected: both psi_i and psi_k are greater and close to 1.')
            elif psi_k_greater_but_close_to_one:  # pragma: no cover
                # pij ~= inf, pjk < inf ==> u = 1
                threshold_utility = self.ce.S(1)
                justification = self.OFFSET_METHOD_WITH_TRIO_APPROXIMATION_CORRECTION
            elif psi_i_greater_but_close_to_one:  # pragma: no cover
                # pij < inf, pjk ~= inf ==> u = 0
                threshold_utility = self.ce.S(0)
                justification = self.OFFSET_METHOD_WITH_TRIO_APPROXIMATION_CORRECTION
            else:
                # General case of the offset method (at last!)
                pij = (1 + self.trio.psi[self.ik]) / (1 - self.trio.psi[self.k])
                pjk = (1 + self.trio.psi[self.j]) * self.trio.psi[self.i] ** 2 / (1 - self.trio.psi[self.i])
                p1t = self.trio.psi[self.i]
                p2t = self.trio.psi[self.ij]
                threshold_utility = self.ce.simplify((pij / 2 + p1t / 3 + p2t / 6)
                                                     / (pij / 2 + pjk / 2 + p1t * 2 / 3 + p2t / 3))
                justification = self.OFFSET_METHOD
        return threshold_utility, justification

    @cached_property
    def results(self):
        """tuple (threshold_utility, justification) : Cf. :attr:`threshold_utility` and :attr:`justification`.
        These results use:

        * :meth:`results_asymptotic_method` if there are two consecutive zeros in the "compass diagram" of the
          tau-vector,
        * :meth:`results_limit_pivot_theorem` otherwise.
        """
        if self.tau.has_two_consecutive_zeros:
            return self.results_asymptotic_method
        else:
            return self.results_limit_pivot_theorem
