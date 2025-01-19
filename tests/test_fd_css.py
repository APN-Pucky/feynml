from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def get_test_fd():
    v1 = Vertex("v1").with_xy(-1, 0).with_shape("blob")
    v2 = Vertex("v2").with_xy(1, 0).with_style("symbol : dot")
    fd = FeynmanDiagram().add(
        v1,
        v2,
        Propagator(name="g").connect(v1, v2),
        Leg(name="g").with_target(v1).with_xy(-2, 1).with_incoming(),
        Leg(name="g")
        .with_target(v1)
        .with_xy(-2, -1)
        .with_incoming()
        .with_class("notred"),
        Leg(name="g").with_target(v2).with_xy(2, 1).with_outgoing().with_class("red"),
        Leg("myid1", name="g")
        .with_target(v2)
        .with_xy(2, -1)
        .with_outgoing()
        .with_style_property("bend-direction", "right"),
    )
    return fd


def test_css_direct():
    fd = get_test_fd()
    le = fd.get_leg("myid1").with_style_property("color", "green")
    assert fd.get_style_property(le, "color") == "green"


def test_css_global_rule():
    fd = get_test_fd()
    fd.with_rule(" * { color: red } ")
    le = fd.get_leg("myid1")
    assert fd.get_style_property(le, "color") == "red"


def test_css_id():
    fd = get_test_fd()
    le = fd.get_leg("myid1")
    fd.add_rule("#myid1 { color: blue }")
    assert fd.get_style_property(le, "color") == "blue"


def test_css_pdgid():
    fd = get_test_fd()
    le = fd.get_leg("myid1")
    fd.add_rule('[pdgid="21"] { color: gray }')
    assert fd.get_style_property(le, "color") == "gray"


def test_css_type():
    fd = get_test_fd()
    le = fd.get_leg("myid1")
    fd.add_rule('[type="gluon"] { color: gray }')
    assert fd.get_style_property(le, "color") == "gray"


def test_css_class():
    fd = get_test_fd()
    le = fd.get_leg("myid1").with_class("notred")
    fd.add_rule(".notred { color: blue }")
    assert fd.get_style_property(le, "color") == "blue"


def test_css_obj():
    fd = get_test_fd()
    le = fd.get_leg("myid1")
    fd.add_rule("leg { color: black }")
    assert fd.get_style_property(le, "color") == "black"

    p = fd.propagators[0]
    fd.add_rule("propagator { color: green }")
    assert fd.get_style_property(p, "color") == "green"

    v = fd.vertices[0]
    fd.add_rule("vertex { color: yellow }")
    assert fd.get_style_property(v, "color") == "yellow"
