from app.sim.service import limit_branches


def test_branch_limiter_caps_at_six():
    branches = list(range(9))
    out = limit_branches(branches)
    assert len(out) == 6
    assert out == [0, 1, 2, 3, 4, 5]

