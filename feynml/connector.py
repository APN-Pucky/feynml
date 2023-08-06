from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

from feynml.labeled import Labeled
from feynml.momentum import Momentum
from feynml.pdgid import PDG
from feynml.styled import Styled


@withify()
@dataclass
class Connector(Labeled, Styled, PDG):
    momentum: Optional[Momentum] = field(
        default=None, metadata={"name": "momentum", "type": "Element"}
    )
    """Momentum of the connector"""

    def goes_into(self, vertex):
        raise NotImplementedError

    def goes_out_of(self, vertex):
        raise NotImplementedError

    def with_tension(self, tension: float):
        """Add tension to the connector"""
        return self.with_style_properties(tension=tension)

    def get_tension(self):
        """Get tension of the connector"""
        return self.get_style_property("tension")

    def with_length(self, length: float):
        """Add length to the connector"""
        return self.with_style_properties(length=length)

    def get_length(self):
        """Get length of the connector"""
        return self.get_style_property("length")
