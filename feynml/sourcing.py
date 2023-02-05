from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sourcing:
    source: Optional[str] = field(default="", metadata={})
    """Source of the object"""

    def with_source(self, source):
        if isinstance(source, str):
            self.source = source
        else:
            self.source = source.id
        return self
