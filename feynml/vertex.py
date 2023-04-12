from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

from feynml.id import Identifiable
from feynml.labeled import Labeled
from feynml.point import Point
from feynml.styled import Styled


@withify()
@dataclass
class Vertex(Labeled, Point, Styled, Identifiable):
    shape: Optional[str] = field(default=None, metadata={"type": "Attribute"})
    """Shape of the vertex"""
