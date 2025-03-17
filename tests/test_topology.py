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
        if fd.is_isomorphic(s):
            assert not has_s
            has_s = True
            break
        if fd.is_isomorphic(t):
            assert not has_t
            has_t = True
            break
        if fd.is_isomorphic(u):
            assert not has_u
            has_u = True
            break
        if fd.is_isomorphic(v):
            assert not has_v
            has_v = True
            break
        assert False
    assert has_s and has_t and has_u and has_v
