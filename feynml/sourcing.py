from dataclasses import dataclass, field
from typing import Optional

from feynml.id import Identifiable
from feynml.pdgid import PDG


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})
    """Source of the object"""

    def __post_init__(self):
        if isinstance(self, PDG):
            PDG.__post_init__(self)
        elif isinstance(self, Identifiable):
            Identifiable.__post_init__(self)
        if isinstance(self.source, Identifiable):
            self.source = self.source.id

    def with_source(self, source):
        if isinstance(source, str):
            self.source = source
        else:
            self.source = source.id
        return self

    def goes_out_of(self, vertex):
        """Return True if the propagator goes out of the vertex, False otherwise."""
        return self.source == vertex.id
