from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})
    """Target of the object"""

    def with_target(self, target):
        if isinstance(target, str):
            self.target = target
        else:
            self.target = target.id
        return self
