from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

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
