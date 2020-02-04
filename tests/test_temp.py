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
        <ballot = a, threshold_utility = 1, justification = Easy vs difficult pivot, pivot_tij = exp(- 0.057191 n - 0.5 log n - 0.354693 + o(1)), pivot_tjk = exp(- 0.333333 n - log n - 2.10515 + o(1)), trio_1t = exp(- 0.333333 n - log n - 1.81747 + o(1)), trio_2t = exp(- 0.333333 n - log n - 2.51061 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
        <ballot = utility-dependent, threshold_utility = 0.610526, justification = Offset method, pivot_tij = exp(- 0.333333 n - log n + 0.128444 + o(1)), pivot_tjk = exp(- 0.333333 n - log n - 0.564703 + o(1)), trio_1t = exp(- 0.333333 n - log n - 1.81747 + o(1)), trio_2t = exp(- 0.333333 n - log n - 0.0257066 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
        <ballot = b, threshold_utility = 1, justification = Easy vs difficult pivot, pivot_tij = exp(- 0.057191 n - 0.5 log n - 0.00811919 + o(1)), pivot_tjk = exp(- 0.333333 n - log n - 1.12432 + o(1)), trio_1t = exp(- 0.333333 n - log n - 1.412 + o(1)), trio_2t = exp(- 0.333333 n - log n - 2.51061 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
        <ballot = utility-dependent, threshold_utility = 0.389474, justification = Offset method, pivot_tij = exp(- 0.333333 n - log n - 0.159238 + o(1)), pivot_tjk = exp(- 0.333333 n - log n + 0.533909 + o(1)), trio_1t = exp(- 0.333333 n - log n - 1.412 + o(1)), trio_2t = exp(- 0.333333 n - log n + 0.379759 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
        <ballot = ac, threshold_utility = 0, justification = Difficult vs easy pivot, pivot_tij = exp(- 0.333333 n - log n + 1.36059 + o(1)), pivot_tjk = exp(- 0.057191 n - 0.5 log n - 0.354693 + o(1)), trio_1t = exp(- 0.333333 n - log n + 1.07291 + o(1)), trio_2t = exp(- 0.333333 n - log n - 0.0257066 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
        <ballot = bc, threshold_utility = 0, justification = Difficult vs easy pivot, pivot_tij = exp(- 0.333333 n - log n + 0.785224 + o(1)), pivot_tjk = exp(- 0.057191 n - 0.5 log n - 0.00811919 + o(1)), trio_1t = exp(- 0.333333 n - log n + 1.07291 + o(1)), trio_2t = exp(- 0.333333 n - log n + 0.379759 + o(1)), trio = exp(- 0.333333 n - log n - 0.718854 + o(1))>
    """
    tau = TauVector({'a': 0.24382716330832704, 'ab': 0.0011384657401753433,
                     'ac': 0.25507268421895707, 'b': 0.2550449552509131,
                     'bc': 0.24379357320990255, 'c': 0.001123158271724989})
    # assert 0 <= tau.d_ranking_best_response['cab'].threshold_utility <= 1
