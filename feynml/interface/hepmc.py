import pyhepmc
from pyhepmc import GenEvent

from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML, Head, Meta
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.util import leg_id_wrap, propagator_id_wrap, vertex_id_wrap
from feynml.vertex import Vertex

# TODO add momenta?


def hepmc_event_to_feynman(event: GenEvent) -> FeynmanDiagram:
    """
    Convert a GenEvent to a FeynmanDiagram.

    Args:
        event: The GenEvent to convert.

    Returns:
        A FeynmanDiagram object.
    """
    fd = FeynmanDiagram()
    for v in event.vertices:
        v = Vertex(id=vertex_id_wrap(v.id))
        fd.add(v)
    for p in event.particles:
        # TODO first create all vertices?
        if p.status == 4:
            # incoming Leg
            fd.add(
                Leg(
                    id=leg_id_wrap(p.id),
                    pdgid=p.pid,
                    target=vertex_id_wrap(p.end_vertex.id),
                    sense="incoming",
                )
            )
        elif p.status == 1:
            # outgoing Leg
            fd.add(
                Leg(
                    id=leg_id_wrap(p.id),
                    pdgid=p.pid,
                    target=vertex_id_wrap(p.production_vertex.id),
                    sense="outgoing",
                )
            )
        else:
            # Propagator
            fd.add(
                Propagator(
                    id=propagator_id_wrap(p.id),
                    pdgid=p.pid,
                    source=vertex_id_wrap(p.production_vertex.id),
                    target=vertex_id_wrap(p.end_vertex.id),
                )
            )
    return fd


def hepmc_to_feynml(
    hepmc_file: str,
    creator="pyfeyn2",
    tool="pyfeyn2.interface.hepmc",
    title="",
    description="",
) -> FeynML:
    """
    Convert a HepMC file to a FeynML object.

    Args:
        hepmc_file: The path to the HepMC file.
        creator: The creator of the file.
        tool: The tool used to create the file.
        title: The title of the file.
        description: The description of the file.

    Returns:
        A FeynML object.
    """
    fds = []
    with pyhepmc.open(hepmc_file) as f:
        for event in f:
            fds.append(hepmc_event_to_feynman(event))
    return FeynML(
        diagrams=fds,
        head=Head(
            metas=[
                Meta(name="creator", content=creator),
                Meta(name="tool", content=tool),
                Meta(name="description", content=description),
                Meta(name="title", content=title),
            ]
        ),
    )
