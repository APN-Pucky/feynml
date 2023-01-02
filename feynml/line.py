from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union
from smpl_util.util import withify
from feynml.connector import Connector

from feynml.sourcing import Sourcing
from feynml.targeting import Targeting


@withify()
@dataclass
class Line(Targeting, Sourcing):
    def connect(self, source, target):
        return self.with_source(source).with_target(target)
