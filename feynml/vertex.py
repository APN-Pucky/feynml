from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

from feynml.id import Identifiable
from feynml.point import Point
from feynml.style import Bending, Labeled, Styled, Texted

from smpl_util.util import withify


@withify()
@dataclass
class Vertex(Labeled, Point, Styled, Identifiable):
    shape: Optional[str] = field(default=None, metadata={"type": "Attribute"})
    """Shape of the vertex"""
