from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.pdgid import pdgid_param
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def fusion(in1=None, in2=None, in3=None, out1=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(in2), sense="incoming", target=v1),
        Leg(**pdgid_param(in3), sense="incoming", target=v1),
        Leg(**pdgid_param(out1), sense="outgoing", target=v1),
    )


def decay(in1=None, out1=None, out2=None, out3=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(out1), sense="outgoing", target=v1),
        Leg(**pdgid_param(out2), sense="outgoing", target=v1),
        Leg(**pdgid_param(out3), sense="outgoing", target=v1),
    )


def s_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(in2), sense="incoming", target=v1),
        Propagator(**pdgid_param(prop)).connect(v1, v2),
        Leg(**pdgid_param(out1), sense="outgoing", target=v2),
        Leg(**pdgid_param(out2), sense="outgoing", target=v2),
    )


def t_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(in2), sense="incoming", target=v2),
        Propagator(**pdgid_param(prop)).connect(v1, v2),
        Leg(**pdgid_param(out1), sense="outgoing", target=v1),
        Leg(**pdgid_param(out2), sense="outgoing", target=v2),
    )


def u_channel(in1=None, in2=None, prop=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v1 := Vertex(),
        v2 := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v1),
        Leg(**pdgid_param(in2), sense="incoming", target=v2),
        Propagator(**pdgid_param(prop)).connect(v1, v2),
        Leg(**pdgid_param(out1), sense="outgoing", target=v2),
        Leg(**pdgid_param(out2), sense="outgoing", target=v1),
    )


def v_channel(in1=None, in2=None, out1=None, out2=None):
    return FeynmanDiagram().add(
        v := Vertex(),
        Leg(**pdgid_param(in1), sense="incoming", target=v),
        Leg(**pdgid_param(in2), sense="incoming", target=v),
        Leg(**pdgid_param(out1), sense="outgoing", target=v),
        Leg(**pdgid_param(out2), sense="outgoing", target=v),
    )
