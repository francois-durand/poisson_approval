from fractions import Fraction
from poisson_approval import TauVector, BestResponse


def test_normalization():
    tau = TauVector({'a': 1, 'b': 1})
    assert tau.a == 0.5


def test_easy_vs_difficult_pivot():
    tau = TauVector({'a': Fraction(1, 3), 'ab': Fraction(1, 3), 'b': Fraction(1, 6), 'c': Fraction(1, 6)})
    assert tau.d_ranking_best_response['acb'].ballot == 'a'
    assert tau.d_ranking_best_response['acb'].justification == BestResponse.EASY_VS_DIFFICULT
    assert tau.d_ranking_best_response['bca'].ballot == 'bc'
    assert tau.d_ranking_best_response['bca'].justification == BestResponse.DIFFICULT_VS_EASY
