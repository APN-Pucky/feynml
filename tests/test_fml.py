from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML, Head, Meta
from feynml.leg import Leg
from feynml.momentum import Momentum
from feynml.propagator import Propagator
from feynml.vertex import Vertex

# Load an FML file and check that it is the same as the original
# FeynmanDiagram object


def test_fml_print():
    fd = FeynmanDiagram()
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    p1 = Propagator("p1")
    l1 = Leg("l1")
    p1.with_source(v1).with_momentum(Momentum("p1", 1, 2, 3, 4))
    p1.with_target(v2)
    fd.propagators.append(p1)
    fd.vertices.append(v1)
    fd.vertices.append(v2)
    fd.legs.append(l1)

    fml = FeynML(
        head=Head(
            metas=[Meta(name="pyfeyn2", content="test")],
        ),
        diagrams=[fd],
    )
    print(fml.to_xml())


def test_fml_load():
    fml = FeynML.from_xml_file("tests/test.fml")
    print(fml)


def test_fml_css():
    fml = FeynML.from_xml_file("tests/test.fml")
    for le in fml.diagrams[0].legs:
        if le.id == "E1":
            if le.style is None:
                continue
            le.style.opacity = "0.5"
            le.style.width = "40%"

    assert (
        fml.get_style_property(
            fml.diagrams[0].get(lambda a: a.type == "fermion")[0], "color"
        )
        == "green"
    )


def test_fml_css_online():
    fml = FeynML.from_xml_file("tests/test.fml")
    fml.head.links[
        0
    ].href = "https://raw.githubusercontent.com/APN-Pucky/feynml/master/tests/test_styles.css"
    for le in fml.diagrams[0].legs:
        if le.id == "E1":
            if le.style is None:
                continue
            le.style.opacity = "0.5"
            le.style.width = "40%"

    assert (
        fml.get_style_property(
            fml.diagrams[0].get(lambda a: a.type == "fermion")[0], "color"
        )
        == "green"
    )


test_fml_print()
# test_fml_load()
# test_fml_plot()
# test_fml_css()
