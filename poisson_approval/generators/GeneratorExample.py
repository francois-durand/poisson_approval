from poisson_approval.utils.Util import initialize_random_seeds


class GeneratorExample:
    """A generator of `something` that meets a given test.

    Parameters
    ----------
    generator : callable or tuple
        This can be:

        * Either a callable that takes no input and that outputs a (random) `something`,
        * Or a tuple of such generators (cf. examples below).
    test : callable
        A function that take as input(s) the output(s) of the generator(s) and that returns a Boolean.
    n_trials_max : int or None
        The maximum number of trials. If None, then attempts will be made until finding an example. The option None
        should be used with extreme care since it may lead to an infinite loop.

    Returns
    -------
    object or tuple or None
        If there is one generator, then return a `something` that meets the given `test`. If there is a tuple of
        generators, then return a tuple of generated objects that meets the given `test`. In both cases, if no example
        is found within `n_trials_max` attempts, then return None.

    Examples
    --------
    In this basic example with one generator, we generate a random integer between 0 included and 100 excluded that
    is divisible by 7:

        >>> import numpy as np
        >>> initialize_random_seeds()
        >>> def generator_integer():
        ...     return np.random.randint(0, 100)
        >>> def test_divisible_7(n):
        ...     return n % 7 == 0
        >>> generator_example = GeneratorExample(generator=generator_integer,
        ...                                      test=test_divisible_7, n_trials_max=None)
        >>> generator_example()
        21

    In this example with a tuple of generators, we generate a random 2*2 matrix and a random vector of size 2, both
    with integer coefficients between -10 included and 11 excluded, such that their dot product is null, but without
    being null themselves:

        >>> import numpy as np
        >>> initialize_random_seeds()
        >>> def generator_matrix():
        ...     return np.random.randint(-10, 11, (2, 2))
        >>> def generator_vector():
        ...     return np.random.randint(-10, 11, 2)
        >>> def test_non_trivial_dot_zero(matrix, vector):
        ...     return (np.all(np.dot(matrix, vector) == 0)
        ...             and not np.all(matrix == 0) and not np.all(vector == 0))
        >>> generator_example = GeneratorExample(generator=(generator_matrix, generator_vector),
        ...                                      test=test_non_trivial_dot_zero, n_trials_max=None)
        >>> matrix, vector = generator_example()
        >>> matrix
        array([[ 2, -8],
               [-1,  4]])
        >>> vector
        array([-4, -1])

    When no example is found, the generator returns None:

        >>> import numpy as np
        >>> def generator_integer():
        ...     return np.random.randint(0, 100)
        >>> def is_negative(n):
        ...     return n < 0
        >>> generator_example = GeneratorExample(generator=generator_integer,
        ...                                      test=is_negative, n_trials_max=100)
        >>> n = generator_example()
        >>> print(n)
        None
    """

    def __init__(self, generator, test, n_trials_max):
        self.generator = generator
        self.test = test
        self.n_trials_max = n_trials_max

    def __call__(self):
        i = 0
        while self.n_trials_max is None or i < self.n_trials_max:
            i += 1
            if isinstance(self.generator, tuple):
                somethings = [g() for g in self.generator]
                if self.test(*somethings):
                    return tuple(somethings)
            else:
                something = self.generator()
                if self.test(something):
                    return something
        return None
