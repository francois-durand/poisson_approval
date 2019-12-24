import math
from poisson_approval.profiles.ProfileOrdinal import ProfileOrdinal
from poisson_approval.utils.Util import give_figure
from fractions import Fraction


class ExploreGridProfilesOrdinal:
    """Explore a grid of ordinal profiles and analyze each profile.

    Parameters
    ----------
    denominator : int or list of int
        The grain of the grid. For example, if ``denominator=9``, we examine profiles such as
        (1/9, 2/9, 2/9, 1/9, 1/3, 0) or (1/9, 5/9, 0, 3/9, 0, 0), etc. If a list of integers is given, then all the
        corresponding denominators are examined.
    test : callable
        A function ``ProfileOrdinal -> bool``. Only the profiles satisfying this test will be examined.
        Default: always True.
    standardized : bool
        If True, then we examine only the `standardized` profiles (i.e. up to relabelling the candidates).
        Cf. :attr:`Profile.is_standardized`.
    well_informed_voters : bool
        Cf. the corresponding parameter in :class:`Profile`.

    Examples
    --------
        >>> def test(r):
        ...     return(
        ...         r.is_profile_condorcet
        ...         and len(r.analyzed_strategies.utility_dependent) > 0
        ...     )
        >>> exploration = ExploreGridProfilesOrdinal(denominator=3, test=test)
        >>> exploration
        0 equilibrium, 1 utility-dependent equilibrium, 3 non-equilibria
        <abc: 2/3, cab: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 1 utility-dependent equilibrium, 7 non-equilibria
        <abc: 1/3, acb: 1/3, bac: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 2 utility-dependent equilibria, 2 non-equilibria
        <abc: 2/3, cba: 1/3> (Condorcet winner: a)
        <abc: 2/3, bca: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 3 utility-dependent equilibria, 5 non-equilibria
        <abc: 1/3, acb: 1/3, bca: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        2 equilibria, 1 utility-dependent equilibrium, 5 non-equilibria
        <abc: 1/3, bac: 1/3, cab: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        >>> r = exploration[(0, 1, 3)][0]
        >>> print(r)
        <abc: 2/3, cab: 1/3> (Condorcet winner: a)

    If the test breaks the symmetry between candidates, you should use the option ``𝚜𝚝𝚊𝚗𝚍𝚊𝚛𝚍𝚒𝚣𝚎𝚍=𝙵𝚊𝚕𝚜𝚎``:

        >>> def test(r):
        ...     return (
        ...         'a' in r.condorcet_winners
        ...     )
        >>> exploration = ExploreGridProfilesOrdinal(test=test, denominator=2, standardized=False)
        >>> exploration
        0 equilibrium, 1 utility-dependent equilibrium, 3 non-equilibria
        <bac: 1/2, cab: 1/2> (Condorcet winner: a, b, c)
        <acb: 1/2, cba: 1/2> (Condorcet winner: a, c)
        <acb: 1/2, bca: 1/2> (Condorcet winner: a, b, c)
        <acb: 1/2, bac: 1/2> (Condorcet winner: a, b)
        <abc: 1/2, cba: 1/2> (Condorcet winner: a, b, c)
        <abc: 1/2, cab: 1/2> (Condorcet winner: a, c)
        <abc: 1/2, bca: 1/2> (Condorcet winner: a, b)
        <BLANKLINE>
        1 equilibrium, 0 utility-dependent equilibrium, 1 non-equilibrium
        <acb: 1> (Condorcet winner: a)
        <abc: 1> (Condorcet winner: a)
        <BLANKLINE>
        1 equilibrium, 0 utility-dependent equilibrium, 3 non-equilibria
        <acb: 1/2, cab: 1/2> (Condorcet winner: a, c)
        <abc: 1/2, bac: 1/2> (Condorcet winner: a, b)
        <abc: 1/2, acb: 1/2> (Condorcet winner: a)
        <BLANKLINE>
    """

    def __init__(self, denominator, test=None, standardized=True, well_informed_voters=True):
        if type(denominator) == int:
            denominators = [denominator]
        else:
            denominators = denominator
        if test is None:
            def test(_):
                return True
        self.d_stats_profiles = dict()
        for d in denominators:
            r_abc_min = int(math.ceil(d / 6)) if standardized else 0
            for r_abc in range(r_abc_min, d + 1):
                r_acb_max = d - r_abc
                if standardized:
                    r_acb_max = min(r_abc, r_acb_max)
                for r_acb in range(0, r_acb_max + 1):
                    r_bac_max = d - r_abc - r_acb
                    if standardized:
                        r_bac_max = min(r_abc, r_bac_max)
                    for r_bac in range(0, r_bac_max + 1):
                        r_bca_max = d - r_abc - r_acb - r_bac
                        if standardized:
                            r_bca_max = min(r_abc, r_bca_max)
                        for r_bca in range(0, r_bca_max + 1):
                            r_cab_max = d - r_abc - r_acb - r_bac - r_bca
                            if standardized:
                                r_cab_max = min(r_abc, r_cab_max)
                            for r_cab in range(0, r_cab_max + 1):
                                r_cba = (
                                    d - r_abc - r_acb - r_bac - r_bca - r_cab)
                                r = ProfileOrdinal({
                                    'abc': Fraction(r_abc, d),
                                    'acb': Fraction(r_acb, d),
                                    'bac': Fraction(r_bac, d),
                                    'bca': Fraction(r_bca, d),
                                    'cab': Fraction(r_cab, d),
                                    'cba': Fraction(r_cba, d)
                                }, well_informed_voters=well_informed_voters)
                                if standardized and not r.is_standardized:
                                    continue
                                if not test(r):
                                    continue
                                analyzed_strat = r.analyzed_strategies
                                eq, ud, non_eq = (
                                    analyzed_strat.equilibria,
                                    analyzed_strat.utility_dependent,
                                    analyzed_strat.non_equilibria
                                )
                                stats = (len(eq), len(ud), len(non_eq))
                                if stats not in self.d_stats_profiles:
                                    self.d_stats_profiles[stats] = []
                                if r not in self.d_stats_profiles[stats]:
                                    self.d_stats_profiles[stats].append(r)

    def __getitem__(self, item):
        return self.d_stats_profiles[item]

    def items(self):
        return self.d_stats_profiles.items()

    def keys(self):
        return self.d_stats_profiles.keys()

    def values(self):
        return self.d_stats_profiles.values()

    def __repr__(self):
        s = ''
        first = True
        for key in sorted(self.d_stats_profiles):
            list_profiles = self.d_stats_profiles[key]
            if first:
                first = False
            else:
                s += '\n'
            s += give_figure(key[0], 'equilibrium', 'equilibria') + ', '
            s += give_figure(key[1], 'utility-dependent equilibrium', 'utility-dependent equilibria') + ', '
            s += give_figure(key[2], 'non-equilibrium', 'non-equilibria') + '\n'
            for profile in list_profiles:
                s += str(profile) + '\n'
        return s
