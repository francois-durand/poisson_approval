=======
History
=======

--------------------------------
0.15.0 (2020-02-10): Weak Orders
--------------------------------

* Implement weak orders:

  * ``Profile`` now has attributes ``d_weak_order_share``, ``support_in_weak_orders``, ``contains_weak_orders``,
    ``contains_rankings``, ``d_ballot_weak_voters_sincere``, ``d_ballot_weak_voters_fanatic``.
  * Subclasses of Profile have a parameter ``d_weak_order_share``.
  * Remove methods ``ProfileOrdinal.support`` and ``ProfileOrdinal.is_generic``: with the presence of weak orders,
    their names had become misleading, whereas ``support_in_rankings`` and ``is_generic_in_ranking`` is non-ambiguous.
  * ``TernaryAxesSubplotPoisson.annotate_condorcet`` now also works with weak orders. However, it may not work on
    all distributions because it relies on the external package `shapely`. If there are only rankings, it should still
    work anyway.
  * Add utilities ``is_weak_order``, ``is_lover``, ``is_hater``, ``sort_weak_order``.

* Add shortcut functions for some common ternary plots:

  * ``ternary_plot_n_bloc_equilibria``: number of bloc equilibria.
  * ``ternary_plot_winners_at_equilibrium``: winners at equilibrium.
  * ``ternary_plot_winning_frequencies``: winning frequencies in fictitious play.

* Methods ``ProfileCardinal.iterated_voting`` and ``ProfileCardinal.fictitious_play`` have a new parameter
  ``winning_frequency_update_ratio``, indicating how the winning frequencies are computed in case of non-convergence.
  Note however that in case of convergence to a periodical orbit (for iterated voting), it remains the arithmetic
  average anyway.

* Add utility ``my_division``: division of two numbers, trying to be exact if it is reasonable.

---------------------------------------------------------------------------------
0.14.0 (2020-02-16): Flexible Initialization of Iterated Voting / Fictitious Play
---------------------------------------------------------------------------------

* Instead of a parameter ``strategy_ini``, the methods ``ProfileCardinal.iterated_voting`` and
  ``ProfileCardinal.fictitious_play`` now have a parameter ``init`` that can be either a strategy (like before), or a
  tau-vector, or a string ``'sincere'`` or ``'fanatic'``.

----------------------------------
0.13.0 (2020-02-16): Ternary Plots
----------------------------------

* Draw plots on the simplex where points have 3 coordinates summing to 1. Cf. the corresponding tutorial.

  * Intensity heat maps.
  * Candidate heat maps.
  * Annotate the Condorcet regions.

* Add ``Profile.winners_at_equilibrium``: for the classes of profile that have a method ``analyzed_strategies``,
  give the set of winners at equilibrium.

-----------------------------------------------------------------
0.12.0 (2020-02-09): GeneratorProfileHistogramSinglePeakedUniform
-----------------------------------------------------------------

* Add ``GeneratorProfileHistogramSinglePeakedUniform``: a generator of single-peaked histogram-profiles following
  the uniform distribution.
* Add examples of functions to be used as update ratios for ``ProfileCardinal.fictitious_play``:
  ``one_over_t_plus_one``, ``one_over_sqrt_t_plus_one``, ``one_over_log_t_plus_two``,
  ``one_over_log_log_t_plus_fifteen``.

-----------------------------------------------------------------------------
0.11.0 (2020-02-09): Winning frequencies in iterated voting / fictitious play
-----------------------------------------------------------------------------

* ``ProfileCardinal.iterated_voting`` and ``ProfileCardinal.fictitious_play`` now also output the winning frequency of
  each candidate (limit frequency in case of convergence, frequency over the history otherwise).
* New utilities:

  * Add ``candidates_to_d_candidate_probability``: convert a set of candidates to a dictionary of probabilities (random
    tie-break)
  * Add ``candidates_to_probabilities``: convert a set of candidates to an array of probabilities (random tie-break).
  * Add ``array_to_d_candidate_value``: convert an array to a dictionary of candidates and values.
  * Add ``d_candidate_value_to_array``: convert a dictionary of candidates and values to an array.

--------------------------------------------------------
0.10.0 (2020-02-09): ProfileDiscrete.analyzed_strategies
--------------------------------------------------------

* Implement ``ProfileDiscrete.analyzed_strategies``: exhaustive analysis of all pure strategies of the profile.

------------------------------------------------
0.9.0 (2020-02-09): Plurality and Anti-plurality
------------------------------------------------

* Implement Plurality and Anti-plurality (cf. the corresponding tutorial).
* Python 3.5 is not officially supported anymore. However, in practice, the package should still essentially work with
  Python 3.5, the only notable difference being the order in which the dictionaries are printed.
* New utilities:

  * Add ``ballot_two``: ballot for the second candidate of a ranking (used for Plurality).
  * Add ``ballot_one_three``: ballot against the second candidate of a ranking (used for Anti-plurality).
  * Add ``ballot_low_u`` and ``ballot_high_u``: the ballot chosen by the voters who have a low (resp. high) utility
    for their middle candidate, depending on the voting rule.
  * Add ``product_dict``: Cartesian product for a dictionary of iterables.
  * Add ``DictPrintingInOrderIgnoringNone``: dictionary that prints in the order of the keys, ignoring value None.
  * In the ``UtilCache`` module, add ``property_deleting_cache``: define a property that deletes the cache when set or
    deleted. This is used for parameters like ``ratio_sincere``, ``voting_rule``, etc.

-----------------------------------------------------------------
0.8.1 (2020-02-04): Better Handling of Edge Cases in BestResponse
-----------------------------------------------------------------

* ``BestResponse``: the focus of this release is to correct rare bugs that used to happen when some offsets are very
  close to 1.

  * API change: ``BestResponse`` now takes as parameters the tau-vector and the ranking, instead of all the events
    that are used for the computation.
  * Exchanged the justifications ``'Easy vs difficult pivot'`` and ``'Difficult vs easy pivot'`` (their usages
    were switched, even if the result itself was correct).
  * Use the asymptotic method only when there are two consecutive zeros in the "compass diagram" of the tau-vector
    (instead of: whenever it gives a result). The motivation is that the asymptotic method may rely on events that rely
    more on numerical approximation than the limit pivot theorem approach.
  * To determine whether pivots are easy or difficult, we rely on expected scores in the duo events, instead of the
    pseudo-offsets of the trio. The motivation is that in some cases, the trio is computed with a numerical optimizer
    that relies more on numerical approximation than the duo events, which use only basic operations like addition,
    multiplication, etc. In the rare cases where the two methods differ, the latter is thus more reliable.
  * Add a sub-algorithm of the "Offset method", called "Offset method with trio
    approximation correction". This is used in some rare cases where both pivots are difficult, but the numeric
    approximations of the trio event lead to an offset that is equal or even slightly greater than 1 (which is abnormal
    and leads to infinite geometric sums). In those cases, we now consider that the offset is lower and infinitely close
    to 1.
  * Corrected a bug in the asymptotic method that could happen when the two personalized pivots had very close
    magnitudes. This uses the correction of ``Asymptotic.limit`` mentioned below.

* ``TauVector``: added the attribute ``has_two_consecutive_zeros``.

* ``Event``: now computes the pseudo-offsets, e.g. ``psi_a``, ``psi_ab``, etc.

* ``Asymptotic``: handles some edge cases more nicely.

  * ``__str__`` displays a coefficient as 0, 1 or -1 only if it is equal to that value. Close is not enough.
  * ``limit`` does not use closeness to 0. It is not its role to decide what coefficients are negligible in the context.
    Only operations like multiplication are allowed to use closeness: for example, if ``mu_1`` and ``- mu_2`` are
    relatively close, the multiplication operator is allowed to decide that ``mu_1 + mu_2`` is equal to 0.
  * In multiplication, when the two magnitudes are close, the resulting magnitude is now always equal to the maximum.
    The same applies for the resulting `nu` when the `nu`'s are also equal.

* ``cached_property``: corrected a bug. In the case of nested cached properties, the inner one was sometimes not
  recorded in cache. It did not lead to incorrect results but slowed down the program.

----------------------------------
0.8.0 (2020-01-30): Fanatic voters
----------------------------------

* Implement the notion of fanatic voting, a variant of sincere voting: a given ratio of voters vote for their top
  candidate only. This is implemented for all subclasses of ``Profile``.
* The utility ``barycenter`` now accepts iterables.
* Corrected bug: ``Profile.standardized_version`` now takes into account the auxiliary parameters like
  ``ratio_sincere``, ``well_informed_voters``, etc.

-----------------------------------
0.7.0 (2020-01-30): ProfileDiscrete
-----------------------------------

* Add ``ProfileDiscrete``: a profile with a discrete distribution of voters.
* Subclasses of ``Profile``: better handling of the additional parameters like ``well_informed_voters`` or
  ``ratio_sincere``. In the conversions to string (``str`` or ``repr``), they are now mentioned. They are also used in
  the equality tests between two profiles.

-----------------------------------
0.6.0 (2020-01-29): Fictitious Play
-----------------------------------

* Implement ``ProfileCardinal.fictitious_play``, where the update ratios of the perceived tau-vector and the actual
  tau-vector can be functions of the time. It is also faster that ``ProfileCardinal.iterated_voting``, but can
  not detect cycles (only convergence).
* ``ProfileCardinal.iterated_voting_taus`` is renamed to ``ProfileCardinal.iterated_voting``. It has been generalized
  by implementing a notion of perceived tau-vector, like for ``ProfileCardinal.fictitious_play``. The syntax has been
  modified in consequence.
* ``ProfileCardinal.iterated_voting_strategies`` is deprecated and suppressed.
* Iterated voting and fictitious play do not need a ``StrategyThreshold`` as initial strategy, but any strategy that is
  consistent with the profile subclass. For example, with ``ProfileTwelve``, you can use a ``StrategyTwelve``.
* ``Strategy.profile`` is now a property that can be reassigned after the creation of the object.
* Add ``Strategy.deepcopy_with_attached_profile``: make a deep copy and attach a given profile.
* Add the utility ``to_callable``: convert an object to a callable (making it a constant function if it is not
  callable already).

----------------------------------------------------------
0.5.1 (2020-01-18): Configure Codecov and Improve Coverage
----------------------------------------------------------

* Configure Codecov.
* Reach 100% coverage for this version.

----------------------------------------------------------------------------
0.5.0 (2020-01-11): Sincere Voting and Progressive Update in Iterated Voting
----------------------------------------------------------------------------

* In iterated voting, implement the possibility to move only *progressively* towards the best response:

  * Add ``ProfileCardinal.iterated_voting_taus``: at each iteration, a given ratio of voters update their ballot.
  * Replace the former method ``ProfileCardinal.iterated_voting`` by ``ProfileCardinal.iterated_voting_strategies``:
    as in former versions, at each iteration, the threshold utility of each ranking's strategy is moved in the
    direction of the best response's threshold utility. The method now returns a cycle of tau-vectors and the
    corresponding cycle of best response strategies, in order to be consistent with
    ``ProfileCardinal.iterated_voting_taus``.
  * Add the utility ``barycenter``: compute a barycenter while respecting the type of one input if the other input has
    weight 0.
  * Accelerate the algorithm used in iterated voting.

* In ``ProfileCardinal``, add the possibility of partial sincere voting:

  * Add parameter ``ratio_sincere``: ratio of sincere voters.
  * Add property ``tau_sincere``: the tau-vector if all voters vote sincerely.
  * The former method ``tau`` is renamed ``tau_strategic``: the tau_vector if all voters vote strategically.
  * The new method ``tau`` takes both sincere and strategic voting into account.
  * The method ``is_equilibrium`` has a new implementation to take this feature into account.

* Add ``TauVector.isclose``: whether the tau-vector is close to another tau-vector (in the sense of
  ``math.isclose``). This method is used by the new version of ``ProfileCardinal.is_equilibrium``.

* Add ``Profile.best_responses_to_strategy``: convert a dictionary of best responses to a ``StrategyThreshold`` that
  mentions only the rankings that are present in the profile.

* In random generators of profiles (``GeneratorProfileOrdinalUniform``, ``GeneratorProfileOrdinalGridUniform``,
  ``GeneratorProfileOrdinalVariations``, ``GeneratorProfileHistogramUniform``): instead of having explicit arguments
  like ``well_informed_voters`` or ``ratio_sincere``, there are ``**kwargs`` that are directly passed to the
  ``__init__`` of the relevant Profile subclass.

* Update the tutorials with these new features.

----------------------------------------------
0.4.0 (2020-01-08): Add ``image_distribution``
----------------------------------------------

* Add ``image_distribution``: estimate the distribution of ``f(something)`` for a random ``something``.
* Update the tutorial on mass simulations with this new feature.

-----------------------------------------
0.3.0 (2020-01-08): New Random Generators
-----------------------------------------

* Add new random generators:

  * ``GeneratorExamples``: run another generator until the generated object meets a given test.
  * ``GeneratorStrategyOrdinalUniform``: draw a StrategyOrdinal uniformly.
  * ``GeneratorProfileOrdinalGridUniform``: draw a ProfileOrdinal uniformly on a grid of rational numbers.
  * ``GeneratorTauVectorGridUniform``: draw a TauVector uniformly on a grid of rational numbers.

* Utilities:

  * Add ``rand_integers_fixed_sum``: draw an array of integers with a given sum.
  * Add ``rand_simplex_grid``: draw a random point in the simplex, with rational coordinates of a given denominator.
  * Update ``probability``: allow for a tuple of generators.

* Tutorials:

  * Add a tutorial on asymptotic developments.
  * Update the tutorial on mass simulations with the new features.

------------------------------------------
0.2.1 (2020-01-05): Fix Deployment on PyPI
------------------------------------------

* Relaunch deployment.

--------------------------------------------------------------
0.2.0 (2020-01-05): Add Tutorials + Various Minor Improvements
--------------------------------------------------------------

* Add ``GeneratorProfileStrategyThreshold``.
* Add ``ProfileHistogram.plot_cdf``.
* Modify ``masks_distribution``: remove the trailing zeros. This has the same impact on
  ``ProfileOrdinal.distribution_equilibria``.
* Modify ``NiceStatsProfileOrdinal.plot_cutoff``: center the textual indications.
* Replace all notations ``r`` with ``profile`` and ``sigma`` with ``strategy``.
* Add tutorials.

-----------------------------------------------------------------
0.1.1 (2019-12-24): Convert all the Documentation to NumPy Format
-----------------------------------------------------------------

* Convert all the documentation to NumPy format, making it more readable in plain text.

-----------------------------------------
0.1.0 (2019-12-20): First release on PyPI
-----------------------------------------

* First release on PyPI.
* Implement only the case of 3 candidates.
* Deal with ordinal or cardinal profiles.
* Compute the asymptotic developments of the probability of pivot events when the number of players tends to infinity.
* Compute the best response to a given tau-vector.
* Explore automatically a grid of ordinal profiles or a grid of tau-vectors.
* Perform Monte-Carlo experiments on profiles or tau-vectors.
