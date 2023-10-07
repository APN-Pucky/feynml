from dataclasses import dataclass, field
from typing import Optional

from feynml.id import Identifiable


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})
    """Source of the object"""

    def __post_init__(self):
        if isinstance(self.source, Identifiable):
            self.source = self.source.id

    def with_source(self, source):
        if isinstance(source, str):
            self.source = source
        else:
            self.source = source.id
        return self
