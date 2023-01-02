from dataclasses import dataclass, field
from typing import Optional

from feynml.id import Identifiable
from feynml.point import Point
from feynml.style import Labeled, Styled

from smpl_util.util import withify


@withify()
@dataclass
class Vertex(Labeled, Point, Styled, Identifiable):
    shape: Optional[str] = field(default=None, metadata={"type": "Attribute"})
    """Shape of the vertex"""
