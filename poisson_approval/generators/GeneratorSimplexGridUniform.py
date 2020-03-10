from poisson_approval.utils.Util import rand_simplex_grid


class GeneratorSimplexGridUniform:

    def __init__(self, cls, denominator, keys, d_key_fixed_share=None, **kwargs):
        # Default values
        if d_key_fixed_share is None:
            d_key_fixed_share = dict()
        # Parameters
        self.cls = cls
        self.keys = keys
        self.denominator = denominator
        self.d_key_fixed_share = d_key_fixed_share
        self.kwargs = kwargs
        # Computed variables
        self.n_keys = len(self.keys)
        self.total_variable_share = 1 - sum(self.d_key_fixed_share.values())

    def __call__(self):
        x_simplex = rand_simplex_grid(d=self.n_keys, denominator=self.denominator) * self.total_variable_share
        d_key_share = dict(zip(self.keys, x_simplex))
        for key, fixed_share in self.d_key_fixed_share.items():
            d_key_share[key] = d_key_share.get(key, 0) + fixed_share
        return self.cls(d_key_share, **self.kwargs)
