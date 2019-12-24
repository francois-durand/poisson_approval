def _cache(f):
    """Auxiliary decorator used by :meth:`cached_property`.

    Parameters
    ----------
    f : callable
        A method with no argument (except ``self``).

    Returns
    -------
    callable
        The same function, but with a `caching` behavior.

    Notes
    -----
    In practice, the values are stored in an attribute of the object that is a dictionary called ``_cached_properties``.
    For example, consider a method ``foo(self)``.

        * If the value is not computed yet, the decorated method will compute the value, store it in
          ``self._cached_properties['foo']`` and return it.
        * If the value is already computed, the decorated method will get it from ``self._cached_properties['foo']``
          and return it.
    """
    name = f.__name__

    # noinspection PyProtectedMember
    def _f(*args):
        try:
            return args[0]._cached_properties[name]
        except KeyError:
            # Not stored in cache
            value = f(*args)
            args[0]._cached_properties[name] = value
            return value
        except AttributeError:
            # cache does not even exist
            value = f(*args)
            args[0]._cached_properties = {name: value}
            return value
    _f.__doc__ = f.__doc__
    return _f


def cached_property(f):
    """Decorator used in replacement of ``@property`` to put the value in cache automatically.

    Notes
    -----
    The first time the attribute is used, it is computed on-demand and put in cache. Later accesses to the
    attributes will use the cached value.

    Cf. :class:`DeleteCacheMixin` for an example.
    """
    return property(_cache(f))


class DeleteCacheMixin:
    """Mixin used to delete cached properties.

    Notes
    -----
    Cf. decorator :meth:`cached_property`.

    Examples
    --------
        >>> class Example(DeleteCacheMixin):
        ...     @cached_property
        ...     def x(self):
        ...         print('Big computation...')
        ...         return 6 * 7
        >>> a = Example()
        >>> a.x
        Big computation...
        42
        >>> a.x
        42
        >>> a.delete_cache()
        >>> a.x
        Big computation...
        42
    """

    # noinspection PyAttributeOutsideInit
    def delete_cache(self) -> None:
        self._cached_properties = dict()
