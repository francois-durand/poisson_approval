=======
History
=======

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
