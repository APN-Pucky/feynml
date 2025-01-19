from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def get_test_fml():
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
    return fd, FeynML(diagrams=[fd])


def test_css_direct():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1").with_style_property("color", "green")
    assert fml.get_style_property(le, "color") == "green"


def test_css_global_rule():
    fd, fml = get_test_fml()
    fml.with_rule(" * { color: red } ")
    le = fd.get_leg("myid1")
    assert fml.get_style_property(le, "color") == "red"
    assert fd.get_style_property(le, "color") == "red"

    fd.with_rule(" * { color: green } ")
    assert fml.get_style_property(le, "color") == "green"
    assert fd.get_style_property(le, "color") == "green"


def test_css_id():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1")
    fml.add_rule("#myid1 { color: blue }")
    assert fml.get_style_property(le, "color") == "blue"
    assert fd.get_style_property(le, "color") == "blue"
    fd.add_rule("#myid1 { color: gray }")
    assert fml.get_style_property(le, "color") == "gray"
    assert fd.get_style_property(le, "color") == "gray"


def test_css_pdgid():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1")
    fml.add_rule('[pdgid="21"] { color: gray }')
    assert fml.get_style_property(le, "color") == "gray"
    assert fd.get_style_property(le, "color") == "gray"
    fd.add_rule('[pdgid="21"] { color: black }')
    assert fml.get_style_property(le, "color") == "black"
    assert fd.get_style_property(le, "color") == "black"


def test_css_type():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1")
    fml.add_rule('[type="gluon"] { color: gray }')
    assert fml.get_style_property(le, "color") == "gray"
    assert fd.get_style_property(le, "color") == "gray"
    fd.add_rule('[type="gluon"] { color: blue }')
    assert fml.get_style_property(le, "color") == "blue"
    assert fd.get_style_property(le, "color") == "blue"


def test_css_class():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1").with_class("notred")
    fml.add_rule(".notred { color: blue }")
    assert fml.get_style_property(le, "color") == "blue"
    assert fd.get_style_property(le, "color") == "blue"
    fd.add_rule(".notred { color: red }")
    assert fml.get_style_property(le, "color") == "red"
    assert fd.get_style_property(le, "color") == "red"


def test_css_obj():
    fd, fml = get_test_fml()
    le = fd.get_leg("myid1")
    fml.add_rule("leg { color: black }")
    assert fml.get_style_property(le, "color") == "black"
    assert fd.get_style_property(le, "color") == "black"

    p = fd.propagators[0]
    fml.add_rule("propagator { color: green }")
    assert fml.get_style_property(p, "color") == "green"
    assert fd.get_style_property(p, "color") == "green"

    v = fd.vertices[0]
    fml.add_rule("vertex { color: yellow }")
    assert fml.get_style_property(v, "color") == "yellow"
    assert fd.get_style_property(v, "color") == "yellow"
    fd.add_rule("vertex { color: blue }")
    assert fml.get_style_property(v, "color") == "blue"
    assert fd.get_style_property(v, "color") == "blue"
