import pytest
from feynml import FeynML, FeynmanDiagram, Leg, Propagator, Vertex


@pytest.mark.parametrize("clazz", [FeynML, FeynmanDiagram])
def test_sheet_with_rule(clazz):
    fml = clazz().with_rule("""
    * {
        momentum-arrow: true;
    }
    """)
    assert "momentum-arrow" in str(fml.get_sheets()[-1].cssText)
    # assert fml.get_style_property("momentum-arrow","test") == "true"


@pytest.mark.parametrize("clazz", [Leg, Vertex, Propagator])
def test_styled_with_style(clazz):
    fml = clazz().with_style("momentum-arrow: true")
    assert fml.get_style_property("momentum-arrow") == "true"
