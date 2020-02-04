from poisson_approval.utils.UtilCache import cached_property


def test():
    """
    In the following example, in the last instruction, foo must not be computed again:

        >>> class MyClass:
        ...
        ...     @cached_property
        ...     def foo(self):
        ...         print('Computing foo...')
        ...         return 'result_foo'
        ...
        ...     @cached_property
        ...     def foobar(self):
        ...         print('Computing foobar...')
        ...         return self.foo + 'bar'
        >>> my_object = MyClass()
        >>> print(my_object.foobar)
        Computing foobar...
        Computing foo...
        result_foobar
        >>> print(my_object.foo)
        result_foo
    """
    pass
