import math
from poisson_approval.tau_vector.TauVector import TauVector
from poisson_approval.constants.Focus import Focus
from fractions import Fraction


class ExploreGridTaus:
    """Explore a grid of tau-vectors.

    Parameters
    ----------
    denominator : int or list of int
        The grain of the grid. For example, if ``denominator=9``, we examine tau-vectors such as
        (1/9, 2/9, 2/9, 1/9, 1/3, 0) or (1/9, 5/9, 0, 3/9, 0, 0), etc. If a list of integers is given, then all the
        corresponding denominators are examined.
    test : callable
        A function ``TauVector -> bool``. Only the tau-vectors satisfying this test will be examined.
        Default: always True.
    standardized : bool
        If True, then we examine only the standardized tau-vectors (i.e. up to relabelling the candidates).
        Cf. :attr:`TauVector.is_standardized`.

    Examples
    --------
        >>> def test(tau):
        ...     return tau.focus == Focus.DIRECT
        >>> exploration = ExploreGridTaus(denominator=6, test=test)
        >>> exploration
        <a: 1/3, ab: 1/6, bc: 1/2> ==> b
        <a: 1/3, b: 1/6, bc: 1/2> ==> b
        <a: 1/3, ab: 1/6, ac: 1/3, b: 1/6> ==> a
        <a: 1/3, ac: 1/6, b: 1/3, c: 1/6> ==> a
        <a: 1/2, ab: 1/3, ac: 1/6> ==> a
        <a: 1/2, ac: 1/3, b: 1/6> ==> a
        <a: 1/2, ab: 1/6, b: 1/6, c: 1/6> ==> a
        >>> print(exploration[0])
        <a: 1/3, ab: 1/6, bc: 1/2> ==> b
    """

    def __init__(self, denominator, test=None, standardized=True):
        if type(denominator) == int:
            denominators = [denominator]
        else:
            denominators = denominator
        if test is None:
            def test(_):
                return True
        self.taus = []
        for d in denominators:
            tau_1_min = int(math.ceil(d / 6)) if standardized else 0
            for tau_1 in range(tau_1_min, d + 1):
                tau_2_max = d - tau_1
                if standardized:
                    tau_2_max = min(tau_1, tau_2_max)
                for tau_2 in range(0, tau_2_max + 1):
                    tau_3_max = d - tau_1 - tau_2
                    if standardized:
                        tau_3_max = min(tau_1, tau_3_max)
                    for tau_3 in range(0, tau_3_max + 1):
                        tau_4_max = d - tau_1 - tau_2 - tau_3
                        if standardized:
                            tau_4_max = min(tau_1, tau_4_max)
                        for tau_4 in range(0, tau_4_max + 1):
                            tau_5_max = d - tau_1 - tau_2 - tau_3 - tau_4
                            if standardized:
                                tau_5_max = min(tau_1, tau_5_max)
                            for tau_5 in range(0, tau_5_max + 1):
                                tau_6 = (
                                    d - tau_1 - tau_2 - tau_3 - tau_4 - tau_5)
                                tau = TauVector({
                                    'a': Fraction(tau_1, d),
                                    'b': Fraction(tau_2, d),
                                    'c': Fraction(tau_3, d),
                                    'ab': Fraction(tau_4, d),
                                    'ac': Fraction(tau_5, d),
                                    'bc': Fraction(tau_6, d)
                                })
                                if standardized and not tau.is_standardized:
                                    continue
                                if not test(tau):
                                    continue
                                self.taus.append(tau)

    def __getitem__(self, item):
        return self.taus[item]

    def __repr__(self):
        return '\n'.join([str(tau) for tau in self.taus])
