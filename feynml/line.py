from dataclasses import dataclass

from smpl_util.util import withify

from feynml.id import Identifiable
from feynml.pdgid import PDG
from feynml.sourcing import Sourcing
from feynml.targeting import Targeting


@withify()
@dataclass
class Line(Targeting, Sourcing):
    def __post_init__(self):
        if isinstance(self, PDG):
            PDG.__post_init__(self)
        elif isinstance(self, Identifiable):
            Identifiable.__post_init__(self)
        Targeting.__post_init__(self)
        Sourcing.__post_init__(self)

    def connect(self, source, target):
        return self.with_source(source).with_target(target)
