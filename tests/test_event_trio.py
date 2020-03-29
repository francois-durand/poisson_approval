from poisson_approval import TauVector, EventTrio


def test():
    tau = TauVector({
        'a': 0.9999999868921308,
        'ab': 7.182846803148341e-09,
        'ac': 1.85196073297195e-09,
        'b': 2.990584787561229e-09,
        'bc': 1.082477022800632e-09,
        'c': 0
    })
    assert tau.trio.phi_a <= 1
    assert tau.trio.phi_b <= 1
    assert tau.trio.phi_c >= 1
