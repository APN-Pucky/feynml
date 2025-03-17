from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.pdgid import pdgid_param
from feynml.vertex import Vertex


def fusion(in1=None, in2=None, out1=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(in2), sense="incoming", target=v1),
        Leg(**pdgid_param(out1), sense="outgoing", target=v1),
    )


def decay(in1=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(out1), sense="outgoing", target=v1),
        Leg(**pdgid_param(out2), sense="outgoing", target=v1),
    )
