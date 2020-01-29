=======
History
=======

------------------
0.6.0 (2020-01-29)
------------------

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

------------------
0.5.1 (2020-01-18)
------------------

* Configure Codecov.
* Reach 100% coverage for this version.

------------------
0.5.0 (2020-01-11)
------------------

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

------------------
0.4.0 (2020-01-08)
------------------

* Add ``image_distribution``: estimate the distribution of ``f(something)`` for a random ``something``.
* Update the tutorial on mass simulations with this new feature.

------------------
0.3.0 (2020-01-08)
------------------

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

------------------
0.2.1 (2020-01-05)
------------------

* Relaunch deployment.

------------------
0.2.0 (2020-01-05)
------------------

* Add ``GeneratorProfileStrategyThreshold``.
* Add ``ProfileHistogram.plot_cdf``.
* Modify ``masks_distribution``: remove the trailing zeros. This has the same impact on
  ``ProfileOrdinal.distribution_equilibria``.
* Modify ``NiceStatsProfileOrdinal.plot_cutoff``: center the textual indications.
* Replace all notations ``r`` with ``profile`` and ``sigma`` with ``strategy``.
* Add tutorials.

------------------
0.1.1 (2019-12-24)
------------------

* Convert all the documentation to NumPy format, making it more readable in plain text.

------------------
0.1.0 (2019-12-20)
------------------

* First release on PyPI.
* Implement only the case of 3 candidates.
* Deal with ordinal or cardinal profiles.
* Compute the asymptotic developments of the probability of pivot events when the number of players tends to infinity.
* Compute the best response to a given tau-vector.
* Explore automatically a grid of ordinal profiles or a grid of tau-vectors.
* Perform Monte-Carlo experiments on profiles or tau-vectors.
