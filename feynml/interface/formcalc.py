"""
Import/Export TopologyList from FormCalc to FeynML
"""

import re

from attr import dataclass

from feynml.feynmandiagram import FeynmanDiagram

Nlimit = 10

rpropagator = (
    r"\s*Propagator\[(Incoming|Outgoing|Internal)\]\[("
    + rvertex
    + r"),("
    + rvertex
    + r"),("
    + rfield
    + r")\]\s*"
)
npropagator = 1 + 1 + nvertex + 1 + nvertex + 1 + nfield


def _parse_propagator(propagator: str):
    """
    Example

    >>> _parse_propagator("Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]]")
    ('Incoming', (1, 1), (3, 5), 1)
    """
    res = re.search(rpropagator, propagator)
    return (
        res.group(1),
        _parse_vertex(res.group(2)),
        _parse_vertex(res.group(3 + 2)),
        _parse_field(res.group(6 + 2)),
    )


# Only 10 Propagators as of now but can be extended easily
rtopology = r"\s*Topology\[(\d+)\]"
rtopology += r"\[(" + rpropagator + r"),?("
for i in range(Nlimit):
    rtopology += rpropagator + r")?,?("
rtopology += rpropagator + r")?\]\s*"
# rtopology = r"\s*Topology\[(\d+)\]\[(" + rpropagator +"(,"+ rpropagator, ")?\]"


def _parse_topology(topology: str) -> FeynmanDiagram:
    """
    Example

    >>> _parse_topology("Topology[1][\
    Propagator[Incoming][Vertex[1][1], Vertex[3][5], Field[1]], \
    Propagator[Incoming][Vertex[1][2], Vertex[3][6], Field[2]], \
    Propagator[Outgoing][Vertex[1][3], Vertex[3][5], Field[3]], \
    Propagator[Outgoing][Vertex[1][4], Vertex[3][6], Field[4]], \
    Propagator[Internal][Vertex[3][5], Vertex[3][6], Field[5]]]")
    (1, [('Incoming', (1, 1), (3, 5), 1), ('Incoming', (1, 2), (3, 6), 2), ('Outgoing', (1, 3), (3, 5), 3), ('Outgoing', (1, 4), (3, 6), 4), ('Internal', (3, 5), (3, 6), 5)])
    """
    # print(rtopology)
    res = re.search(rtopology, topology)
    order = int(res.group(1))
    lst = []
    # print(res.groups())
    # return 0
    nn = npropagator + 1
    for i in range(0, int((len_not_none(res.groups()) - 1) / nn)):
        g = res.group(2 + i * nn)
        lst += [_parse_propagator(g)]
    return (order, lst)


rsquenceform = r"\s*\{(\d+)\s*,\s*SequenceForm\[\"(\w+)\",\s*(\d+)\]\}\s*"
nsequenceform = 3


def _parse_sequenceform(sequenceform: str):
    """
    Example

    >>> _parse_sequenceform("{1, SequenceForm[\"Col\", 1]}")
    (1, 'Col', 1)
    """
    res = re.search(rsquenceform, sequenceform)
    return int(res.group(1)), res.group(2), int(res.group(3))


rparticle = r"\s*(?:(V)\[(\d+)\]|(F)\[(\d+)," + rsquenceform + r"\])\s*"


def _parse_particle(particle: str):
    """
    Example

    >>> _parse_particle("V[1]")
    ('V', 1)
    >>> _parse_particle("F[3, {1, SequenceForm[\"Col\", 1]}]")
    ('F', 3, (1, 'Col', 1))
    """
    res = re.search(rparticle, particle)
    if res.group(1) is not None:
        return res.group(1), int(res.group(2))
    else:
        return res.group(3), int(res.group(4)), _parse_sequenceform(res.group(5))


rrule = rfield + r"\s*->\s*" + rparticle


def _parse_rule(rule: str):
    """
    Example

    >>> _parse_rule("Field[1] -> V[1]")
    (1, ('V', 1))
    >>> _parse_rule("Field[1] -> F[3, {1, SequenceForm[\"Col\", 1]}]")
    (1, ('F', 3, (1, 'Col', 1)))
    """
    res = re.search(rrule, rule)
    return _parse_field(res.group(1)), _parse_particle(res.group(2))


rinsertions = r"\s*Insertions\[(Generic|Classes)\]FeynmanGraph\[(\d+),\s*(Generic|Classes)\s*==\s*(\d+)\]"
rinsertions += r"\[(" + rrule + r")(,"
for i in range(Nlimit):
    rinsertions += rrule + r")?(,"
rinsertions += rrule + r")?\]\s*"


def _parse_insertions(insertions: str):
    """
    Example

    >>> _parse_insertions('Insertions[Generic][\
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
    Field[5] -> F[3, {1, SequenceForm["Col", 2]}]]]]')
    0
    """
    return 0
