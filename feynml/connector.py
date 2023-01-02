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
