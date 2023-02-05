from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

from feynml.connector import Connector
from feynml.point import Point
from feynml.targeting import Targeting


@withify()
@dataclass
class Leg(Point, Targeting, Connector):
    sense: str = field(default=None, metadata={})
    """Sense of the leg, either 'incoming' or 'outgoing'"""

    external: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """External text for leg"""

    def is_incoming(self):
        """Return True if the leg is incoming, False otherwise."""
        return "in" == self.sense[:2] or self.sense[:8] == "anti-out"

    def is_outgoing(self):
        """Return True if the leg is outgoing, False otherwise."""
        return "out" == self.sense[:3] or self.sense[:7] == "anti-in"

    def with_incoming(self):
        self.sense = "incoming"
        return self

    def with_outgoing(self):
        self.sense = "outgoing"
        return self
