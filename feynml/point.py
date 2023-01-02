from dataclasses import dataclass, field
from typing import Optional


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
