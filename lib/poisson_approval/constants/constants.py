RANKINGS = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
PERMUTATIONS = RANKINGS
TWELVE_TYPES = ['a_bc', 'ab_c', 'a_cb', 'ac_b', 'b_ac', 'ba_c', 'b_ca', 'bc_a', 'c_ab', 'ca_b', 'c_ba', 'cb_a']

WEAK_ORDERS_LOVE_WITHOUT_INVERSIONS = ['a>b~c', 'b>a~c', 'c>a~b']
WEAK_ORDERS_HATE_WITHOUT_INVERSIONS = ['a~b>c', 'a~c>b', 'b~c>a']
WEAK_ORDERS_WITHOUT_INVERSIONS = WEAK_ORDERS_LOVE_WITHOUT_INVERSIONS + WEAK_ORDERS_HATE_WITHOUT_INVERSIONS

CANDIDATES = ['a', 'b', 'c']
PAIRS_WITHOUT_INVERSIONS = ['ab', 'ac', 'bc']
PAIRS_INVERTED = ['ba', 'ca', 'cb']
PAIRS_WITH_INVERSIONS = PAIRS_WITHOUT_INVERSIONS + PAIRS_INVERTED
BALLOTS_WITHOUT_INVERSIONS = CANDIDATES + PAIRS_WITHOUT_INVERSIONS
BALLOTS_WITH_INVERSIONS = BALLOTS_WITHOUT_INVERSIONS + PAIRS_INVERTED
BALLOTS_WITHOUT_INVERSIONS_SORTED_ALPHABETICAL = sorted(BALLOTS_WITHOUT_INVERSIONS)

UTILITY_DEPENDENT = 'utility-dependent'
INCONCLUSIVE = 'inconclusive'

APPROVAL = 'Approval'
PLURALITY = 'Plurality'
ANTI_PLURALITY = 'Anti-plurality'


def _f_abc_xyz(my_list):
    return [element.replace('a', 'x').replace('b', 'y').replace('c', 'z') for element in my_list]


XYZ_RANKINGS = _f_abc_xyz(RANKINGS)
XYZ_PERMUTATIONS = XYZ_RANKINGS
XYZ_TWELVE_TYPES = _f_abc_xyz(TWELVE_TYPES)
XYZ_BALLOTS_WITHOUT_INVERSION = _f_abc_xyz(BALLOTS_WITHOUT_INVERSIONS)
XYZ_BALLOTS_INVERTED = _f_abc_xyz(PAIRS_INVERTED)
XYZ_BALLOTS_WITH_INVERSIONS = _f_abc_xyz(BALLOTS_WITH_INVERSIONS)
XYZ_WEAK_ORDERS_WITHOUT_INVERSIONS = _f_abc_xyz(WEAK_ORDERS_WITHOUT_INVERSIONS)


NORMALIZATION_WARNING = ("Warning: the input is not normalized, I will normalize it. If you use floats, consider using "
                         "fractions. To disable this warning, use the parameter normalization_warning=False.")
