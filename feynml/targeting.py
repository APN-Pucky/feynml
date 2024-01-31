from dataclasses import dataclass, field
from typing import Optional

from feynml.id import Identifiable
from feynml.pdgid import PDG


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})
    """Target of the object"""

    def __post_init__(self):
        if isinstance(self, PDG):
            PDG.__post_init__(self)
        elif isinstance(self, Identifiable):
            Identifiable.__post_init__(self)
        if isinstance(self.target, Identifiable):
            self.target = self.target.id

    def with_target(self, target):
        if isinstance(target, str):
            self.target = target
        else:
            self.target = target.id
        return self

    def goes_into(self, vertex):
        """Return True if the propagator goes into the vertex, False otherwise."""
        return self.target == vertex.id
