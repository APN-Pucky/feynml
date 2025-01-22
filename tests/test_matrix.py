from feynml.feynmandiagram import FeynmanDiagram
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def test_split_gamma():
    fd = FeynmanDiagram().add(
        v1 := Vertex(), v2 := Vertex(), Propagator(pdgid=11).connect(v1, v2)
    )
    print(fd.to_matrix())
    # TODO how do I test that this matrix is
    # [[ 0.  0.  0.  0.]
    #  [ 0.  0. 11.  0.]
    #  [ 0.  0.  0.  0.]
    #  [ 0.  0.  0.  0.]]
