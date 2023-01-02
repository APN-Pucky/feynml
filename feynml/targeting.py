from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union
from smpl_doc.doc import deprecated

# We don't want to see the cssutils warnings, since we have custom properties


@dataclass
class Targeting:
    target: Optional[str] = field(default="", metadata={})
    """Target of the object"""

    def with_target(self, target):
        if isinstance(target, str):
            self.target = target
        else:
            self.target = target.id
        return self

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_target(self, *args, **kwargs):
        return self.with_target(*args, **kwargs)
