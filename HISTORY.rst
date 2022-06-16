=======
History
=======

--------------------------------------------
0.31.0 (2022-06-16): Stability of Equilibria
--------------------------------------------

* Add `ProfileHistogram.is_equilibrium_stable`: whether a forward-focused equilibrium strategy is stable in this
  profile (which is a sufficient condition for it to be an equilibrium in the sense of Myerson).

--------------------------------------------------------------------------
0.30.0 (2022-01-24): Equilibrium Properties in Monte Carlo Fictitious Play
--------------------------------------------------------------------------

* Add new Monte-Carlo settings:

  * ``MCS_FOCUS``: focus of the equilibrium.
  * ``MCS_IS_ORDINAL_EQ``: whether the equilibrium is ordinal.

* Add ``BestResponse.is_ordinal``: whether the best response is purely ordinal.
* Add ``TauVector.is_best_response_ordinal``: whether the best responses of all rankings are ordinal.
* Object of the class ``Focus`` are now hashable.
* For developers:

  * Add a local coverage report.
  * The run configuration to generate the documentation is stored as a project file.

-----------------------------------------------------------
0.29.3 (2022-01-18): Patch test for latest release of SymPy
-----------------------------------------------------------

* Correct a unit test due to a change of behavior in the latest release of SymPy.

---------------------------------------------------------------
0.29.2 (2021-02-16): Notebook on Robustness to the Initial Poll
---------------------------------------------------------------

* Update the notebook on the robustness to the initial poll in the documentation.

-----------------------------------------------------
0.29.1 (2021-02-16): Notebook on Confidence Intervals
-----------------------------------------------------

* Update the notebook on confidence intervals in the documentation.

------------------------------------------------
0.29.0 (2021-02-15): Monte-Carlo Fictitious Play
------------------------------------------------

Monte-Carlo fictitious play:

* Add ``monte_carlo_fictitious_play``: Monte-Carlo analysis of fictitious play (or iterated voting).
* Add ``MonteCarloSetting``: setting for ``monte_carlo_fictitious_play``.
* Add ``MCS_BALLOT_STATISTICS``, ``MCS_CANDIDATE_WINNING_FREQUENCY``, ``MCS_CONVERGES``, ``MCS_DECREASING_SCORES``,
  ``MCS_FREQUENCY_CW_WINS``, ``MCS_N_EPISODES``, ``MCS_PROFILE``, ``MCS_TAU_INIT``, ``MCS_UTILITY_THRESHOLDS``,
  ``MCS_WELFARE_LOSSES``: pre-defined settings for ``monte_carlo_fictitious_play``.
* Add ``plot_utility_thresholds``: plot the distribution (CDF) of the utility threshold.
* Add ``plot_welfare_losses``: plot the distribution (CDF) of the welfare losses, for each voting rule.
* Modify ``plot_distribution_scores``: the new syntax takes advantage of ``monte_carlo_fictitious_play``.

Improvement of ``iterated_voting`` and ``fictitious_play``:

* Both methods now takes additional parameters: ``other_statistics_update_ratio``, ``other_statistics_tau`` and
  ``other_statistics_strategy``, in order to compute long-run averages of any kind of statistics.
* New output ``converges``: whether the process converges.
* New output ``tau_init``: the actual value of the tau-vector used at initialization (especially useful when
  initialization is random).
* New results related to the "other statistics" are included in the output dictionary.

Other tools for meta-analysis:

* Add ``convergence_test``: create a convergence test.
* Add ``is_condorcet``: whether a profile has one Condorcet winner.
* Add ``is_not_condorcet``: whether a profile has no Condorcet winner.
* ``heatmap_candidates`` accepts a new parameter, ``file_save_data``, to save into a file the data computed in order
  to prepare the plot. Same for ``ternary_plot_winners_at_equilibrium``.

``UtilPlots`` module:

* Add ``plt_plot_with_error``: adaptation of ``plt.plot`` for Monte-Carlo experiments, with error area.
* Add ``plt_step_with_error``: adaptation of ``plt.step`` for Monte-Carlo experiments, with error area.
* Add ``plt_cdf``: plot a cumulative distribution function from Monte-Carlo experiments, with error area.

Misc:

* Rename the module ``constants`` to ``basic_constants``.
* Add constant ``VOTING_RULES``: the three voting rules of the package, i.e. Approval, Plurality and Anti-Plurality.
* Add constant ``SETS_OF_RANKINGS_UP_TO_RELABELLING``: all possible sets of rankings, up to relabelling the candidates.
* Rename ``BestResponse.threshold_utility`` to ``BestResponse.utility_threshold`` (for consistency with other
  occurrences of the phrase "utility threshold").
* Revision of the whole documentation, including the tutorials (typos, missing hyperlinks, etc).
* In the documentation, add the notebooks related to our research article:
  *Voter Coordination in Elections: A Case for Approval Voting*.

Fix bugs:

* In ``EventTrio``: solve a rare bug occurring when an offset ratio is greater but very close to 1.
* ``Profile.random_tau_undominated`` did not take voters with weak orders into account.
* In Plurality, voters with a weak order of type "hate" (e.g. `a~b>c`) were treated incorrectly for strategic voting.
  There was a similar bug in Anti-Plurality for voters with a weak order of type "love" (e.g. `a>b~c`). Fixing this bug
  has consequences, in particular, for the method ``tau_strategic`` of several subclasses of ``Profile``, but only
  for profiles involving weak orders, in Plurality or Anti-Plurality.

Fixing the latter bug lead to several collateral modifications concerning the strategies of the voters with a weak
order of preference:

* All subclasses of ``Strategy`` now take an additional parameter: ``d_weak_order_ballot``, that can be filled in
  the few cases where strategic voting is not automatic for voters with a weak order: "haters" (e.g. `a~b>c`) in
  Plurality and "lovers" (e.g. `a>b~c`) in Anti-Plurality. Note, in particular, that this parameter is not
  used for Approval.
* Add ``Profile.d_ballot_share_weak_voters_strategic``: ballot shares due to the weak orders if they vote
  strategically.
* ``Profile.best_responses_to_strategy`` now takes as input a tau-vector (instead of a dictionary of best responses)
  and an optional ratio of optimistic voters.

---------------------------------------------------------
0.28.0 (2020-12-11): Plurality and Anti-Plurality Welfare
---------------------------------------------------------

* In ``Profile``:

  * Add ``d_candidate_plurality_welfare``: plurality welfare of each candidate.
  * Add ``d_candidate_anti_plurality_welfare``: anti-plurality welfare of each candidate.
  * Add ``d_candidate_relative_plurality_welfare``: relative plurality welfare of each candidate.
  * Add ``d_candidate_relative_anti_plurality_welfare``: relative anti-plurality welfare of each candidate.

* In ``ProfileCardinal``:

  * ``d_candidate_welfare`` and ``d_candidate_relative_welfare`` now return a ``DictPrintingInOrder`` instead of
    a basic ``dict``.

---------------------------------------
0.27.1 (2020-11-26): Use GitHub actions
---------------------------------------

* This patch concerns only Poisson Approval's developpers. To develop and maintain the package, it uses GitHub actions
  instead of additional services such as Travis-CI and ReadTheDocs.

-----------------------------------
0.27.0 (2020-11-11): Analysis tools
-----------------------------------

* Add ``plot_distribution_scores``: CDF of the score of the winner, the challenger and the loser (conditionally
  on the convergence of fictitious play / iterated voting).
* Add ``TernaryAxesSubplotPoisson.f_point_values_``: when a candidate heatmap has been drawn, this function gives
  access to the computed values.
* Add ``TauVector.print_magnitudes_order``: print the order of the magnitudes of the weak pivots.
* In ``fictitious_play`` and ``iterated_voting``, in verbose mode, display also the order of the magnitudes of
  the weak pivots.

----------------------------------------------------------
0.26.0 (2020-06-26): Descriptive Statistics of the Ballots
----------------------------------------------------------

* In ``TauVector``:

  * Add ``share_single_votes``: share of single votes, i.e. votes for one candidate only.
  * Add ``share_double_votes``: share of double votes, i.e. votes for two candidates.

* In ``ProfileCardinal``:

  * Add ``share_sincere_among_strategic_voters``: share of strategic voters that happen to cast a sincere ballot (when
    a strategy is given).
  * Add ``share_sincere_among_fanatic_voters``: share of fanatic voters that happen to cast a sincere ballot.
  * Add ``share_sincere``: share of voters that happen to cast a sincere ballot (when a strategy is given). This
    takes sincere, fanatic and strategic voters into account.

* In ``Strategy``:

  * Add ``share_single_votes`` and ``share_double_votes``: these shortcuts are defined when the strategy
    is defined with an embedded profile.
  * Add ``share_sincere_among_strategic_voters`` and ``share_sincere``: these shortcuts are defined when the strategy
    is defined with an embedded profile, provided the profile is cardinal.

-------------------------------------------
0.25.1 (2020-06-25): Welfare of a Candidate
-------------------------------------------

* ``ProfileCardinal`` now has attributes ``d_candidate_welfare`` and ``d_candidate_relative_welfare``: for each
  candidate, it gives its welfare, i.e. its total utility. The relative welfare is normalized so that the candidate
  with maximal welfare has 1 and the one with minimal welfare has 0.
* The function ``probability`` now accepts a tuple of tests as inputs.
* Bug fix: the recent versions of the external package ``scipy`` changed the behavior of ``scipy.optimize.minimize``.
  Since ``PivotTrio`` relies on this function, its behavior changed in an unexpected way and it sometimes lead to
  incorrect results, such as a positive magnitude. This version solves the problem: ``PivotTrio`` has regained its
  former (correct) behavior.

----------------------------------------------------
0.24.0 (2020-03-29): Plots for Convergence Frequency
----------------------------------------------------

* Add ``ternary_plot_convergence`` and ``binary_plot_convergence``: plot the convergence frequency, which is defined
  as the proportion of initializations where iterated voting or fictitious play lead to convergence within
  ``n_max_episodes`` iterations.

----------------------------------------------------------------
0.23.0 (2020-03-29): Improve Iterated Voting and Fictitious Play
----------------------------------------------------------------

* Random initialization of iterated voting and fictitious play:

  * Add the option ``'random_tau'``: a random tau-vector that is consistent with the voting rule.
  * Add the option ``'random_tau_undominated'``: a random tau-vector where each voter randomly uses an undominated
    ballot. Relies on the new method ``Profile.random_tau_undominated``.
  * Remove the option ``'random_strategy'``: it had an unnatural behavior for Plurality and Anti-Plurality.
    Subsequently, remove also the method ``Profile.random_strategy``.

* In iterated voting and fictitious play, winning frequencies are computed from t=1 instead of t=0. The motivation is
  twofold. Firstly, if the result at initialization is essentially arbitrary and, for example, candidate `a` always
  wins afterwards, we consider it more natural to have a winning frequency of 1 for `a`. Secondly, when using the
  arithmetic average, the denominator is the number of steps, rather than the number of steps plus one. As a
  consequence, we updated the helper functions in order to account for this time translation:

  * Replace ``one_over_t_plus_one`` with ``one_over_t``.
  * Replace ``one_over_sqrt_t_plus_one`` with ``one_over_sqrt_t``.
  * Replace ``one_over_log_t_plus_two`` with ``one_over_log_t_plus_one``.
  * Replace ``one_over_log_log_t_plus_fifteen`` with ``one_over_log_log_t_plus_fourteen``.

* Fix a rare bug: in some tau-vectors, when computing the trio event, an offset was found greater than 1, whereas theory
  shows that it is lower than 1. This used to cause a collateral error when computing the best response with the
  offset method.

---------------------------------
0.22.0 (2020-03-22): Binary Plots
---------------------------------

* Implement *binary plots*, i.e. plots designed to study profiles based on two ranking with varying utilities. Cf. the
  corresponding tutorial.

  * Intensity heat maps.
  * Candidate heat maps.
  * Annotate the Condorcet regions.

* Utilities:

  * Add ``d_candidate_ordinal_utility``: ordinal utility of a candidate for a given preference order.
  * Add ``my_range``: similar to ``range``, but works also for fractions.
  * Add ``my_sign``: sign of a number. Return an integer in {-1, 0, 1}, unlike ``np.sign``.

---------------------------------------------------
0.21.0 (2020-03-12): Iterables and Random Factories
---------------------------------------------------

* Add new iterables and random factories for profiles, tau-vectors and strategies. These iterables and random factories
  are very flexible: you can specify that some types have a fixed share, that only some types have a variable share,
  etc. Cf. the corresponding tutorials and the corresponding section in Reference.
* Remove ``ExploreGridProfilesOrdinal`` and ``ExploreGridTaus``: their features are included in the new iterables.
* Remove all classes whose name began with ``Generator``: their features are included in the new random factories.
* All the methods that had a parameter ``generator`` now have a parameter ``factory`` instead. This choice is due to
  the fact that the word "generator" has another meaning in Python, which could be misleading.
* ``SimplexToProfile`` works similarly to the new iterables and random factories. In particular it is now allowed to
  use the same type several times, for example in the fixed shares and in the variable shares.
* There is a new syntax option to define a ``ProfileHistogram``, which is especially convenient for
  iterables and random factories.
* Utilities:

  * Add ``iterator_integers_fixed_sum``: iterate over vectors of integers with a fixed sum.
  * Add ``iterate_simplex_grid``: iterate over the points in the simplex, with rational coordinates of a given
    denominator.
  * Add ``allowed_ballots``: allowed ballots in a voting rule.

* Complete revision of the tutorials.

-----------------------------------------
0.20.0 (2020-03-03): Symbolic Computation
-----------------------------------------

* ``Profile`` and its subclasses, ``TauVector``, ``Asymptotic`` and its constructors (such as
  ``Asymptotic.poisson_value``, ``Asymptotic.poisson_eq``, etc.) accept an optional argument ``symbolic``. If False
  (default), then all computations are numeric as before. If True, then almost all computations are symbolic; the
  only exception is when the trio event can be evaluated only via the Dual Magnitude Theorem. Please note that:

  * This feature relies on the external package `sympy` and works with its current version (1.5.1) but we cannot
    guarantee that it will still work with future versions of `sympy`.
  * When activated, it slows downs the computation considerably. In particular, it is strongly advised not to use
    fictitious play or iterated voting in symbolic mode.

* Equality and closeness tests:

  * ``Asymptotic.isclose`` is renamed to ``look_equal``: in numeric mode, it is still a closeness test, but in
    symbolic mode, it is an equality test.
  * Remove ``StrategyThreshold.isclose``: this method was not used anymore.

* ``Event`` and its subclasses take a ``TauVector`` as input, instead of the dictionary of its coefficients. Firstly, it
  speeds up computation. Secondly, it avoids a minor bug in symbolic mode.

* Utilities:

  * Add the classes ``ComputationEngine``, ``ComputationEngineNumeric`` and ``ComputationEngineSymbolic``, defining
    how some mathematical operations are performed.
  * Add the function ``computation_engine``: choose the computation engine.
  * Remove the utility function ``barycenter`` and include it as a method in ``ComputationEngine``.

-------------------------------------
0.19.0 (2020-02-27): Mixed Strategies
-------------------------------------

* ``StrategyThreshold``: for each ranking, there is a ``threshold`` (like before) and an optional ``ratio_optimistic``.
  Voters whose utility for their second candidate is equal to the threshold of the strategy are split: a share
  ``ratio_optimistic`` behave as if the threshold was higher (in Approval, they vote only for their top candidate)
  and the rest behave as if the threshold was lower (in Approval, they vote for their two first candidates). Hence the
  strategy is mixed. Note that this only makes a difference when the profile has "atoms" (concentration of voters on a
  single utility point); currently, this is only the case in ``ProfileDiscrete``.
* For ``ProfileDiscrete``, fictitious play and iterated voting consider that the responses use a ratio of optimistic
  voters equal to 1/2.
* Add ``ProfileCardinalContinuous``: this abstract class is a child of ``ProfileCardinal`` and a parent class
  of ``ProfileNoisyDiscrete`` and ``ProfileHistogram``. In these profiles, the ratios of optimistic voters are not
  important because there is no "atom".
* ``GeneratorStrategyThresholdUniform``: for each ranking, the ratio of optimistic voters is also chosen uniformly.
* The utility ``DictPrintingInOrderIgnoringNone`` now also ignores values that are iterables containing only None.

-------------------------------------------
0.18.0 (2020-02-26): Improved Ternary Plots
-------------------------------------------

* Nicer colors than before. For example, an equal mix of candidate `a` (red) and `b` (green) was brownish, whereas it
  is now yellow. Similarly, a mix of the three candidates (red, green, blue) was gray, and it is now white. Etc.
* Improved ternary plot shortcuts ``ternary_plot_n_equilibria``, ``ternary_plot_winners_at_equilibrium`` and
  ``ternary_plot_winning_frequencies``:

  * New versions of these functions with more options. Cf. the tutorial on ternary plots.
  * Add class ``SimplexToProfile`` to map a point of the simplex to a profile. This includes the possibility of
    having fixed additional voters.

* ``TernaryAxesSubplotPoisson``:

  * Add methods ``legend_color_patches`` and ``legend_palette``: two different styles of legends for candidate
    heat maps.
  * The method ``heatmap_candidates`` has a new parameter ``legend_style``.
  * The method ``annotate_condorcet`` has a new parameter ``d_order_fixed_share`` to account for fixed additional
    voters.
  * In several methods, the old parameters ``color_a``, ``color_b`` and ``color_c`` are suppressed, because
    the colors for `a`, `b`, `c` are not modifiable anymore.

* Random strategies:

  * Add ``GeneratorStrategyTwelveUniform``.
  * Add method ``Profile.random_strategy``: return a random strategy that is suitable for the profile (e.g. an ordinal
    strategy for an ordinal profile, etc.).
  * ``ProfileCardinal.iterated_voting`` and ``ProfileCardinal.fictitious_play`` now accept the parameter
    ``init='random'`` for an initialization with a random strategy.

* Add ``Profile.order_and_label``: order and label of a discrete type. This auxiliary function is used for the ternary
  plots.

----------------------------------------
0.17.0 (2020-02-24): Analyzed Strategies
----------------------------------------

* ``Profile`` and its subclasses:

  * The method ``analyzed_strategies`` now inputs an iterator of strategies: it perform an analysis on all the
    strategies given by this iterator.
  * Add pre-defined iterators of strategies:

    * ``strategies_ordinal`` is defined for any profile.
    * ``strategies_pure`` is defined for any discrete profile, such as ``ProfileDiscrete`` or ``ProfileTwelve``.
    * ``strategies_group`` is defined for any profile where a reasonable notion of "group" is defined, such as
      ``ProfileNoisyDiscrete`` or ``ProfileHistogram``.

  * Add the attributes ``analyzed_strategies_ordinal``, ``analyzed_strategies_pure``, ``analyzed_strategies_group``.
    Not only do they provide shortcuts combining ``analyzed_strategies`` with the relevant iterator, but they also have
    the added value of being cached properties: if the user accesses the same attribute several times, it is only
    computed once.

  * Remove the attribute ``winners_at_equilibrium``. Instead, the corresponding attribute is added to the class
    ``AnalyzedStrategies``. This gives more flexibility because it is defined for any ``AnalyzedStrategies`` object.

* The consequences on ternary plots are temporary and are likely to change in the near future, with a new release
  focusing on improved ternary plots.

  * ``ternary_plot_winners_at_equilibrium`` becomes ``ternary_plot_winners_at_equilibrium_ordinal``.
  * ``ternary_plot_n_bloc_equilibria`` becomes ``ternary_plot_n_equilibria_ordinal``.

* ``Strategy.deepcopy_with_attached_profile`` now also copies the voting rule of the given profile.

-------------------------------------------------------------------------
0.16.1 (2020-02-24): More Flexible Initialization of ProfileNoisyDiscrete
-------------------------------------------------------------------------

* ``ProfileNoisyDiscrete``: add a parameter ``noise`` that enables not to mention explicitly the value of the noise for
  each group of voters. This is especially convenient in the quite common case where all groups of voters have the
  same noise.

-----------------------------------------
0.16.0 (2020-02-22): ProfileNoisyDiscrete
-----------------------------------------

* Add ``ProfileNoisyDiscrete``: a profile with a discrete distribution of voters, with noise.

--------------------------------
0.15.0 (2020-02-20): Weak Orders
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
