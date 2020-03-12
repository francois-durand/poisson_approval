from fractions import Fraction
from poisson_approval import TauVector, BestResponseApproval, PLURALITY, ANTI_PLURALITY


def test_normalization():
    tau = TauVector({'a': 1, 'b': 1})
    assert tau.a == 0.5


def test_easy_vs_difficult_pivot():
    tau = TauVector({'a': Fraction(1, 3), 'ab': Fraction(1, 3), 'b': Fraction(1, 6), 'c': Fraction(1, 6)})
    assert tau.d_ranking_best_response['acb'].ballot == 'a'
    assert tau.d_ranking_best_response['acb'].justification == BestResponseApproval.EASY_VS_DIFFICULT
    assert tau.d_ranking_best_response['bca'].ballot == 'bc'
    assert tau.d_ranking_best_response['bca'].justification == BestResponseApproval.DIFFICULT_VS_EASY


def test_scores_in_duos():
    """
        >>> tau = TauVector({'a': Fraction(1, 10), 'ab': Fraction(3, 5), 'c': Fraction(3, 10)})
        >>> tau.score_ba_in_duo_ba
        Fraction(3, 5)
        >>> tau.score_ca_in_duo_ca
        0.45825756949558394
        >>> tau.score_cb_in_duo_cb
        0.4242640687119285
        >>> tau.score_c_in_duo_ba
        Fraction(3, 10)
        >>> tau.score_b_in_duo_ca
        0.39279220242478624
        >>> tau.score_a_in_duo_cb
        0.5242640687119285
    """


def test_tau_plurality():
    """
        >>> tau = TauVector({'a': Fraction(2, 5), 'b': Fraction(2, 5), 'c': Fraction(1, 5)}, voting_rule=PLURALITY)
        >>> tau
        TauVector({'a': Fraction(2, 5), 'b': Fraction(2, 5), 'c': Fraction(1, 5)}, voting_rule='Plurality')
        >>> tau.d_ranking_best_response
        {'abc': <ballot = a, threshold_utility = 1, justification = Plurality analysis>, \
'acb': <ballot = a, threshold_utility = 1, justification = Plurality analysis>, \
'bac': <ballot = b, threshold_utility = 1, justification = Plurality analysis>, \
'bca': <ballot = b, threshold_utility = 1, justification = Plurality analysis>, \
'cab': <ballot = a, threshold_utility = 0, justification = Plurality analysis>, \
'cba': <ballot = b, threshold_utility = 0, justification = Plurality analysis>}
    """
    pass


def test_tau_anti_plurality():
    """
        >>> tau = TauVector({'ab': Fraction(2, 5), 'ac': Fraction(2, 5), 'bc': Fraction(1, 5)},
        ...                 voting_rule=ANTI_PLURALITY)
        >>> tau
        TauVector({'ab': Fraction(2, 5), 'ac': Fraction(2, 5), 'bc': Fraction(1, 5)}, voting_rule='Anti-plurality')
        >>> tau.d_ranking_best_response
        {'abc': <ballot = ab, threshold_utility = 0, justification = Anti-plurality analysis>, \
'acb': <ballot = ac, threshold_utility = 0, justification = Anti-plurality analysis>, \
'bac': <ballot = utility-dependent, threshold_utility = 0.5, justification = Anti-plurality analysis>, \
'bca': <ballot = bc, threshold_utility = 0, justification = Anti-plurality analysis>, \
'cab': <ballot = utility-dependent, threshold_utility = 0.5, justification = Anti-plurality analysis>, \
'cba': <ballot = bc, threshold_utility = 0, justification = Anti-plurality analysis>}
    """
    pass


def test_unfocused():
    """
        >>> tau = TauVector({'a': 1})
        >>> tau.focus
        Focus.UNFOCUSED
    """
    pass


def test_backward_focused():
    """
        >>> tau = TauVector({'ab': Fraction(1, 2), 'ac': Fraction(1, 2)})
        >>> tau.focus
        Focus.BACKWARD_FOCUSED
    """
    pass
