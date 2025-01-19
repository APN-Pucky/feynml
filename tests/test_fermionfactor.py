import logging

from feynmodel.interface.qgraf import feynmodel_to_qgraf
from feynmodel.interface.ufo import load_ufo_model
from pyqgraf import qgraf
from xsdata.formats.dataclass.parsers import XmlParser

from feynml.feynml import FeynML
from feynml.interface.qgraf import style

logger = logging.getLogger("feynml")
logger.setLevel(logging.DEBUG)


def test_fermion_factor():
    fm = load_ufo_model("ufo_sm")
    qfm = feynmodel_to_qgraf(fm, True, False)
    qgraf.install()
    xml_string = qgraf.run(
        "g[p1], g[p2]",
        "u[p3], u_bar[p4]",
        loops=0,
        loop_momentum="l",
        model=qfm,
        style=style,
    )
    # print(xml_string)
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)
    fds = fml.diagrams
    assert fds[0].get_fermion_factor(fds[0]) == 1
    assert fds[1].get_fermion_factor(fds[1]) == 1
    assert fds[2].get_fermion_factor(fds[2]) == 1
    # TODO what's up here?:
    # assert fds[1].get_fermion_factor(fds[2]) == -1
    # assert fds[0].get_fermion_factor(fds[1]) == -fds[0].get_fermion_factor(fds[2])
