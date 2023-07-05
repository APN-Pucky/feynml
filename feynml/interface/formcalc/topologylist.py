import re
from dataclasses import dataclass
from typing import List, Tuple

from feynml.feynml import FeynML
from feynml.head import Head
from feynml.interface.formcalc.insertions import Insertions
from feynml.interface.formcalc.topology import Topology
from feynml.meta import Meta


@dataclass
class TopologyList:
    rest: str
    topologies: List[Tuple[Topology, Insertions]]

    def to_feynml(
        self,
        creator="pyfeyn2",
        tool="pyfeyn2.interface.formcalc",
        title="",
        description="",
    ) -> FeynML:
        fds = []
        for t in self.topologies:
            fds.append(t[0].to_feynml(t[1]))
        return FeynML(
            head=Head(
                metas=[
                    Meta(name="creator", content=creator),
                    Meta(name="tool", content=tool),
                    Meta(name="description", content=description),
                    Meta(name="title", content=title),
                ]
            ),
            diagrams=fds,
        )

    def __str__(self):
        return f"TopologyList[{self.rest}][{','.join([str(ti[0]) +' -> ' + str(ti[1])  for ti in self.topologies ])}]"

    @classmethod
    def re(cls, full=True):
        if full:
            rtopology = Topology.re()
            rinsertions = Insertions.re()
        else:
            rtopology = r"\s*Topology\[\d+\]\[.*?\]\s*"
            rinsertions = r"\s*Insertions\[Generic\]\[.*?\]\s*"

        rtopologylist = r"\s*TopologyList\[(.*)\]\["
        rtopologylist += r"((?:" + rtopology + r"->" + rinsertions + r",?)+)\]\s*"
        return rtopologylist

    @classmethod
    def n(cls):
        """
        Example

        >>> TopologyList.n() == TopologyList.re().count('(') -TopologyList.re().count('(?')
        True
        """
        return 1 + 1 + Topology.n() + Insertions.n()

    @classmethod
    def from_str(cls, topologylist: str):
        """
        Example

        >>> str(TopologyList.from_str('TopologyList[\
        Process -> {V[1], V[1]} -> {-F[3, {3, SequenceForm["Col", 3]}], \
        F[3, {3, SequenceForm["Col", 4]}]}, Model -> {"SM"}, \
        GenericModel -> {"Lorentz"}, InsertionLevel -> {Generic, Classes}, \
        ExcludeParticles -> {}, \
        ExcludeFieldPoints -> {FieldPoint[0][-F[1], F[2], -S[3]], \
        FieldPoint[0][F[1], -F[2], S[3]], \
        FieldPoint[0][-F[2], F[2], S[1]], \
        FieldPoint[0][-F[2], F[2], S[2]], \
        FieldPoint[0][-F[4], F[4], S[1]], \
        FieldPoint[0][-F[4], F[4], S[2]], \
        FieldPoint[1][-F[1], F[2], -S[3]], \
        FieldPoint[1][F[1], -F[2], S[3]], \
        FieldPoint[1][-F[2], F[2], S[1]], \
        FieldPoint[1][-F[2], F[2], S[2]], \
        FieldPoint[1][-F[4], F[4], S[1]], \
        FieldPoint[1][-F[4], F[4], S[2]]}, LastSelections -> {}][\
        Topology[1][\
        Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], \
        Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], \
        Propagator[Outgoing][Vertex[1][3], Vertex[3][5], Field[3]], \
        Propagator[Outgoing][Vertex[1][4], Vertex[3][6], Field[4]], \
        Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]] -> \
        Insertions[Generic][\
        FeynmanGraph[1, Generic == 1][Field[1] -> V[1], Field[2] -> V[1], \
        Field[3] -> F[3, {3, SequenceForm["Col", 3]}], \
        Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> F] ->\
        Insertions[Classes][\
        FeynmanGraph[1, Classes == 1][Field[1] -> V[1], Field[2] -> V[1],\
        Field[3] -> F[3, {3, SequenceForm["Col", 3]}], \
        Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], \
        Field[5] -> F[3, {3, SequenceForm["Col", 3]}]]]], \
        Topology[1][\
        Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], \
        Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], \
        Propagator[Outgoing][Vertex[1][3], Vertex[3][6], Field[3]], \
        Propagator[Outgoing][Vertex[1][4], Vertex[3][5], Field[4]], \
        Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]] -> \
        Insertions[Generic][\
        FeynmanGraph[1, Generic == 1][Field[1] -> V[1], Field[2] -> V[1], \
        Field[3] -> F[3, {3, SequenceForm["Col", 3]}], \
        Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> F] ->\
        Insertions[Classes][\
        FeynmanGraph[1, Classes == 1][Field[1] -> V[1], Field[2] -> V[1],\
        Field[3] -> F[3, {3, SequenceForm["Col", 3]}], \
        Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], \
        Field[5] -> -F[3, {3, SequenceForm["Col", 3]}]]]]]'))
        'TopologyList[ Process -> {V[1], V[1]} -> {-F[3, {3, SequenceForm["Col", 3]}], F[3, {3, SequenceForm["Col", 4]}]}, Model -> {"SM"}, GenericModel -> {"Lorentz"}, InsertionLevel -> {Generic, Classes}, ExcludeParticles -> {}, ExcludeFieldPoints -> {FieldPoint[0][-F[1], F[2], -S[3]], FieldPoint[0][F[1], -F[2], S[3]], FieldPoint[0][-F[2], F[2], S[1]], FieldPoint[0][-F[2], F[2], S[2]], FieldPoint[0][-F[4], F[4], S[1]], FieldPoint[0][-F[4], F[4], S[2]], FieldPoint[1][-F[1], F[2], -S[3]], FieldPoint[1][F[1], -F[2], S[3]], FieldPoint[1][-F[2], F[2], S[1]], FieldPoint[1][-F[2], F[2], S[2]], FieldPoint[1][-F[4], F[4], S[1]], FieldPoint[1][-F[4], F[4], S[2]]}, LastSelections -> {}][Topology[1][Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], Propagator[Outgoing][Vertex[1][3], Vertex[3][5], Field[3]], Propagator[Outgoing][Vertex[1][4], Vertex[3][6], Field[4]], Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]] -> Insertions[Generic][FeynmanGraph[1, Generic == 1][Field[1] -> V[1], Field[2] -> V[1], Field[3] -> F[3, {3, SequenceForm["Col", 3]}], Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> F] -> Insertions[Classes][FeynmanGraph[1, Classes == 1][Field[1] -> V[1], Field[2] -> V[1], Field[3] -> F[3, {3, SequenceForm["Col", 3]}], Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> F[3, {3, SequenceForm["Col", 3]}]]]],Topology[1][Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], Propagator[Outgoing][Vertex[1][3], Vertex[3][6], Field[3]], Propagator[Outgoing][Vertex[1][4], Vertex[3][5], Field[4]], Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]] -> Insertions[Generic][FeynmanGraph[1, Generic == 1][Field[1] -> V[1], Field[2] -> V[1], Field[3] -> F[3, {3, SequenceForm["Col", 3]}], Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> F] -> Insertions[Classes][FeynmanGraph[1, Classes == 1][Field[1] -> V[1], Field[2] -> V[1], Field[3] -> F[3, {3, SequenceForm["Col", 3]}], Field[4] -> -F[3, {3, SequenceForm["Col", 4]}], Field[5] -> -F[3, {3, SequenceForm["Col", 3]}]]]]]'
        """
        res = re.search(cls.re(), topologylist)
        rest = res.group(1).replace("\t", " ")
        # remove repeated whitespaces from rest
        rest = re.sub(r"\s+", " ", rest)
        lst = []

        for x in re.findall(
            r"(" + Topology.re() + r")->(" + Insertions.re() + r"),?", res.group(2)
        ):
            lst += [
                (
                    Topology.from_str(x[0]),
                    Insertions.from_str(x[Topology.n() + 1]),
                )
            ]
        return TopologyList(rest, lst)
