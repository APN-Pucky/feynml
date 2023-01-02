import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from feynml.connector import Connector
from feynml.point import Point
from feynml.style import Bending, Labeled, Styled, Texted
from feynml.targeting import Targeting


from smpl_doc.doc import deprecated
from smpl_util.util import withify


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

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_external(self, *args, **kwargs):
        return self.with_external(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_incoming(self, *args, **kwargs):
        return self.with_incoming(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_outgoing(self, *args, **kwargs):
        return self.with_outgoing(*args, **kwargs)
