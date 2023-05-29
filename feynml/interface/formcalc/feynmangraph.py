import re
from dataclasses import dataclass
from typing import List

from feynml.interface.formcalc.rule import Rule
from feynml.util import len_not_none

Nlimit = 10


@dataclass
class FeynmanGraph:
    order: int
    type: str
    type_i: int
    rules: List[Rule]

    def __str__(self):
        return f"FeynmanGraph[{self.order}, {self.type} == {self.type_i}][{', '.join([str(rule) for rule in self.rules]) }]"

    @classmethod
    def re(cls):
        rgraph = r"\s*FeynmanGraph\[(\d+),\s*(Generic|Classes)\s*==\s*(\d+)\]"
        rgraph += r"\[(" + Rule.re() + r"),?("
        for i in range(Nlimit - 1):
            rgraph += Rule.re() + r")?,?("
        rgraph += Rule.re() + r")?\]\s*"
        return rgraph

    @classmethod
    def n(cls):
        """
        Example

        >>> FeynmanGraph.n() == FeynmanGraph.re().count('(') - FeynmanGraph.re().count('(?')
        True
        """
        return 1 + 1 + 1 + (1 + Nlimit) * (1 + Rule.n())

    @classmethod
    def from_str(cls, graph: str):
        """
        Example


        >>> str(FeynmanGraph.from_str('FeynmanGraph[1, Generic == 1][Field[1] -> V[1]]'))
        'FeynmanGraph[1, Generic == 1][Field[1] -> V[1]]'

        >>> str(FeynmanGraph.from_str('FeynmanGraph[1, Generic == 1][\
        Field[1] -> F[3, {1, SequenceForm["Col", 1]}], \
        Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], \
        Field[4] -> V[5, {\
        SequenceForm["Glu", 4]}], Field[5] -> F]'))
        'FeynmanGraph[1, Generic == 1][Field[1] -> F[3, {1, SequenceForm["Col", 1]}], Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], Field[4] -> V[5, {SequenceForm["Glu", 4]}], Field[5] -> F]'
        """
        res = re.search(cls.re(), graph)
        order = int(res.group(1))
        type = res.group(2)
        type_i = int(res.group(3))
        lst = []
        # print(res.groups())
        # return 0
        nn = Rule.n() + 1
        i = 0

        g = res.group(4 + i * nn)
        while g is not None and i < Nlimit and 4 + i * nn < len(res.groups()):
            lst += [Rule.from_str(g)]
            # print(g)
            i += 1
            g = res.group(4 + i * nn)
        return FeynmanGraph(order, type, type_i, lst)
