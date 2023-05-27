import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional

from feynml.styled import CSSSheet


@dataclass
class Link:
    class Meta:
        name = "link"

    rel: Optional[str] = field(default="", metadata={"type": "Attribute"})
    href: Optional[str] = field(default="", metadata={"type": "Attribute"})
