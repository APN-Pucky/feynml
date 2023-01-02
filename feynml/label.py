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
from feynml.id import Identifiable
from feynml.point import Point
from feynml.style import Bending, Labeled, Styled, Texted
from feynml.targeting import Targeting


from smpl_doc.doc import deprecated
from smpl_util.util import withify


@withify()
@dataclass
class Label(Point, Texted, Identifiable):
    @deprecated(version="2.0.7.1", reason="Use a orphaned Vertex with Label.")
    def __init__(self, *args, **kwargs):
        pass