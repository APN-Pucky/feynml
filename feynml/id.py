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


# from pyfeyn2.propagator import Propagator
# from pyfeyn2.vertex import Vertex

# Global counter for unique ids
global_id = 0


@withify()
@dataclass
class Identifiable:
    id: Optional[str] = field(
        default=None, metadata={"name": "id", "namespace": "", "type": "Attribute"}
    )
    # id2: Optional[str] = field(default=None, metadata={"name": "id2", "namespace": ""})

    def __post_init__(self):
        global global_id
        if self.id is None:
            # use some global counter to generate unique id
            self.id = self.__class__.__name__ + str(global_id)
            global_id = global_id + 1
