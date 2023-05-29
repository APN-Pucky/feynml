import re
from dataclasses import dataclass

from feynml.interface.formcalc.field import Field
from feynml.interface.formcalc.vertex import Vertex


@dataclass
class Propagator:
    type: str
    v1: Vertex
    v2: Vertex
    f: Field

    def __str__(self):
        return f"Propagator[{self.type}][{self.v1}, {self.v2}, {self.f}]"

    @classmethod
    def re(cls):
        return (
            r"\s*Propagator\[(Incoming|Outgoing|Internal)\]\[("
            + Vertex.re()
            + r"),("
            + Vertex.re()
            + r"),("
            + Field.re()
            + r")\]\s*"
        )

    @classmethod
    def n(cls):
        return 1 + 1 + Vertex.n() + 1 + Vertex.n() + 1 + Field.n()

    @classmethod
    def from_str(cls, propagator: str):
        """
        Example

        >>> str(Propagator.from_str("Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]]"))
        'Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]]'
        """
        res = re.search(cls.re(), propagator)
        return Propagator(
            res.group(1),
            Vertex.from_str(res.group(2)),
            Vertex.from_str(res.group(3 + Vertex.n())),
            Field.from_str(res.group(6 + Vertex.n())),
        )
