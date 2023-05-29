import pylhe

from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML, Head, Meta
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.util import leg_id_wrap, vertex_id_wrap
from feynml.vertex import Vertex

# TODO add momenta?


def lhe_event_to_feynman(event: pylhe.LHEEvent) -> FeynmanDiagram:
    fd = FeynmanDiagram()
    hp = Vertex(id=vertex_id_wrap(0))
    fd.add(hp)
    hpids = []
    for lhe_id, p in enumerate(event.particles):
        lhe_id += 1
        pdgid = round(p.id)
        if p.status == -1:
            # outgoing Leg
            fd.add(
                Leg(
                    id=leg_id_wrap(lhe_id),
                    pdgid=pdgid,
                    target=vertex_id_wrap(0),
                    sense="incoming",
                )
            )
            hpids.append(lhe_id)
    for lhe_id, p in enumerate(event.particles):
        lhe_id += 1
        pdgid = round(p.id)
        if p.mother1 in hpids and p.mother2 in hpids:
            if p.status == 1:
                # outgoing Leg
                fd.add(
                    Leg(
                        id=leg_id_wrap(lhe_id),
                        pdgid=pdgid,
                        target=vertex_id_wrap(0),
                        sense="outgoing",
                    )
                )
            if p.status == 2:
                # Propagator
                # create a new vertex...
                fd.add(Vertex(id=vertex_id_wrap(lhe_id)))
                fd.add(
                    Propagator(
                        id=leg_id_wrap(lhe_id),
                        pdgid=pdgid,
                        source=vertex_id_wrap(0),
                        target=vertex_id_wrap(lhe_id),
                    )
                )
    nvertices = 1  # the hard process vertex
    while nvertices != len(fd.vertices):
        nvertices = len(fd.vertices)
        for lhe_id, p in enumerate(event.particles):
            lhe_id += 1
            pdgid = round(p.id)
            # print("Candidate particle: ", lhe_id, p.id, p.status, p.mother1, p.mother2)
            for v in fd.vertices:
                # print("1Candidate particle: ", lhe_id, p.id, p.status, p.mother1, p.mother2)
                if (
                    vertex_id_wrap(p.mother1) == v.id
                    and vertex_id_wrap(p.mother2) == v.id
                ):  # TODO this will not cover all cases, i.e. when there are more than one vertex in the decay chain
                    # print("2Candidate particle: ", lhe_id, p.id, p.status, p.mother1, p.mother2)
                    if p.status == 1:
                        # check if the particle is already in the diagram
                        if not leg_id_wrap(lhe_id) in [l.id for l in fd.legs]:
                            fd.add(
                                Leg(
                                    id=leg_id_wrap(lhe_id),
                                    pdgid=pdgid,
                                    target=v.id,
                                    sense="outgoing",
                                )
                            )
                    if p.status == 2:
                        # Propagator
                        # create a new vertex... , this will result in rerunning the loop
                        if not vertex_id_wrap(lhe_id) in [l.id for l in fd.vertices]:
                            fd.add(Vertex(id=vertex_id_wrap(lhe_id)))
                            fd.add(
                                Propagator(
                                    id=leg_id_wrap(lhe_id),
                                    pdgid=pdgid,
                                    source=v.id,
                                    target=vertex_id_wrap(lhe_id),
                                )
                            )

    assert len(fd.legs) + len(fd.propagators) == len(
        event.particles
    ), "Not all particles are accounted for!\nlegs = {}\npropagators = {}\nparticles = {}".format(
        len(fd.legs), len(fd.propagators), len(event.particles)
    )

    return fd


def lhe_to_feynml(
    lhe_file: str,
    creator="pyfeyn2",
    tool="pyfeyn2.interface.hepmc",
    title="",
    description="",
) -> FeynML:
    fds = []
    events = pylhe.read_lhe_with_attributes(lhe_file)
    for event in events:
        fds.append(lhe_event_to_feynman(event))
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
