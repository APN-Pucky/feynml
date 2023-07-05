import re
from dataclasses import dataclass
from typing import List

from feynml.feynmandiagram import FeynmanDiagram
from feynml.interface.formcalc.insertions import Insertions
from feynml.interface.formcalc.propagator import Propagator


@dataclass
class Topology:
    order: int
    propagators: List[Propagator]

    def to_feynml(self, insertions: Insertions) -> FeynmanDiagram:
        fd = FeynmanDiagram()
        for p in self.propagators:
            prop, verts = p.to_feynml(insertions)
            fd.add(prop)
            for v in verts:
                if not fd.has_vertex_id(v.id):  # Unique vertices
                    fd.add(v)
        return fd

    def __str__(self):
        return (
            f"Topology[{self.order}][{', '.join([str(p) for p in self.propagators])}]"
        )

    @classmethod
    def re(cls):
        rtopology = r"\s*Topology\[(\d+)\]"
        rtopology += r"\[((?:" + Propagator.re() + r",?)+)\]\s*"
        return rtopology

    @classmethod
    def n(cls):
        """
        Example

        >>> Topology.n() == Topology.re().count('(') -Topology.re().count('(?')
        True
        """
        return 1 + 1 + Propagator.n()

    @classmethod
    def from_str(cls, topology: str):
        """
        Example

        >>> str(Topology.from_str('Topology[1][\
        Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], \
        Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], \
        Propagator[Outgoing][Vertex[1][3], Vertex[3][6], Field[3]], \
        Propagator[Outgoing][Vertex[1][4], Vertex[3][5], Field[4]], \
        Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]]'))
        'Topology[1][Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], Propagator[Outgoing][Vertex[1][3], Vertex[3][6], Field[3]], Propagator[Outgoing][Vertex[1][4], Vertex[3][5], Field[4]], Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]]'
        """
        res = re.search(cls.re(), topology)
        return cls._handle_match(res)

    @classmethod
    def _handle_match(cls, res):
        order = int(res.group(1))
        lst = []
        # print(res.groups())
        # return 0

        for x in re.findall(r"(" + Propagator.re() + r"),?", res.group(2)):
            lst += [Propagator.from_str(x[0])]

        return Topology(order, lst)
