from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def s_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(pdgid=in1, sense="incoming", target=v1),
        Leg(pdgid=in2, sense="incoming", target=v1),
        Propagator(pdgid=prop).connect(v1, v2),
        Leg(pdgid=out1, sense="outgoing", target=v2),
        Leg(pdgid=out2, sense="outgoing", target=v2),
    )


def t_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(pdgid=in1, sense="incoming", target=v1),
        Leg(pdgid=in2, sense="incoming", target=v2),
        Propagator(pdgid=prop).connect(v1, v2),
        Leg(pdgid=out1, sense="outgoing", target=v1),
        Leg(pdgid=out2, sense="outgoing", target=v2),
    )


def u_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(pdgid=in1, sense="incoming", target=v1),
        Leg(pdgid=in2, sense="incoming", target=v2),
        Propagator(pdgid=prop).connect(v1, v2),
        Leg(pdgid=out1, sense="outgoing", target=v2),
        Leg(pdgid=out2, sense="outgoing", target=v1),
    )


def v_channel(in1=None, in2=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v := Vertex(),
        Leg(pdgid=in1, sense="incoming", target=v),
        Leg(pdgid=in2, sense="incoming", target=v),
        Leg(pdgid=out1, sense="outgoing", target=v),
        Leg(pdgid=out2, sense="outgoing", target=v),
    )
