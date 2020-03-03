from poisson_approval import ProfileOrdinal, StrategyOrdinal


# N.B.: I commented the tests that are the same as for symbolic=False, with exactly the same results.

# def test_main():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          symbolic=True)
#         >>> profile
#         ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)})
#         >>> print(profile)
#         <abc: 1/10, bac: 3/5, cab: 3/10> (Condorcet winner: b)
#         >>> profile.abc
#         Fraction(1, 10)
#         >>> profile.d_ranking_share['abc']  # Alternate syntax for profile.abc
#         Fraction(1, 10)
#         >>> profile.weighted_maj_graph
#         array([[0, Fraction(-1, 5), Fraction(2, 5)],
#                [Fraction(1, 5), 0, Fraction(2, 5)],
#                [Fraction(-2, 5), Fraction(-2, 5), 0]], dtype=object)
#         >>> profile.condorcet_winners
#         Winners({'b'})
#         >>> profile.is_profile_condorcet
#         1.0
#         >>> profile.has_majority_favorite  # Is one candidate 'top' in a majority of ballots?
#         True
#         >>> profile.has_majority_ranking  # Does one ranking represent a majority of ballots?
#         True
#         >>> profile.is_single_peaked  # Is the profile single-peaked?
#         True
#         >>> profile.support_in_rankings
#         {'abc', 'bac', 'cab'}
#         >>> profile.is_generic_in_rankings  # Are all rankings there?
#         False
#         >>> profile.analyzed_strategies_ordinal
#         Equilibria:
#         <abc: a, bac: b, cab: ac> ==> b (FF)
#         <abc: a, bac: ab, cab: c> ==> a (D)
#         <BLANKLINE>
#         Utility-dependent equilibrium:
#         <abc: ab, bac: b, cab: c> ==> b (FF)
#         <BLANKLINE>
#         Non-equilibria:
#         <abc: a, bac: b, cab: c> ==> b (FF)
#         <abc: a, bac: ab, cab: ac> ==> a (D)
#         <abc: ab, bac: b, cab: ac> ==> b (FF)
#         <abc: ab, bac: ab, cab: c> ==> a, b (FF)
#         <abc: ab, bac: ab, cab: ac> ==> a (D)
#         >>> print(profile.analyzed_strategies_ordinal.equilibria[0])
#         <abc: a, bac: b, cab: ac> ==> b
#         >>> print(profile.analyzed_strategies_ordinal.winners_at_equilibrium)
#         a, b
#     """
#     pass
#
#
# def test_main_weak_orders():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10)},
#         ...                          d_weak_order_share={'c>a~b': Fraction(3, 10)}, symbolic=True)
#         >>> profile
#         ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(3, 5)}, d_weak_order_share={'c>a~b': Fraction(3, 10)})
#         >>> print(profile)
#         <abc: 1/10, bac: 3/5, c>a~b: 3/10> (Condorcet winner: b)
#     """
#     pass
#
#
# def test_repr():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          well_informed_voters=False, ratio_fanatic=Fraction(1, 10), symbolic=True)
#         >>> profile
#         ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)}, \
# well_informed_voters=False, ratio_fanatic=Fraction(1, 10))
#     """
#     pass
#
#
# def test_str():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          well_informed_voters=False, ratio_fanatic=Fraction(1, 10), symbolic=True)
#         >>> print(profile)
#         <abc: 1/10, bac: 3/5, cab: 3/10> (Condorcet winner: b) (badly informed voters) (ratio_fanatic: 1/10)
#     """
#     pass
#
#
# def test_eq():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          symbolic=True)
#         >>> profile == ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                           symbolic=True)
#         True
#     """
#     pass
#
#
# def test_standardized_version():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          symbolic=True)
#         >>> profile.standardized_version
#         ProfileOrdinal({'abc': Fraction(3, 5), 'bac': Fraction(1, 10), 'cba': Fraction(3, 10)})
#         >>> profile.is_standardized
#         False
#     """
#     pass


def test_tau():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...                          symbolic=True)
        >>> strategy = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
        >>> tau = profile.tau(strategy)
        >>> print(tau)
        <a: 1/10, ab: 3/5, c: 3/10> ==> a
        >>> τ = profile.τ(strategy)  # Alternate syntax
        >>> print(τ)
        <a: 1/10, ab: 3/5, c: 3/10> ==> a
        >>> tau.trio
        <asymptotic = exp(n*(-1 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), \
phi_a = 0, phi_c = sqrt(2), phi_ab = sqrt(2)/2>
    """
    pass


# def test_tau_strategic():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          symbolic=True)
#         >>> strategy = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
#         >>> tau_strategic = profile.tau_strategic(strategy)
#         >>> print(tau_strategic)
#         <a: 1/10, ab: 3/5, c: 3/10> ==> a
#     """
#     pass
#
#
# def test_tau_strategic_badly_informed():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          well_informed_voters=False, symbolic=True)
#         >>> strategy = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
#         >>> tau_strategic = profile.tau_strategic(strategy)
#         >>> print(tau_strategic)
#         <a: 7/16, b: 3/8, c: 3/16> ==> a
#     """
#     pass
#
#
# def test_is_equilibrium():
#     """
#         >>> from fractions import Fraction
#         >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
#         ...                          symbolic=True)
#         >>> strategy = StrategyOrdinal({'abc': 'a', 'bac': 'ab', 'cab': 'c'})
#         >>> profile.is_equilibrium(strategy)
#         EquilibriumStatus.EQUILIBRIUM
#     """
#     pass


def test_proba_equilibrium_and_co():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileOrdinal({'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...                          symbolic=True)
        >>> profile.proba_equilibrium()
        1
        >>> profile.distribution_equilibria()
        array([0, 0, 120/121 - 9*sqrt(3)/121, 1/121 + 9*sqrt(3)/121], dtype=object)
        >>> profile.distribution_winners()
        array([0, 0, 1, 0], dtype=object)
    """
    pass
