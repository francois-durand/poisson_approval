def is_hater(weak_order):
    """Whether a weak order represents a "hater".

    Parameters
    ----------
    weak_order : str
        A weak order, e.g. ``'a>b~c'``, ``'a~b>c'``, etc.

    Returns
    -------
    bool
        True iff the weak order is of the form ``'a~b>c'``.

    Examples
    --------
        >>> is_hater('a~b>c')
        True
    """
    return weak_order[3] == '>'


def is_lover(weak_order):
    """Whether a weak order represents a "lover".

    Parameters
    ----------
    weak_order : str
        A weak order, e.g. ``'a>b~c'``, ``'a~b>c'``, etc.

    Returns
    -------
    bool
        True iff the weak order is of the form ``'a>b~c'``.

    Examples
    --------
        >>> is_lover('a>b~c')
        True
    """
    return weak_order[1] == '>'


def is_weak_order(o):
    """Whether an object is a weak order.

    Parameters
    ----------
    o : object

    Returns
    -------
    bool
        True iff `o` is a string that represent a weak order, i.e. of the form 'a>b~c' (lover) or 'a~b>c' (hater).

    Examples
    --------
        >>> is_weak_order('a>b~c')
        True
        >>> is_weak_order('a>b~')
        False
        >>> is_weak_order(42)
        False
    """
    return isinstance(o, str) and len(o) == 5 and {o[1], o[3]} == {'>', '~'}


def sort_weak_order(weak_order):
    """Put a weak order in normalized format (with the indifferent candidates sorted alphabetically).

    Parameters
    ----------
    weak_order : str
        A weak order, e.g. ``'a>b~c'``, ``'a~b>c'``, etc.

    Returns
    -------
    str
        The same weak order in normalized format.

    Examples
    --------
        >>> sort_weak_order('a>c~b')
        'a>b~c'
        >>> sort_weak_order('b~a>c')
        'a~b>c'
    """
    if is_lover(weak_order):
        return weak_order[0] + '>' + '~'.join(sorted([weak_order[2], weak_order[4]]))
    else:
        return '~'.join(sorted([weak_order[0], weak_order[2]])) + '>' + weak_order[4]
