from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify


@withify()
@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
