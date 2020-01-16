from fractions import Fraction
from poisson_approval import TauVector, BestResponse


def test():
    # Test if normalization works as expected
    tau = TauVector({'a': 1, 'b': 1})
    assert tau.a == 0.5

    # Test a case where the justification is easy vs difficult pivot (or the contrary)
    tau = TauVector({'a': Fraction(1, 3), 'ab': Fraction(1, 3), 'b': Fraction(1, 6), 'c': Fraction(1, 6)})
    assert tau.d_ranking_best_response['acb'].ballot == 'a'
    assert tau.d_ranking_best_response['bca'].ballot == 'bc'
