from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Meta:
    class Meta:
        name = "meta"

    name: Optional[str] = field(default="", metadata={"type": "Attribute"})
    content: Optional[str] = field(default="", metadata={"type": "Attribute"})
