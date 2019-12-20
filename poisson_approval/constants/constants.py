RANKINGS = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
PERMUTATIONS = RANKINGS
TWELVE_TYPES = ['a_bc', 'ab_c', 'a_cb', 'ac_b', 'b_ac', 'ba_c', 'b_ca', 'bc_a', 'c_ab', 'ca_b', 'c_ba', 'cb_a']

CANDIDATES = ['a', 'b', 'c']
PAIRS_WITHOUT_INVERSIONS = ['ab', 'ac', 'bc']
PAIRS_INVERTED = ['ba', 'ca', 'cb']
PAIRS_WITH_INVERSIONS = PAIRS_WITHOUT_INVERSIONS + PAIRS_INVERTED
BALLOTS_WITHOUT_INVERSIONS = CANDIDATES + PAIRS_WITHOUT_INVERSIONS
BALLOTS_WITH_INVERSIONS = BALLOTS_WITHOUT_INVERSIONS + PAIRS_INVERTED

UTILITY_DEPENDENT = 'utility-dependent'
INCONCLUSIVE = 'inconclusive'


def _f_abc_xyz(my_list):
    return [element.replace('a', 'x').replace('b', 'y').replace('c', 'z') for element in my_list]


XYZ_RANKINGS = _f_abc_xyz(RANKINGS)
XYZ_PERMUTATIONS = XYZ_RANKINGS
XYZ_TWELVE_TYPES = _f_abc_xyz(TWELVE_TYPES)
XYZ_BALLOTS_WITHOUT_INVERSION = _f_abc_xyz(BALLOTS_WITHOUT_INVERSIONS)
XYZ_BALLOTS_INVERTED = _f_abc_xyz(PAIRS_INVERTED)
XYZ_BALLOTS_WITH_INVERSIONS = _f_abc_xyz(BALLOTS_WITH_INVERSIONS)
