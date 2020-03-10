import numpy as np
from poisson_approval.utils.Util import iterator_simplex_grid


class IterableSimplexGrid:

    def __init__(self, cls, denominator, keys, d_key_fixed_share=None, test=None, **kwargs):
        # Default parameters
        if d_key_fixed_share is None:
            d_key_fixed_share = dict()
        # Parameters
        self.cls = cls
        self.denominator = denominator
        self.keys = keys
        self.d_key_fixed_share = d_key_fixed_share
        self.test = test
        self.kwargs = kwargs
        # Computed variables
        self.n_keys = len(keys)
        self.total_variable_share = 1 - sum(d_key_fixed_share.values())

    def __iter__(self):
        for x_simplex in iterator_simplex_grid(d=self.n_keys, denominator=self.denominator):
            x_simplex = np.array(x_simplex) * self.total_variable_share
            d_key_share = dict(zip(self.keys, x_simplex))
            for key, fixed_share in self.d_key_fixed_share.items():
                d_key_share[key] = d_key_share.get(key, 0) + fixed_share
            result = self.cls(d_key_share, **self.kwargs)
            if self.test is None or self.test(result):
                yield result
