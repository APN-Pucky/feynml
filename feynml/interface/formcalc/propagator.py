import re
from dataclasses import dataclass

from feynml.interface.formcalc.field import Field
from feynml.interface.formcalc.vertex import Vertex


@dataclass
class Propagator:
    v1: Vertex
    v2: Vertex
    f: Field

    def __str__(self):
        """
        Example

        >>> Propagator.from_str(str(Propagator(Vertex(1,1),Vertex(3,5),Field(1)))) == Propagator(Vertex(1,1),Vertex(3,5),Field(1))
        True
        """
        return f"Propagator[Internal][{self.v1},{self.v2},{self.f}]"

    @classmethod
    def re():
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
    def n():
        return 1 + 1 + Vertex.n() + 1 + Vertex.n() + 1 + Field.n()

    @classmethod
    def from_str(cls, propagator: str):
        """
        Example

        >>> Propagator.from_str("Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]]")
        Propagator(Vertex(1,1),Vertex(3,5),Field(1))
        """
        res = re.search(cls.re(), propagator)
        return Propagator(
            Vertex.from_str(res.group(2)),
            Vertex.from_str(res.group(3 + Vertex.n())),
            Field.from_str(res.group(6 + Vertex.n())),
        )
