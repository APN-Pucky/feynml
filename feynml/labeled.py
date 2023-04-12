import logging
from dataclasses import dataclass, field
from typing import Optional

import cssutils
from smpl_doc.doc import deprecated
from smpl_util.util import withify
from xsdata.formats.converter import Converter, converter


@withify()
@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
