from poisson_approval import ExploreGridTaus


def test():
    """
        >>> exploration = ExploreGridTaus(denominator=[3, 4])
        >>> exploration
        <a: 1/3, bc: 2/3> ==> b, c
        <a: 1/3, ab: 1/3, bc: 1/3> ==> a, b
        <a: 1/3, ab: 1/3, ac: 1/3> ==> a
        <a: 1/3, ac: 1/3, b: 1/3> ==> a
        <a: 1/3, ab: 1/3, b: 1/3> ==> a, b
        <a: 1/3, b: 1/3, c: 1/3> ==> a, b, c
        <a: 2/3, bc: 1/3> ==> a
        <a: 2/3, ab: 1/3> ==> a
        <a: 2/3, b: 1/3> ==> a
        <a: 1> ==> a
        <a: 1/4, bc: 3/4> ==> b, c
        <a: 1/4, ab: 1/4, bc: 1/2> ==> b
        <a: 1/4, ab: 1/4, ac: 1/4, bc: 1/4> ==> a
        <a: 1/4, ac: 1/4, b: 1/4, bc: 1/4> ==> a, b, c
        <a: 1/4, ab: 1/4, ac: 1/4, b: 1/4> ==> a
        <a: 1/4, ab: 1/4, b: 1/4, c: 1/4> ==> a, b
        <a: 1/2, bc: 1/2> ==> a, b, c
        <a: 1/2, ab: 1/4, bc: 1/4> ==> a
        <a: 1/2, ab: 1/4, ac: 1/4> ==> a
        <a: 1/2, ab: 1/2> ==> a
        <a: 1/2, b: 1/4, bc: 1/4> ==> a, b
        <a: 1/2, ac: 1/4, b: 1/4> ==> a
        <a: 1/2, ab: 1/4, b: 1/4> ==> a
        <a: 1/2, b: 1/4, c: 1/4> ==> a
        <a: 1/2, b: 1/2> ==> a, b
        <a: 3/4, bc: 1/4> ==> a
        <a: 3/4, ab: 1/4> ==> a
        <a: 3/4, b: 1/4> ==> a
        <a: 1> ==> a
    """
    pass
