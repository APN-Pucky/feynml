from dataclasses import dataclass

from smpl_util.util import withify

from feynml.connector import Connector
from feynml.line import Line


@withify()
@dataclass
class Propagator(Line, Connector):
    pass
