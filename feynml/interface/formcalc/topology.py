import re
from dataclasses import dataclass
from typing import List

from feynml.interface.formcalc.propagator import Propagator
from feynml.util import len_not_none

Nlimit = 10


@dataclass
class Topology:
    order: int
    propagators: List[Propagator]

    def __str__(self):
        return (
            f"Topology[{self.order}][{', '.join([str(p) for p in self.propagators])}]"
        )

    @classmethod
    def re(cls):
        rtopology = r"\s*Topology\[(\d+)\]"
        rtopology += r"\[(" + Propagator.re() + r"),?("
        for i in range(Nlimit - 1):
            rtopology += Propagator.re() + r")?,?("
        rtopology += Propagator.re() + r")?\]\s*"
        return rtopology

    @classmethod
    def n(cls):
        """
        Example

        >>> Topology.n() == Topology.re().count('(') -Topology.re().count('(?')
        True
        """
        return 1 + (1 + Propagator.n()) * (Nlimit + 1)

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
        order = int(res.group(1))
        lst = []
        # print(res.groups())
        # return 0
        nn = Propagator.n() + 1
        for i in range(0, int((len_not_none(res.groups()) - 1) / nn)):
            g = res.group(2 + i * nn)
            lst += [Propagator.from_str(g)]
        return Topology(order, lst)
