from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Link:
    class Meta:
        name = "link"

    rel: Optional[str] = field(default="", metadata={"type": "Attribute"})
    href: Optional[str] = field(default="", metadata={"type": "Attribute"})
