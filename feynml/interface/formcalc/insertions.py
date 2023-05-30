import re
from dataclasses import dataclass
from typing import List

from feynml.interface.formcalc.feynmangraph import FeynmanGraph
from feynml.interface.formcalc.field import Field


@dataclass
class Insertions:
    generic: FeynmanGraph
    classes: FeynmanGraph

    def get_pdgid(self, f: Field) -> int:
        for r in self.classes.rules:
            if f == r.lhs:
                return r.rhs.get_pdgid()
        raise Exception(f"Field {f} not found in Insertions {self}")

    def __str__(self):
        return f"Insertions[Generic][{self.generic} -> Insertions[Classes][{self.classes}]]"

    @classmethod
    def re(cls):
        rgraph = (
            r"\s*Insertions\[Generic\]\[("
            + FeynmanGraph.re()
            + r")\s*->\s*Insertions\[Classes\]\[("
            + FeynmanGraph.re()
            + r")\]\]\s*"
        )
        return rgraph

    @classmethod
    def n(cls):
        """
        Example

        >>> Insertions.n() == Insertions.re().count('(') - Insertions.re().count('(?')
        True
        """
        return 1 + FeynmanGraph.n() + 1 + FeynmanGraph.n()

    @classmethod
    def from_str(cls, insertions: str):
        """
        Example


        >>> str(Insertions.from_str('Insertions[Generic][\
        FeynmanGraph[1, Generic == 1][\
        Field[1] -> F[3, {1, SequenceForm["Col", 1]}]] -> \
        Insertions[Classes][\
        FeynmanGraph[1, Classes == 1][\
        Field[1] -> F[3, {1, SequenceForm["Col", 1]}]]]]'))
        'Insertions[Generic][FeynmanGraph[1, Generic == 1][Field[1] -> F[3, {1, SequenceForm["Col", 1]}]] -> Insertions[Classes][FeynmanGraph[1, Classes == 1][Field[1] -> F[3, {1, SequenceForm["Col", 1]}]]]]'

        >>> str(Insertions.from_str('Insertions[Generic][\
        FeynmanGraph[1, Generic == 1][\
        Field[1] -> F[3, {1, SequenceForm["Col", 1]}], \
        Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], \
        Field[4] -> V[5, {\
        SequenceForm["Glu", 4]}], Field[5] -> F] -> \
        Insertions[Classes][\
        FeynmanGraph[1, Classes == 1][\
        Field[1] -> F[3, {1, SequenceForm["Col", 1]}], \
        Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], \
        Field[4] -> V[5, {\
        SequenceForm["Glu", 4]}], \
        Field[5] -> F[3, {1, SequenceForm["Col", 2]}]]]]'))
        'Insertions[Generic][FeynmanGraph[1, Generic == 1][Field[1] -> F[3, {1, SequenceForm["Col", 1]}], Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], Field[4] -> V[5, {SequenceForm["Glu", 4]}], Field[5] -> F] -> Insertions[Classes][FeynmanGraph[1, Classes == 1][Field[1] -> F[3, {1, SequenceForm["Col", 1]}], Field[2] -> -F[3, {1, SequenceForm["Col", 2]}], Field[3] -> V[1], Field[4] -> V[5, {SequenceForm["Glu", 4]}], Field[5] -> F[3, {1, SequenceForm["Col", 2]}]]]]'
        """
        res = re.search(cls.re(), insertions)
        return cls._handle_match(res)
        generic = FeynmanGraph.from_str(res.group(1))
        # print(res.groups())
        classes = None
        classes = FeynmanGraph.from_str(res.group(FeynmanGraph.n() + 2))

        return Insertions(generic, classes)

    @classmethod
    def _handle_match(cls, res):
        generic = FeynmanGraph.from_str(res.group(1))
        classes = FeynmanGraph.from_str(res.group(FeynmanGraph.n() + 2))
        return Insertions(generic, classes)
