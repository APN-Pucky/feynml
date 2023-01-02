from dataclasses import dataclass, field
from typing import Optional

from feynml.momentum import Momentum
from feynml.pdgid import PDG
from feynml.style import Labeled, Styled


from smpl_util.util import withify


@withify()
@dataclass
class Connector(Labeled, Styled, PDG):
    momentum: Optional[Momentum] = field(
        default=None, metadata={"name": "momentum", "type": "Element"}
    )
    """Momentum of the connector"""

    def with_tension(self, tension: float):
        """Add tension to the connector"""
        return self.put_styles(tension=tension)

    def get_tension(self):
        """Get tension of the connector"""
        return self.get_style("tension")

    def with_length(self, length: float):
        """Add length to the connector"""
        return self.put_styles(length=length)

    def get_length(self):
        """Get length of the connector"""
        return self.get_style("length")
