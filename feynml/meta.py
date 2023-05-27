import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional

from feynml.styled import CSSSheet


@dataclass
class Meta:
    class Meta:
        name = "meta"

    name: Optional[str] = field(default="", metadata={"type": "Attribute"})
    content: Optional[str] = field(default="", metadata={"type": "Attribute"})
