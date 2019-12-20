import random
import numpy as np
from math import isclose
from itertools import product


def masks_area_naive(inf, sup, masks):
    """
    Area of some masks. Naive implementation (used as a sanity test for the recursive implementation)

        >>> area = masks_area_naive(inf=[0, 0], sup=[1, 2],
        ...                         masks=[[(.2, True), (.6, False)], [(.3, False), (.4, True)]])
        >>> isclose(area, 0.8 * 0.6 + 0.3 * 1.6 - 0.1 * 0.2)
        True

    Same specifications as :meth:`mask_area`.
    """
    dim = len(inf)
    limits = [sorted({mask[d][0] for mask in masks}.union({inf[d], sup[d]})) for d in range(dim)]
    medians_and_lengths = [
        [((limits[d][i + 1] + limits[d][i]) / 2, limits[d][i + 1] - limits[d][i]) for i in range(len(limits[d]) - 1)]
        for d in range(dim)]
    area = 0
    for point in product(*medians_and_lengths):
        if any([all([(point[d][0] > mask[d][0]) == mask[d][1] for d in range(dim)]) for mask in masks]):
            area += np.prod([point[d][1] for d in range(dim)])
    return area


def masks_area(inf, sup, masks):
    """
    Area of some masks (recursive `divide and conquer` implementation).

    Denote ``dim`` the dimension of the Euclidean space under study.

    :param inf: a list of ``d`` numbers. The inf limit of the bounding rectangle in each dimension.
    :param sup: a list of ``d`` numbers. The sup limit of the bounding rectangle in each dimension.
    :param masks: a list of masks. Each mask is a list of ``d`` pairs ``(lim, direction)``, where ``lim`` is the limit
        of the mask, and ``direction`` is a Boolean: ``True`` (resp ``False``) means that the points of the mask
        meet the condition ``x_d >= lim`` (resp. x_d <= lim).

        >>> area = masks_area(inf=[0, 0], sup=[1, 2], masks=[[(.2, True), (.6, False)], [(.3, False), (.4, True)]])
        >>> isclose(area, 0.8 * 0.6 + 0.3 * 1.6 - 0.1 * 0.2)
        True

    Bounding rectangle: points where ``0 <= x_1 <= 1 and 0 <= x_2 <= 2``.
    First mask: points where ``x_1 >= 0.2 and x_2 <= 0.6``.
    Second mask: points where ``x_1 <= 0.3 and x_2 >= 0.4``.

    The function returns the area of ``Intersection(bounding rectangle, Union(masks))``.
    """
    dim = len(inf)
    # Is there a mask covering everything?
    if any([all([(mask[d][0] <= inf[d]) if mask[d][1] else (mask[d][0] >= sup[d]) for d in range(dim)])
            for mask in masks]):
        return np.prod([high - low for (low, high) in zip(inf, sup)])
    # Eliminate empty masks
    new_masks = [mask for mask in masks
                 if not any([(mask[d][0] >= sup[d]) if mask[d][1] else (mask[d][0] <= inf[d]) for d in range(dim)])]
    if not new_masks:
        return 0
    mask = random.choice(new_masks)
    d_lim = random.choice([d for d in range(dim) if inf[d] < mask[d][0] < sup[d]])
    lim = mask[d_lim][0]
    return (masks_area(inf, [lim if d == d_lim else sup[d] for d in range(dim)], new_masks)
            + masks_area([lim if d == d_lim else inf[d] for d in range(dim)], sup, new_masks))


def masks_distribution_naive(inf, sup, masks):
    """
    Distribution of the number of masks. Naive implementation (used as a sanity test for the recursive implementation)

        >>> histogram = masks_distribution_naive(inf=[0, 0], sup=[1, 2],
        ...                                      masks=[[(.2, True), (.6, False)], [(.3, False), (.4, True)]])
        >>> histogram
        array([1.06, 0.92, 0.02])

    Same specifications as :meth:`mask_distribution`.
    """
    dim = len(inf)
    limits = [sorted({mask[d][0] for mask in masks}.union({inf[d], sup[d]})) for d in range(dim)]
    medians_and_lengths = [
        [((limits[d][i + 1] + limits[d][i]) / 2, limits[d][i + 1] - limits[d][i]) for i in range(len(limits[d]) - 1)]
        for d in range(dim)]
    histogram = np.zeros(dim + 1)
    for point in product(*medians_and_lengths):
        n_masks = np.sum([all([(point[d][0] > mask[d][0]) == mask[d][1] for d in range(dim)]) for mask in masks])
        area = np.prod([point[d][1] for d in range(dim)])
        histogram[n_masks] += area
    return histogram


def masks_distribution(inf, sup, masks, histogram=None, cover_alls=0):
    """
    Distribution of the number of masks (recursive `divide and conquer` implementation).

    Denote ``dim`` the dimension of the Euclidean space under study.

    :param inf: a list of ``d`` numbers. The inf limit of the bounding rectangle in each dimension.
    :param sup: a list of ``d`` numbers. The sup limit of the bounding rectangle in each dimension.
    :param masks: a list of masks. Each mask is a list of ``d`` pairs ``(lim, direction)``, where ``lim`` is the limit
        of the mask, and ``direction`` is a Boolean: ``True`` (resp ``False``) means that the points of the mask
        meet the condition ``x_d >= lim`` (resp. x_d <= lim).
    :param histogram: a list. This parameter should only be used for recursive calls. If specified, then instead of
        creating a new list for the output, it is added to the given list ``histogram``.
    :param cover_alls: an int. This parameter should only be used for recursive calls. If specified, then we consider
        that we have this number of implicit masks (i.e. not given in the argument ``masks``) that cover the whole area.
    :return: a list of length ``dim + 1``. The ``i``-th coefficient is the area covered by ``i`` masks exactly (in
        the bounding rectangle).

        >>> histogram = masks_distribution(inf=[0, 0], sup=[1, 2],
        ...                                masks=[[(.2, True), (.6, False)], [(.3, False), (.4, True)]])
        >>> histogram
        array([1.06, 0.92, 0.02])

    Bounding rectangle: points where ``0 <= x_1 <= 1 and 0 <= x_2 <= 2``.
    First mask: points where ``x_1 >= 0.2 and x_2 <= 0.6``.
    Second mask: points where ``x_1 <= 0.3 and x_2 >= 0.4``.
    """
    dim = len(inf)
    if histogram is None:
        histogram = np.zeros(dim + 1)
    # Eliminate empty masks
    new_masks = [mask for mask in masks
                 if not any([(mask[d][0] >= sup[d]) if mask[d][1] else (mask[d][0] <= inf[d]) for d in range(dim)])]
    # Detect the new cover-alls (masks covering everything)
    cover_alls += np.sum([all([(mask[d][0] <= inf[d]) if mask[d][1] else (mask[d][0] >= sup[d]) for d in range(dim)])
                          for mask in new_masks], dtype=int)
    new_masks = [mask for mask in new_masks
                 if not all([(mask[d][0] <= inf[d]) if mask[d][1] else (mask[d][0] >= sup[d]) for d in range(dim)])]
    if not new_masks:
        area = np.prod([high - low for (low, high) in zip(inf, sup)])
        histogram[cover_alls] += area
    else:
        mask = random.choice(new_masks)
        d_lim = random.choice([d for d in range(dim) if inf[d] < mask[d][0] < sup[d]])
        lim = mask[d_lim][0]
        masks_distribution(inf, [lim if d == d_lim else sup[d] for d in range(dim)], new_masks, histogram, cover_alls)
        masks_distribution([lim if d == d_lim else inf[d] for d in range(dim)], sup, new_masks, histogram, cover_alls)
    return histogram


def winners_distribution(inf, sup, masks_winners, histogram=None, cover_alls=None):
    """
    Distribution of the number of winners (recursive `divide and conquer` implementation).

    Denote ``dim`` the dimension of the Euclidean space under study.

    :param inf: a list of ``d`` numbers. The inf limit of the bounding rectangle in each dimension.
    :param sup: a list of ``d`` numbers. The sup limit of the bounding rectangle in each dimension.
    :param masks_winners: a list of couples ``(mask, winners)``. A mask is defined as usual. A winner is a set of
        winning candidates in this mask, e.g. {'a', 'b'}.
    :param histogram: a list. This parameter should only be used for recursive calls. If specified, then instead of
        creating a new list for the output, it is added to the given list ``histogram``.
    :param cover_alls: a set. e.g. {'a', 'b'}. This parameter should only be used for recursive calls. If specified,
        then we consider that we have all these candidates winning in the whole area.
    :return: a list of length 4. The ``i``-th coefficient is the area where ``i`` candidates may win.

        >>> histogram = winners_distribution(
        ...     inf=[0, 0], sup=[1, 2],
        ...     masks_winners=[([(.2, True), (.6, False)], {'a'}), ([(.3, False), (.4, True)], {'a', 'b'})])
        >>> histogram
        array([1.06, 0.46, 0.48, 0.  ])

    Bounding rectangle: points where ``0 <= x_1 <= 1 and 0 <= x_2 <= 2``.
    First mask: points where ``x_1 >= 0.2 and x_2 <= 0.6``. Winner ``{'a'}``.
    Second mask: points where ``x_1 <= 0.3 and x_2 >= 0.4``. Winner ``{'b'}``.
    """
    dim = len(inf)
    if histogram is None:
        histogram = np.zeros(4)
    if cover_alls is None:
        cover_alls = set()
    # Eliminate empty masks
    new_mw = [(mask, winners) for mask, winners in masks_winners
              if not any([(mask[d][0] >= sup[d]) if mask[d][1] else (mask[d][0] <= inf[d]) for d in range(dim)])
              and not winners.issubset(cover_alls)]
    # Detect the new cover-alls (masks covering everything)
    toto = set.union(*([set()] + [
        winners
        for mask, winners in new_mw
        if all([(mask[d][0] <= inf[d]) if mask[d][1] else (mask[d][0] >= sup[d]) for d in range(dim)])
    ]))
    cover_alls = cover_alls.union(toto)
    new_mw = [(mask, winners) for mask, winners in new_mw
              if not all([(mask[d][0] <= inf[d]) if mask[d][1] else (mask[d][0] >= sup[d]) for d in range(dim)])]
    if not new_mw:
        area = np.prod([high - low for (low, high) in zip(inf, sup)])
        histogram[len(cover_alls)] += area
    else:
        mask, _ = random.choice(new_mw)
        d_lim = random.choice([d for d in range(dim) if inf[d] < mask[d][0] < sup[d]])
        lim = mask[d_lim][0]
        winners_distribution(inf, [lim if d == d_lim else sup[d] for d in range(dim)], new_mw, histogram, cover_alls)
        winners_distribution([lim if d == d_lim else inf[d] for d in range(dim)], sup, new_mw, histogram, cover_alls)
    return histogram


def random_mask(dim):
    """
    Random mask.

    :param dim: dimension of the Euclidean space.
    :return: a mask of dimension ``d``, whose limits are in [0, 1].

    Cf. :meth:`mask_area`.
    """
    return [(random.random(), random.choice([True, False])) for _ in range(dim)]


def random_masks(dim, n_masks):
    """
    List of random masks.

    :param dim: dimension of the Euclidean space.
    :param n_masks: number of masks.
    :return: a list of ``n_masks`` masks of dimension ``d``, whose limits are in [0, 1].

        >>> dim = 6
        >>> n_masks = 4
        >>> masks = random_masks(dim=dim, n_masks=n_masks)
        >>> isclose(masks_area(inf=[0]*dim, sup=[1]*dim, masks=masks),
        ...         masks_area_naive(inf=[0]*dim, sup=[1]*dim, masks=masks))
        True

    Cf. :meth:`mask_area`.
    """
    return [random_mask(dim) for _ in range(n_masks)]
