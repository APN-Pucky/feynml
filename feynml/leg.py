from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

from feynml.connector import Connector
from feynml.point import Point
from feynml.targeting import Targeting


@withify()
@dataclass
class Leg(Point, Targeting, Connector):
    shape: Optional[str] = field(default=None, metadata={"type": "Attribute"})
    """Shape of the leg end"""
    sense: str = field(
        default=None, metadata={}
    )  # TODO why is this a string and not a bool?!?
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
        """Set the leg to be incoming."""
        self.sense = "incoming"
        return self

    def goes_into(self, vertex):
        """Return True if the leg goes into the vertex, False otherwise."""
        return self.target == vertex.id and self.is_incoming()

    def goes_out_of(self, vertex):
        """Return True if the leg goes out of the vertex, False otherwise."""
        return self.target == vertex.id and self.is_outgoing()

    incoming = with_incoming

    def with_outgoing(self):
        """Set the leg to be outgoing."""
        self.sense = "outgoing"
        return self

    outgoing = with_outgoing

    def conjugate(self):
        """Set incoming to outgoing and vice versa."""
        if self.is_incoming():
            return self.with_outgoing()
        elif self.is_outgoing():
            return self.with_incoming()
