from feynml.feynmandiagram import FeynmanDiagram
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def test_split_gamma():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), p1 := Propagator(pdgid=11).connect(v1, v2)
    )
    fd.split(p1, 22, sense="outgoing")
    print(fd.to_matrix())
    assert len(fd.vertices) == 3
    assert len(fd.legs) == 1
    assert len(fd.propagators) == 2
    # assert fd == 0
    # [[ 0.  0.  0.  0.  0.]
    # [ 0.  0.  0. 11.  0.]
    # [ 0.  0.  0.  0.  0.]
    # [ 0.  0. 11.  0. 22.]
    # [ 0.  0.  0.  0.  0.]]


# TODO more test cases here: Leg split
# TODO visualize matrices to be safe (store ascii here too)


def test_split_gluon():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), p1 := Propagator(pdgid=1).connect(v1, v2)
    )
    fd.split(p1, 1, 1, 21, sense="incoming")

    print(fd.to_matrix())
    assert len(fd.vertices) == 3
    assert len(fd.legs) == 1
    assert len(fd.propagators) == 2
    # [[ 0.  0.  0.  1.  0.]
    # [ 0.  0.  0.  1.  0.]
    # [ 0.  0.  0.  0.  0.]
    # [ 0.  0. 21.  0.  0.]
    # [ 0.  0.  0.  0.  0.]]
