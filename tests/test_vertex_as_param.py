from feynml import Leg, Propagator, Vertex


def test_vertex_as_param():
    v1 = Vertex()
    v2 = Vertex()
    p = Propagator(pdgid=2, target=v2, source=v1)
    le = Leg(pdgid=-1, target=v1)

    assert p.target == v2.id
    assert p.source == v1.id
    assert le.target == v1.id
    # assert p.goes_into(v2)
    # assert p.goes_out_of(v1)
    # assert l.goes_into(v1)
