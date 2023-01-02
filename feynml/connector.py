import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from feynml.momentum import Momentum
from feynml.pdgid import PDG
from feynml.style import Bending, Labeled, Styled, Texted


from smpl_doc.doc import deprecated
from smpl_util.util import withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


@withify()
@dataclass
class Connector(Labeled, Bending, Styled, PDG):
    momentum: Optional[Momentum] = field(
        default=None, metadata={"name": "momentum", "type": "Element"}
    )
    """Momentum of the connector"""
