import numpy as np
from collections import Counter
try:
    from shapely.geometry import Polygon
except OSError:  # pragma: no cover
    pass
from poisson_approval.constants.constants import CANDIDATES
from poisson_approval.utils.Util import is_weak_order, is_lover


def _m_permutation(role_x, role_y, role_z):
    """Permutation matrix

    Parameters
    ----------
    role_x, role_y, role_z : int
        `role_x` is the new index that `plays the role` that x does in the pattern. For example, if the coefficient
        of index `x` is positive in the pattern, the coefficient of index role_x is positive in the instance.

    Returns
    -------
    ndarray
        The permutation matrix (cf. example).

    Examples
    --------
        >>> pattern = [42, 51, 69]
        >>> m = _m_permutation(role_x=1, role_y=2, role_z=0)  # E.g. role_x=1 ==> coordinate 1 must receive 42
        >>> m @ pattern
        array([69, 42, 51])
    """
    result = np.zeros((3, 3), dtype=int)
    result[role_x, 0] = 1
    result[role_y, 1] = 1
    result[role_z, 2] = 1
    return result


def _polygon_victory(x, y, z):  # pragma: no cover
    """Polygon of victory.

    Polygon of victory of one candidate, say `a`, against another candidate, say `b`.

    Parameters
    ----------
    x, y, z : Number in {-1, 0, 1}
        For example, `x` is 1 if the first order likes `a` better than `b`, 0 if she is indifferent between them,
        and -1 if she likes `b` better than `a`. The roles of `y` and `z` are similar for the second and the third
        orders.

    Returns
    -------
    Polygon
        The polygon of victory of `a` against `b`, in the simplex defined by the first, second and third orders
        (each point of the simplex represents the shares of each order).

    Examples
    --------
        # >>> print(_polygon_victory(1, 1, 1))
        # POLYGON Z ((1 0 0, 0 1 0, 0 0 1, 1 0 0))
        # >>> print(_polygon_victory(-1, -1, -1))
        # GEOMETRYCOLLECTION EMPTY
        # >>> print(_polygon_victory(1, 1, -1))
        # POLYGON Z ((1 0 0, 0.5 0 0.5, 0 0.5 0.5, 0 1 0, 1 0 0))
        # >>> print(_polygon_victory(1, -1, -1))
        # POLYGON Z ((1 0 0, 0.5 0.5 0, 0.5 0 0.5, 1 0 0))
        # >>> print(_polygon_victory(1, 0, -1))
        # POLYGON Z ((1 0 0, 0 1 0, 0.5 0 0.5, 1 0 0))
    """
    # x, y, z \in {-1, 0, 1}
    xyz = [x, y, z]
    if x >= 0 and y >= 0 and z >= 0:
        return Polygon([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
    if x <= 0 and y <= 0 and z <= 0:
        return Polygon()
    counter = Counter(xyz)
    if counter[1] == 2:
        # + + -
        role_x = xyz.index(1)
        role_y = role_x + 1 + xyz[role_x + 1:].index(1)
        role_z = xyz.index(-1)
        m = _m_permutation(role_x, role_y, role_z)
        return Polygon([m @ (1, 0, 0), m @ (.5, 0, .5), m @ (0, .5, .5), m @ (0, 1, 0)])
    elif counter[-1] == 2:
        # + - -
        role_x = xyz.index(1)
        role_y = xyz.index(-1)
        role_z = role_y + 1 + xyz[role_y + 1:].index(-1)
        m = _m_permutation(role_x, role_y, role_z)
        return Polygon([m @ (1, 0, 0), m @ (.5, .5, 0), m @ (.5, 0, .5)])
    else:  # counter[0] == 1
        # + 0 -
        m = _m_permutation(role_x=xyz.index(1), role_y=xyz.index(0), role_z=xyz.index(-1))
        return Polygon([m @ (1, 0, 0), m @ (0, 1, 0), m @ (.5, 0, .5)])


def _d_candidate_ordinal_utility(order):
    """Ordinal utilities of the candidates.

    Parameters
    ----------
    order : str
        For example 'abc' (ranking) or 'a~b>c' (weak order).

    Returns
    -------
    dict
        Key: candidate. Value: an ordinal utility.

    Examples
    --------
        >>> _d_candidate_ordinal_utility('abc')
        {'a': 1, 'b': 0.5, 'c': 0}
        >>> _d_candidate_ordinal_utility('a>b~c')
        {'a': 1, 'b': 0, 'c': 0}
        >>> _d_candidate_ordinal_utility('a~b>c')
        {'a': 1, 'b': 1, 'c': 0}
    """
    if is_weak_order(order):
        if is_lover(order):
            return {order[0]: 1, order[2]: 0, order[4]: 0}
        else:
            return {order[0]: 1, order[2]: 1, order[4]: 0}
    else:
        return {order[0]: 1, order[1]: .5, order[2]: 0}


def _polygon_condorcet(candidate, order_x, order_y, order_z):  # pragma: no cover
    """Polygon representing the zone where a candidate is a Condorcet winner.

    Parameters
    ----------
    candidate : str
        'a', 'b' or 'c'.
    order_x, order_y, order_z : str
        Rankings ('abc') or weak orders ('a~b>c' or 'a>b~c').

    Returns
    -------
    Polygon
        Zone where `candidate` is the CW, in the simplex defined by the three orders.

    Examples
    --------
        # >>> print(_polygon_condorcet('a', 'abc', 'bca', 'cab'))
        # POLYGON Z ((0.5 0.5 0, 1 0 0, 0.5 0 0.5, 0.5 0.5 0))
    """
    other_candidates = sorted({'a', 'b', 'c'} - {candidate})
    other1, other2 = tuple(other_candidates)
    d_candidate_pseudo_utility_x = _d_candidate_ordinal_utility(order_x)
    d_candidate_pseudo_utility_y = _d_candidate_ordinal_utility(order_y)
    d_candidate_pseudo_utility_z = _d_candidate_ordinal_utility(order_z)
    polygon1 = _polygon_victory(
        np.sign(d_candidate_pseudo_utility_x[candidate] - d_candidate_pseudo_utility_x[other1]),
        np.sign(d_candidate_pseudo_utility_y[candidate] - d_candidate_pseudo_utility_y[other1]),
        np.sign(d_candidate_pseudo_utility_z[candidate] - d_candidate_pseudo_utility_z[other1]),
    )
    polygon2 = _polygon_victory(
        np.sign(d_candidate_pseudo_utility_x[candidate] - d_candidate_pseudo_utility_x[other2]),
        np.sign(d_candidate_pseudo_utility_y[candidate] - d_candidate_pseudo_utility_y[other2]),
        np.sign(d_candidate_pseudo_utility_z[candidate] - d_candidate_pseudo_utility_z[other2]),
    )
    return polygon1.intersection(polygon2)


def _draw_polygon(tax, polygon, name):  # pragma: no cover
    """Draw a polygon in a ternary plot.

    Parameters
    ----------
    tax : TernaryAxesSubplotPoisson
    polygon : Polygon
    name : str
        The name to display in the centroid of the polygon.
    """
    if polygon.area == 0:
        return
    for p1, p2 in zip(polygon.exterior.coords[:-1], polygon.exterior.coords[1:]):
        tax.line_simplex(p1, p2)
    tax.annotate_simplex(name, polygon.centroid.coords[0])


def draw_condorcet_zones(tax, right_ranking, top_ranking, left_ranking):  # pragma: no cover
    """Draw and annotate the Condorcet zones.

    Cf. :meth:`TernaryAxesSubplotPoisson.annotate_condorcet`.
    """
    polygon_not_condorcet = Polygon([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
    for candidate in CANDIDATES:
        polygon = _polygon_condorcet(candidate, right_ranking, top_ranking, left_ranking)
        _draw_polygon(tax, polygon, '%s is CW' % candidate)
        polygon_not_condorcet = polygon_not_condorcet.difference(polygon)
    _draw_polygon(tax, polygon_not_condorcet, 'no CW')
