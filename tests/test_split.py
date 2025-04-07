from feynml.feynmandiagram import FeynmanDiagram
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def test_emission_gamma():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), p1 := Propagator(pdgid=11).connect(v1, v2)
    )
    fd.emission(p1, 22, sense="outgoing")
    print(fd.to_matrix().tolist())
    assert len(fd.vertices) == 3
    assert len(fd.legs) == 1
    assert len(fd.propagators) == 2

    assert fd.to_matrix().tolist() == [
        [[], [], [11], []],
        [[], [], [], []],
        [[], [11], [], [22]],
        [[], [], [], []],
    ]


# TODO more test cases here: Leg split
# TODO visualize matrices to be safe (store ascii here too)


def test_emission_gluon():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), p1 := Propagator(pdgid=1).connect(v1, v2)
    )
    fd.emission(p1, 1, 1, 21, sense="incoming")

    fd.to_matrix()
    assert len(fd.vertices) == 3
    assert len(fd.legs) == 1
    assert len(fd.propagators) == 2

    assert fd.to_matrix().tolist() == [
        [[], [], [], [1]],
        [[], [], [], [1]],
        [[], [], [], []],
        [[], [], [21], []],
    ]


# TODO continue here!
