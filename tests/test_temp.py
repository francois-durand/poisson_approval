from math import log
from poisson_approval import *


def test():
    """
        >>> tau = TauVector({'a': 9/15, 'b': 4/15, 'ac': 1/15, 'bc': 1/15})
        >>> best_response = BestResponse(tau, 'abc')
        >>> best_response.ballot
        'a'
        >>> best_response.threshold_utility
        1
        >>> for ranking in RANKINGS:
        ...     print(BestResponse(tau, ranking))
        <ballot = a, threshold_utility = 1, justification = Easy vs difficult pivot>
        <ballot = utility-dependent, threshold_utility = 0.610526, justification = Offset method>
        <ballot = b, threshold_utility = 1, justification = Easy vs difficult pivot>
        <ballot = utility-dependent, threshold_utility = 0.389474, justification = Offset method>
        <ballot = ac, threshold_utility = 0, justification = Difficult vs easy pivot>
        <ballot = bc, threshold_utility = 0, justification = Difficult vs easy pivot>
    """
    tau = TauVector({'a': 0.24382716330832704, 'ab': 0.0011384657401753433,
                     'ac': 0.25507268421895707, 'b': 0.2550449552509131,
                     'bc': 0.24379357320990255, 'c': 0.001123158271724989})
    assert 0 <= tau.d_ranking_best_response['cab'].threshold_utility <= 1
