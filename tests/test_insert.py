from feynml.interface.qgraf import generate_fml as qgraf_generate_fml
from feynml.topology import generate_fml
from feynmodel.interface.ufo import load_ufo_model


def test_own_vs_qgraf_tt():
    fm = load_ufo_model("ufo_sm")
    own_fml = generate_fml(fm, incoming_pdgs=[21, 21], outgoing_pdgs=[6, -6])
    qgraf_fml = qgraf_generate_fml(fm, incoming_pdgs=[21, 21], outgoing_pdgs=[6, -6])
    assert own_fml.is_isomorphic(qgraf_fml)
