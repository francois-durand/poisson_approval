================
Poisson Approval
================


.. image:: https://img.shields.io/pypi/v/poisson_approval.svg
        :target: https://pypi.python.org/pypi/poisson_approval
        :alt: PyPI Status

.. image:: https://github.com/francois-durand/poisson_approval/workflows/build/badge.svg?branch=master
        :target: https://github.com/francois-durand/poisson_approval/actions?query=workflow%3Abuild
        :alt: Build Status

.. image:: https://github.com/francois-durand/poisson_approval/workflows/docs/badge.svg?branch=master
        :target: https://github.com/francois-durand/poisson_approval/actions?query=workflow%3Adocs
        :alt: Documentation Status

.. image:: https://codecov.io/gh/francois-durand/poisson_approval/branch/master/graphs/badge.svg
        :target: https://codecov.io/gh/francois-durand/poisson_approval/tree/master
        :alt: Code Coverage


Poisson Approval studies the Poisson Game of Approval Voting.


* Free software: GNU General Public License v3.
* Documentation: https://francois-durand.github.io/poisson_approval/.

--------
Features
--------

* Implement only the case of 3 candidates.
* Deal with ordinal or cardinal profiles.
* Compute the asymptotic developments of the probability of pivot events when the number of players tends to infinity.
* Compute the best response to a given tau-vector.
* Explore automatically a grid of ordinal profiles or a grid of tau-vectors.
* Perform Monte-Carlo experiments on profiles or tau-vectors.
* Search an equilibrium by iterated voting or fictitious play.
* In addition to Approval, implement Plurality and Anti-plurality as Poisson games.
* Perform numeric or symbolic computation.

-------
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
