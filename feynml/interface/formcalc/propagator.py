import re
from dataclasses import dataclass
from typing import List, Tuple

from feynml.connector import Connector
from feynml.interface.formcalc.field import Field
from feynml.interface.formcalc.insertions import Insertions
from feynml.interface.formcalc.vertex import Vertex
from feynml.leg import Leg as FMLLeg
from feynml.propagator import Propagator as FMLPropagator


@dataclass
class Propagator:
    type: str
    v1: Vertex
    v2: Vertex
    f: Field

    def to_feynml(self, insertions: Insertions) -> Tuple[Connector, List[Vertex]]:
        if self.type == "Internal":
            fmlv1 = self.v1.to_feynml()
            fmlv2 = self.v2.to_feynml()
            return FMLPropagator(
                source=fmlv2.id, target=fmlv1.id, pdgid=insertions.get_pdgid(self.f)
            ), [fmlv1, fmlv2]
        elif self.type == "Incoming":
            fmlv1 = self.v1.to_feynml()
            fmlv2 = self.v2.to_feynml()
            return FMLLeg(
                target=fmlv2.id, sense="incoming", pdgid=insertions.get_pdgid(self.f)
            ), [fmlv2]
        elif self.type == "Outgoing":
            fmlv1 = self.v1.to_feynml()
            fmlv2 = self.v2.to_feynml()
            return FMLLeg(
                target=fmlv2.id, sense="outgoing", pdgid=insertions.get_pdgid(self.f)
            ), [fmlv2]
        else:
            raise Exception("Unknown propagator type")

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
