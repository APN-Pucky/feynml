from dataclasses import dataclass, field
from typing import Optional

from smpl_util.util import withify

# Global counter for unique ids
global_id = 0


def generate_new_id():
    global global_id
    global_id = global_id + 1
    return global_id


@withify()
@dataclass
class Identifiable:
    id: Optional[str] = field(
        default=None, metadata={"name": "id", "namespace": "", "type": "Attribute"}
    )
    # id2: Optional[str] = field(default=None, metadata={"name": "id2", "namespace": ""})

    def __post_init__(self):
        if self.id is None:
            # use some global counter to generate unique id
            self.with_new_id()

    def with_id(self, id: str):
        """set id"""
        self.id = id
        return self

    def with_new_id(self):
        """generate new id"""
        id = generate_new_id()
        self.id = self.__class__.__name__ + str(id)
        return self

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __hash__(self):
        return hash(self.id)
