import numpy as np
import random
import itertools
from math import sqrt, log
from fractions import Fraction
from poisson_approval.constants.constants import *
from poisson_approval.utils.DictPrintingInOrder import DictPrintingInOrder
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros


def initialize_random_seeds(n=0):
    """Initialize the random seeds.

    Parameters
    ----------
    n : int
        The desired random seed. Default: 0.
    """
    random.seed(n)
    np.random.seed(n)


def rand_simplex(d=6):
    """Draw a random point in the simplex.

    Parameters
    ----------
    d : int
        Number of coordinates. In other words, we consider the simplex of dimension `d - 1`.

    Returns
    -------
    numpy.ndarray
        A numpy array of length `d`, whose sum is 1.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> rand_simplex(d=6)  # doctest: +SKIP
        array([0.4236548 , 0.12122838, 0.00393032, 0.05394987, 0.11242599, 0.28481063])
    """
    x = np.sort(np.random.rand(d - 1))
    return np.concatenate((x, [1])) - np.concatenate(([0], x))


def rand_integers_fixed_sum(n_integers, fixed_sum):
    """Generate integers with a given sum (uniformly).

    Parameters
    ----------
    n_integers : int
        The desired number of integers.
    fixed_sum : int
        The fixed sum.

    Returns
    -------
    numpy.ndarray
        A numpy array of `d` integers, whose sum is `fixed_sum`, and drawn uniformly.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> rand_integers_fixed_sum(n_integers=6, fixed_sum=100)
        array([ 2, 23, 34,  0, 22, 19])
    """
    n_separators = n_integers - 1
    separators = np.concatenate((
        [-1],
        np.sort(np.random.choice(fixed_sum + n_separators, n_separators, replace=False)),
        [fixed_sum + n_separators]))
    return np.array([up - down - 1 for down, up in zip(separators[:-1], separators[1:])])


def rand_simplex_grid(d, denominator):
    """Draw a random point in the simplex, with rational coordinates of a given denominator

    Parameters
    ----------
    d : int
        Number of coordinates. In other words, we consider the simplex of dimension `d - 1`.
    denominator : int
        The coordinates will be fractions with this denominator.

    Returns
    -------
    numpy.ndarray
        A numpy array of length `d`, whose coordinates are fractions of the given denominator, and whose sum is 1.

    Examples
    --------
        >>> initialize_random_seeds()
        >>> rand_simplex_grid(d=3, denominator=100)
        array([Fraction(13, 50), Fraction(13, 20), Fraction(9, 100)], dtype=object)
    """
    return np.array([
        Fraction(int(n), denominator)
        for n in rand_integers_fixed_sum(n_integers=d, fixed_sum=denominator)])


def probability(generator, n_samples, test, conditional_on=None):
    """Probability that a random `something` meets some given test.

    Parameters
    ----------
    generator : callable or tuple
        This can be:

        * Either a callable that takes no input and that outputs a (random) `something`,
        * Or a tuple of such generators (cf. examples below).
    n_samples : int
        Number of samples.
    test : callable
        A function that take as input(s) the output(s) of the generator(s) and that returns a Boolean.
    conditional_on : callable
        A function that take as input(s) the output(s) of the generator(s) and that returns a Boolean.
        Default: always True.

    Returns
    -------
    float
        The probability that the output(s) generated by `generator` meet(s) `test`, conditional on the fact
        that it meets `conditional_on`, based on a Monte-Carlo estimation of `n_samples` trials.

    Examples
    --------
    In this basic example with one generator, we estimate the probability that a random float between 0 and 1 is greater
    than .5, conditionally on being greater than .25:

        >>> import random
        >>> initialize_random_seeds()
        >>> def generator():
        ...     return random.random()
        >>> probability(generator, n_samples=1000, test=lambda x: x > .5, conditional_on=lambda x: x > .25)
        0.661

    In this example with a tuple of generators, we estimate the probability that a random 2*2 matrix and a random vector
    of size 2, both with integer coefficients between -10 included and 11 excluded, have a dot product that is null,
    conditionally on not being null themselves:

        >>> import numpy as np
        >>> initialize_random_seeds()
        >>> def generator_matrix():
        ...     return np.random.randint(-10, 11, (2, 2))
        >>> def generator_vector():
        ...     return np.random.randint(-10, 11, 2)
        >>> def test_dot_zero(matrix, vector):
        ...     return np.all(np.dot(matrix, vector) == 0)
        >>> def test_non_trivial(matrix, vector):
        ...     return not np.all(matrix == 0) and not np.all(vector == 0)
        >>> probability(generator=(generator_matrix, generator_vector), n_samples=10000,
        ...             test=test_dot_zero, conditional_on=test_non_trivial)
        0.0003
    """
    if not isinstance(generator, tuple):
        generator = (generator, )
    success = 0
    i_samples = 0
    while i_samples < n_samples:
        somethings = [g() for g in generator]
        if conditional_on is None or conditional_on(*somethings):
            i_samples += 1
            if test(*somethings):
                success += 1
    return success / n_samples


def image_distribution(generator, n_samples, f, conditional_on=None):
    """Distribution of ``f(something)`` for a random `something`.

    Parameters
    ----------
    generator : callable or tuple
        This can be:

        * Either a callable that takes no input and that outputs a (random) `something`,
        * Or a tuple of such generators (cf. examples below).
    n_samples : int
        Number of samples.
    f : callable
        A function that take as input(s) the output(s) of the generator(s)..
    conditional_on : callable
        A function that take as input(s) the output(s) of the generator(s) and that returns a Boolean.
        Default: always True.

    Returns
    -------
    DictPrintingInOrder
        Keys: the obtained outputs for `f`. Values: the probability that `f(something)` has this output when `something`
        is generated by `generator`, conditional on the fact that it meets `conditional_on`,
        based on a Monte-Carlo estimation of `n_samples` trials.

    Examples
    --------
    In this basic example with one generator, we compute the distribution of `n` modulo 10, when `n` is drawn uniformly
    at random between 0 included and 100 excluded, conditionally on the fact that `n` is even:

        >>> import numpy as np
        >>> initialize_random_seeds()
        >>> def generator_integer():
        ...     return np.random.randint(0, 100)
        >>> def modulo_10(n):
        ...     return n % 10
        >>> def is_even(n):
        ...     return n % 2 == 0
        >>> image_distribution(generator=generator_integer, n_samples=100, f=modulo_10, conditional_on=is_even)
        {0: 0.21, 2: 0.21, 4: 0.2, 6: 0.18, 8: 0.2}

    In this example with a tuple of generator, we compute the distribution of `a mod b`, when `a` is drawn uniformly
    at random between 0 included and 100 excluded, and `b` is drawn uniformly at random between 1 included and 11
    excluded:

        >>> import numpy as np
        >>> initialize_random_seeds()
        >>> def generator_integer():
        ...     return np.random.randint(0, 100)
        >>> def generator_divider():
        ...     return np.random.randint(1, 11)
        >>> def modulo(a, b):
        ...     return a % b
        >>> image_distribution(generator=(generator_integer, generator_divider),
        ...                    n_samples=100, f=modulo)
        {0: 0.31, 1: 0.16, 2: 0.18, 3: 0.12, 4: 0.07, 5: 0.04, 6: 0.02, 7: 0.08, 9: 0.02}
    """
    if not isinstance(generator, tuple):
        generator = (generator, )
    d_result_occurrences = dict()
    i_samples = 0
    while i_samples < n_samples:
        somethings = [g() for g in generator]
        if conditional_on is None or conditional_on(*somethings):
            i_samples += 1
            result = f(*somethings)
            d_result_occurrences[result] = d_result_occurrences.get(result, 0) + 1
    return DictPrintingInOrder({result: occurrences / n_samples
                                for result, occurrences in d_result_occurrences.items()})


def _false_for_fraction(f):
    """Decorator to return False when the input is a Fraction (cf. usages below)."""
    def _f(x):
        if isinstance(x, Fraction):
            return False
        return f(x)
    _f.__doc__ = f.__doc__
    return _f


@_false_for_fraction
def isnan(x):
    """Is nan.

    Parameters
    ----------
    x : Number

    Returns
    -------
    bool
        True if `x` is nan.

    Notes
    -----
    This extends the usual numpy function ``isnan`` to fractions.

    Examples
    --------
        >>> from fractions import Fraction
        >>> isnan(Fraction(1, 10))
        False
        >>> isnan(1)
        False
        >>> isnan(np.nan)
        True
    """
    return np.isnan(x)


@_false_for_fraction
def isposinf(x):
    """Is positive infinity.

    Parameters
    ----------
    x : Number

    Returns
    -------
    bool
        True if `x` is positive infinity.

    Notes
    -----
    This extends the usual numpy function ``isposinf`` to fractions.

    Examples
    --------
        >>> from fractions import Fraction
        >>> isposinf(Fraction(1, 10))
        False
        >>> isposinf(1)
        False
        >>> isposinf(np.inf)
        True
    """
    return np.isposinf(x)


@_false_for_fraction
def isneginf(x):
    """Is negative infinity.

    Parameters
    ----------
    x : Number

    Returns
    -------
    bool
        True if `x` is negative infinity.

    Notes
    -----
    This extends the usual numpy function ``isneginf`` to fractions.

    Examples
    --------
        >>> from fractions import Fraction
        >>> isposinf(Fraction(1, 10))
        False
        >>> isneginf(1)
        False
        >>> isneginf(- np.inf)
        True
    """
    return np.isneginf(x)


def sort_ballot(ballot):
    """Put a ballot in alphabetical order.

    Parameters
    ----------
    ballot : str
        A ballot, e.g. ``'a'``, ``'ab'``, ``'ba'``, etc.

    Returns
    -------
    str
        The same ballot in alphabetical order.

    Examples
    --------
        >>> sort_ballot('a')
        'a'
        >>> sort_ballot('ab')
        'ab'
        >>> sort_ballot('ba')
        'ab'
    """
    return ''.join(sorted(ballot))


def ballot_one(ranking):
    """Ballot for the voter's preferred candidate.

    Parameters
    ----------
    ranking : str
        A ranking.

    Returns
    -------
    str
        The first candidate.

    Examples
    --------
        >>> ballot_one('abc')
        'a'
    """
    return ranking[0]


def ballot_two(ranking):
    """Ballot for the voter's second most-liked candidate.

    Parameters
    ----------
    ranking : str
        A ranking.

    Returns
    -------
    str
        The second candidate.

    Examples
    --------
        >>> ballot_two('abc')
        'b'
    """
    return ranking[1]


def ballot_one_two(ranking):
    """Ballot for the voter's two preferred candidates.

    Parameters
    ----------
    ranking : str
        A ranking.

    Returns
    -------
    str
        The ballot with the two first candidates.

    Examples
    --------
        >>> ballot_one_two('abc')
        'ab'
        >>> ballot_one_two('bac')
        'ab'
    """
    return sort_ballot(ranking[:2])


def ballot_one_three(ranking):
    """Ballot for the voter's first and third candidates.

    Parameters
    ----------
    ranking : str
        A ranking.

    Returns
    -------
    str
        The ballot with the first and third candidates.

    Examples
    --------
        >>> ballot_one_three('abc')
        'ac'
        >>> ballot_one_three('cba')
        'ac'
    """
    return sort_ballot(ranking[0] + ranking[2])


def ballot_low_u(ranking, voting_rule):
    """Ballot chosen by the voters who have a low utility for their middle candidate.

    Parameters
    ----------
    ranking : str
        A ranking.
    voting_rule : str
        The voting rule. Possible values are ``APPROVAL``, ``PLURALITY`` and ``ANTI_PLURALITY``.

    Returns
    -------
    str
        The ballot chosen by the voters with this ranking and a low utility for their middle candidate, in case
        the response is utility-dependent.

    Examples
    --------
        >>> ballot_low_u('abc', APPROVAL)
        'a'
        >>> ballot_low_u('abc', PLURALITY)
        'a'
        >>> ballot_low_u('abc', ANTI_PLURALITY)
        'ac'
    """
    if voting_rule in {APPROVAL, PLURALITY}:
        return ballot_one(ranking)
    elif voting_rule == ANTI_PLURALITY:
        return ballot_one_three(ranking)
    else:
        raise NotImplementedError


def ballot_high_u(ranking, voting_rule):
    """Ballot chosen by the voters who have a high utility for their middle candidate.

    Parameters
    ----------
    ranking : str
        A ranking.
    voting_rule : str
        The voting rule. Possible values are ``APPROVAL``, ``PLURALITY`` and ``ANTI_PLURALITY``.

    Returns
    -------
    str
        The ballot chosen by the voters with this ranking and a high utility for their middle candidate, in case
        the response is utility-dependent.

    Examples
    --------
        >>> ballot_high_u('abc', APPROVAL)
        'ab'
        >>> ballot_high_u('abc', PLURALITY)
        'b'
        >>> ballot_high_u('abc', ANTI_PLURALITY)
        'ab'
    """
    if voting_rule in {APPROVAL, ANTI_PLURALITY}:
        return ballot_one_two(ranking)
    elif voting_rule == PLURALITY:
        return ballot_two(ranking)
    else:
        raise NotImplementedError


def give_figure(n, singular, plural=None):
    """Combine a number with a unit, whose word can be singular or plural.

    Parameters
    ----------
    n : int
        The number.
    singular : str
        The singular word.
    plural : str
        The plural word. Default: the singular with a final 's'.

    Returns
    -------
    str
        The number and the word.

    Examples
    --------
        >>> give_figure(1, 'apple')
        '1 apple'
        >>> give_figure(2, 'apple')
        '2 apples'
        >>> give_figure(1, 'equilibrium', 'equilibria')
        '1 equilibrium'
        >>> give_figure(2, 'equilibrium', 'equilibria')
        '2 equilibria'
    """
    if n <= 1:
        return str(n) + ' ' + singular
    else:
        if plural is None:
            return str(n) + ' ' + singular + 's'
        else:
            return str(n) + ' ' + plural


def barycenter(a, b, ratio_b):
    """Barycenter.

    Parameters
    ----------
    a : Number
    b : Number or iterable
    ratio_b : Number or iterable
        The ratio of `b` in the result. If an iterable, must be the same size as `b`.

    Returns
    -------
    Number
        The result of ``(1 - ratio_b) * a + ratio_b * b``. The added value of this function is to preserve the type
        of `a` (resp. `b`) when `ratio_b` is 0 (resp. 1). If `b` and `ratio_b` are iterable, return
        ``(1 - sum(ratio_b)) * a + sum(ratio_b * b)``.

    Examples
    --------
    In this first example, `barycenter` preserves the type Fraction, whereas a naive computation returns a float:

        >>> a, b = Fraction(1, 10), 0.7
        >>> ratio_b = 0
        >>> barycenter(a, b, ratio_b)
        Fraction(1, 10)
        >>> (1 - ratio_b) * a + ratio_b * b
        0.1

    The second example is symmetric of the first one, in the sense that it preserves the type of `b`:

        >>> a, b = 0.7, 42
        >>> ratio_b = 1
        >>> barycenter(a, b, ratio_b)
        42
        >>> (1 - ratio_b) * a + ratio_b * b
        42.0

    In the following example, `b` and `ratio_b` are iterables:

        >>> a = 0
        >>> b = [-1 , 1]
        >>> barycenter(0, [-1, 1], [Fraction(2, 10), Fraction(3, 10)])
        Fraction(1, 10)
    """
    def multiply(ratio, x):
        """Does not contaminate with `x`'s type if `ratio` == 0"""
        return 0 if ratio == 0 else ratio * x
    try:
        # b and ratio_b are numbers
        return multiply(1 - ratio_b, a) + multiply(ratio_b, b)
    except TypeError:
        # b and ratio_b are iterables
        ratio_a = 1 - sum(ratio_b)
        return multiply(ratio_a, a) + sum([multiply(r, x) for r, x in zip(b, ratio_b)])


def to_callable(o):
    """Convert to a callable.

    Parameters
    ----------
    o : object

    Returns
    -------
    callable
        The conversion of `o` to a callable.

    Examples
    --------
    If `o` is callable, then return `o`:

        >>> def square(x):
        ...     return x**2
        >>> my_function = to_callable(square)
        >>> my_function(4)
        16

    If `o` is not callable, then return a function ``*args, **kwargs -> o``:

        >>> x = 42
        >>> my_function = to_callable(x)
        >>> my_function('some_argument', keyword='some_value')
        42
    """
    if callable(o):
        return o
    else:
        def my_function(*args, **kwargs):
            return o
        return my_function


def product_dict(d_key_possible_values):
    """Iterable: product of dictionaries.

    Source: https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists.

    Parameters
    ----------
    d_key_possible_values
        To each key, associate a list of possible values (cf. example below).

    Yields
    ------
    dict
        A dictionary that, to each key, associates one of its possible values. All elements of the Cartesian product
        are returned this way.

    Examples
    --------
        >>> d_key_possible_values = {'foo': [0, 1], 'bar': ['a', 'b', 'c']}
        >>> for d_key_value in product_dict(d_key_possible_values):
        ...     print(d_key_value)
        {'foo': 0, 'bar': 'a'}
        {'foo': 0, 'bar': 'b'}
        {'foo': 0, 'bar': 'c'}
        {'foo': 1, 'bar': 'a'}
        {'foo': 1, 'bar': 'b'}
        {'foo': 1, 'bar': 'c'}
    """
    keys = d_key_possible_values.keys()
    vals = d_key_possible_values.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def candidates_to_d_candidate_probability(candidates):
    """Convert a set of candidates to a dictionary of probabilities (random tie-break).

    Parameters
    ----------
    candidates : set
        A subset of ``{'a', 'b', 'c'}``. Typically: a set of winners.

    Returns
    -------
    DictPrintingInOrderIgnoringZeros
        Key: ``'a'``, ``'b'`` or ``'c'``. Value: the probability of this candidate winning with a uniformly random
        tie-break.

    Examples
    --------
        >>> winners = {'a', 'b'}
        >>> candidates_to_d_candidate_probability(winners)
        {'a': Fraction(1, 2), 'b': Fraction(1, 2)}
    """
    n_candidates = len(candidates)
    return DictPrintingInOrderIgnoringZeros({
        candidate: Fraction(1, n_candidates) if candidate in candidates else 0 for candidate in CANDIDATES})


def candidates_to_probabilities(candidates):
    """Convert a set of candidates to an array of probabilities (random tie-break).

    Parameters
    ----------
    candidates : set
        A subset of ``{'a', 'b', 'c'}``. Typically: a set of winners.

    Returns
    -------
    ndarray
        Array of size 3. For example, the first coefficient is the probability that candidate `a` win by a random
        tie-break.

    Examples
    --------
        >>> winners = {'a', 'b'}
        >>> candidates_to_probabilities(winners)
        array([Fraction(1, 2), Fraction(1, 2), 0], dtype=object)
    """
    n_candidates = len(candidates)
    return np.array([Fraction(1, n_candidates) if candidate in candidates else 0 for candidate in CANDIDATES])


def array_to_d_candidate_value(values):
    """Convert an array to a dictionary of candidates and values

    Parameters
    ----------
    values : ndarray
        An array of size 3.

    Returns
    -------
    DictPrintingInOrderIgnoringZeros
        The corresponding dictionary.

    Examples
    --------
        >>> values = [42, 51, 69]
        >>> array_to_d_candidate_value(values)
        {'a': 42, 'b': 51, 'c': 69}
    """
    return DictPrintingInOrderIgnoringZeros({candidate: value for candidate, value in zip(CANDIDATES, values)})


def d_candidate_value_to_array(d_candidate_value):
    """Convert a dictionary of candidates and values to an array

    Parameters
    ----------
    d_candidate_value : dict
        Key: ``'a'``, ``'b'`` or ``'c'``.

    Returns
    -------
    ndarray
        The corresponding array.

    Examples
    --------
        >>> d_candidate_value = {'a': 42, 'b': 51, 'c': 69}
        >>> d_candidate_value_to_array(d_candidate_value)
        array([42, 51, 69])
    """
    return np.array([d_candidate_value[candidate] for candidate in CANDIDATES])


def one_over_t_plus_one(t):
    """Function `1 / (t + 1)`.

    When used as an update ratio (cf. :meth:`ProfileCardinal.fictitious_play`), this amounts to computing the arithmetic
    mean.

    Parameters
    ----------
    t : Number

    Returns
    -------
    Number

    Examples
    --------
        >>> one_over_t_plus_one(1)
        0.5
    """
    return 1 / (t + 1)


def one_over_sqrt_t_plus_one(t):
    """Function `1 / sqrt(t + 1)`.

    This function is provided as an example of update ratio for :meth:`ProfileCardinal.fictitious_play`. The constant
    1 in the denominator is the smallest integer such that `f(t = 1) < 1`.

    Parameters
    ----------
    t : Number

    Returns
    -------
    Number

    Examples
    --------
        >>> one_over_sqrt_t_plus_one(1)
        0.7071067811865475
    """
    return 1 / sqrt(t + 1)


def one_over_log_t_plus_two(t):
    """Function `1 / log(t + 2)`.

    This function is provided as an example of update ratio for :meth:`ProfileCardinal.fictitious_play`. The constant
    2 in the denominator is the smallest integer such that `f(t = 1) < 1`.

    Parameters
    ----------
    t : Number

    Returns
    -------
    Number

    Examples
    --------
        >>> one_over_log_t_plus_two(1)
        0.9102392266268373
    """
    return 1 / log(t + 2)


def one_over_log_log_t_plus_fifteen(t):
    """Function `1 / log(log(t + 15))`.

    This function is provided as an example of update ratio for :meth:`ProfileCardinal.fictitious_play`. The constant
    15 in the denominator is the smallest integer such that `f(t = 1) < 1`.

    Parameters
    ----------
    t : Number

    Returns
    -------
    Number

    Examples
    --------
        >>> one_over_log_log_t_plus_fifteen(1)
        0.9806022744169713
    """
    return 1 / log(log(t + 15))
