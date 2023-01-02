from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union
from smpl_util.util import withify
from feynml.connector import Connector
from feynml.line import Line

from feynml.sourcing import Sourcing
from feynml.targeting import Targeting


@withify()
@dataclass
class Propagator(Line, Connector):
    pass
