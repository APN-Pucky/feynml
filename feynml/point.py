import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from feynml.style import Bending, Labeled, Styled, Texted

from smpl_doc.doc import deprecated
from smpl_util.util import withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


@dataclass
class Point:
    x: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """x coordinate"""
    y: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """y coordinate"""
    z: Optional[float] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """z coordinate"""

    def with_point(self, p):
        self.x = float(p.x)
        self.y = float(p.y)
        return self

    def with_xy(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def with_xyz(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        return self
