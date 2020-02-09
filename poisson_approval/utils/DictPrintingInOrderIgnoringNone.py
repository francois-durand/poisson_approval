class DictPrintingInOrderIgnoringNone(dict):
    """A dictionary that prints in the order of the keys, ignoring value None.

    Examples
    --------
        >>> d = DictPrintingInOrderIgnoringNone({'b': 'x', 'a': 'y', 'c': 'z', 'd': 0, 'e': None, 'f': []})
        >>> print(d)
        {a: y, b: x, c: z, d: 0, f: []}
        >>> print(repr(d))
        {'a': 'y', 'b': 'x', 'c': 'z', 'd': 0, 'f': []}
    """

    def __repr__(self):
        return "{" + ", ".join([
            "%r: %r" % (key, self[key]) for key in sorted(self)
            if self[key] is not None
        ]) + "}"

    def __str__(self):
        return "{" + ", ".join([
            "%s: %s" % (key, self[key]) for key in sorted(self)
            if self[key] is not None
        ]) + "}"

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')
