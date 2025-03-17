from feynml.topology import generate_topologies
from feynml.topology import four


def test_topology_two():
    fml = generate_topologies(2, 2)
    s = four.s_channel()
    t = four.t_channel()
    u = four.u_channel()
    v = four.v_channel()

    has_s, has_t, has_u, has_v = False, False, False, False
    for fd in fml.diagrams:
        hit = False
        if fd.is_isomorphic(s):
            assert not has_s
            assert not hit
            has_s = True
            hit = True
        if fd.is_isomorphic(t):
            assert not has_t
            assert not hit
            has_t = True
            hit = True
        if fd.is_isomorphic(u):
            assert not has_u
            assert not hit
            has_u = True
            hit = True
        if fd.is_isomorphic(v):
            assert not has_v
            assert not hit
            has_v = True
            hit = True
        assert hit
    assert has_s
    assert has_t
    assert has_u
    assert has_v
