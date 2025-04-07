from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def test_matrix():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), Propagator(pdgid=11).connect(v1, v2)
    )
    print(fd.to_matrix())

    assert fd.to_matrix().tolist() == [
        [[], [11]],
        [[], []],
    ]


def test_matrix_idempotency():
    fd = FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Propagator(pdgid=11).connect(v1, v2),
        Leg(pdgid=11, sense="outgoing", target=v1),
        Leg(pdgid=2, sense="incoming", target=v2),
    )
    mat = fd.to_matrix()
    nfd = FeynmanDiagram.from_matrix(mat, li=1, lo=1)
    assert nfd.to_matrix().tolist() == fd.to_matrix().tolist()


# TODO visualize matrices to be safe (store ascii here too)
