from poisson_approval import ExploreGridProfilesOrdinal


def test():
    """
        >>> exploration = ExploreGridProfilesOrdinal(denominator=[3, 4])
        >>> exploration
        0 equilibrium, 1 utility-dependent equilibrium, 3 non-equilibria
        <abc: 2/3, cab: 1/3> (Condorcet winner: a)
        <abc: 1/2, cba: 1/2> (Condorcet winner: a, b, c)
        <abc: 1/2, bca: 1/2> (Condorcet winner: a, b)
        <abc: 3/4, cab: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 1 utility-dependent equilibrium, 7 non-equilibria
        <abc: 1/3, acb: 1/3, bac: 1/3> (Condorcet winner: a)
        <abc: 1/2, bca: 1/4, cab: 1/4> (Condorcet winner: a)
        <abc: 1/2, acb: 1/4, cab: 1/4> (Condorcet winner: a)
        <abc: 1/2, acb: 1/4, bac: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 2 utility-dependent equilibria, 2 non-equilibria
        <abc: 2/3, cba: 1/3> (Condorcet winner: a)
        <abc: 2/3, bca: 1/3> (Condorcet winner: a)
        <abc: 3/4, cba: 1/4> (Condorcet winner: a)
        <abc: 3/4, bca: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 2 utility-dependent equilibria, 6 non-equilibria
        <abc: 1/3, bca: 1/3, cab: 1/3>
        <abc: 1/2, cab: 1/4, cba: 1/4> (Condorcet winner: a, c)
        <abc: 1/2, bac: 1/4, bca: 1/4> (Condorcet winner: a, b)
        <abc: 1/2, acb: 1/4, cba: 1/4> (Condorcet winner: a)
        <abc: 1/2, acb: 1/4, bca: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 3 utility-dependent equilibria, 5 non-equilibria
        <abc: 1/3, acb: 1/3, bca: 1/3> (Condorcet winner: a)
        <BLANKLINE>
        0 equilibrium, 4 utility-dependent equilibria, 12 non-equilibria
        <abc: 1/4, acb: 1/4, bac: 1/4, cba: 1/4> (Condorcet winner: a, b)
        <abc: 1/4, acb: 1/4, bac: 1/4, bca: 1/4> (Condorcet winner: a, b)
        <BLANKLINE>
        0 equilibrium, 7 utility-dependent equilibria, 9 non-equilibria
        <abc: 1/4, acb: 1/4, bca: 1/4, cba: 1/4> (Condorcet winner: a, b, c)
        <BLANKLINE>
        1 equilibrium, 0 utility-dependent equilibrium, 1 non-equilibrium
        <abc: 1> (Condorcet winner: a)
        <BLANKLINE>
        1 equilibrium, 0 utility-dependent equilibrium, 3 non-equilibria
        <abc: 2/3, bac: 1/3> (Condorcet winner: a)
        <abc: 2/3, acb: 1/3> (Condorcet winner: a)
        <abc: 1/2, bac: 1/2> (Condorcet winner: a, b)
        <abc: 1/2, acb: 1/2> (Condorcet winner: a)
        <abc: 3/4, bac: 1/4> (Condorcet winner: a)
        <abc: 3/4, acb: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        1 equilibrium, 2 utility-dependent equilibria, 5 non-equilibria
        <abc: 1/2, bca: 1/4, cba: 1/4> (Condorcet winner: a, b)
        <BLANKLINE>
        2 equilibria, 0 utility-dependent equilibrium, 6 non-equilibria
        <abc: 1/2, bac: 1/4, cba: 1/4> (Condorcet winner: a, b)
        <BLANKLINE>
        2 equilibria, 1 utility-dependent equilibrium, 5 non-equilibria
        <abc: 1/3, bac: 1/3, cab: 1/3> (Condorcet winner: a)
        <abc: 1/2, bac: 1/4, cab: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        2 equilibria, 2 utility-dependent equilibria, 12 non-equilibria
        <abc: 1/4, acb: 1/4, bac: 1/4, cab: 1/4> (Condorcet winner: a)
        <BLANKLINE>
        >>> len(exploration.items())
        13
        >>> len(exploration.keys())
        13
        >>> len(exploration.values())
        13
    """
    pass
