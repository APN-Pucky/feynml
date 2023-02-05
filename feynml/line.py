from dataclasses import dataclass

from smpl_util.util import withify

from feynml.sourcing import Sourcing
from feynml.targeting import Targeting


@withify()
@dataclass
class Line(Targeting, Sourcing):
    def connect(self, source, target):
        return self.with_source(source).with_target(target)
