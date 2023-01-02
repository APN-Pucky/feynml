# TODO think about withify for sub-classes
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Momentum:
    class Meta:
        name = "momentum"

    name: Optional[str] = field(default=None, metadata={"type": "Element"})
    px: Optional[float] = field(default=None, metadata={"type": "Element"})
    py: Optional[float] = field(default=None, metadata={"type": "Element"})
    pz: Optional[float] = field(default=None, metadata={"type": "Element"})
    e: Optional[float] = field(default=None, metadata={"type": "Element"})
