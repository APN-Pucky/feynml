"""
Generate a list of topologies with incoming/outgoing number of legs and loops.
"""

import itertools
import logging
from typing import List

from feynmodel.feyn_model import FeynModel

from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML
from feynml.leg import Leg
from feynml.pdgid import pdgid_param
from feynml.topology import three


def generate_fml(
    feyn_model: FeynModel,
    incoming_pdgs: List[int],
    outgoing_pdgs: List[int],
    loops: int = 0,
):
    fml = generate_topologies(len(incoming_pdgs), len(outgoing_pdgs), loops=loops)
    return insert_fields(fml, feyn_model, incoming_pdgs, outgoing_pdgs)


def insert_fields(
    fml: FeynML, fm: FeynModel, incoming: List[int], outgoing: List[int], progress=True
) -> FeynML:
    """
    For each diagram deep copy it.
    Then loop over every propagator and over every particle from the feynmodel (itertools).
    If the diagram is valid for given models' vertices add it to the return list (to be implemented in FeynmanDiagram class taking also the model as parameter).
    """
    # TODO maybe skip already inserted fields!, maybe skip legs?
    # TODO assert inserted legs
    ret = []
    for _fdi, fd in enumerate(fml.diagrams):
        for i, le in enumerate([ll for ll in fd.legs if ll.is_incoming()]):
            le.with_pdgid(incoming[i], feynmodel=fm, sync=True)
        for i, le in enumerate([ll for ll in fd.legs if ll.is_outgoing()]):
            le.with_pdgid(outgoing[i], feynmodel=fm, sync=True)
        # TODO speed up, by not considering all combinations but only the valid ones, step by step
        # TODO remove duplicates from list
        for ps in itertools.product(
            [p.pdg_code for p in fm.particles], repeat=len(fd.propagators)
        ):
            for i, p in enumerate(ps):
                fd.propagators[i].with_pdgid(
                    pdgid=p, feynmodel=fm, sync=True
                )  # we need sync to know if it is a fermion
            if fd.is_valid(fm, only_vertex=True):
                # deep copy is very slow..
                ret.append(fd.fastcopy())

    return FeynML(diagrams=ret)


def generate_topologies(incoming: int, outgoing: int, loops: int = 0) -> FeynML:
    logging.debug(f"generate_topologies({incoming}, {outgoing}, {loops})")
    assert incoming > 0
    assert outgoing > 0
    if loops == 0:
        fds = []
        if incoming == 2 and outgoing == 1:
            fds = [three.fusion()]
        elif incoming == 1 and outgoing == 2:
            fds = [three.decay()]
        # subtract one from either incoming or outgoing in case one is already zero
        elif outgoing > 1:
            for fd in generate_topologies(incoming, outgoing - 1, loops).diagrams:
                fds.extend(add_leg(fd, sense="outgoing"))
        elif incoming > 1:
            for fd in generate_topologies(incoming - 1, outgoing, loops).diagrams:
                fds.extend(add_leg(fd, sense="incoming"))
        else:
            raise ValueError(f"unexpected incoming={incoming} and outgoing={outgoing}")

    else:
        fds = generate_topologies(incoming, outgoing + 2, loops - 1).diagrams
        for fd in fds:
            fd.merge_legs(fd.legs[-1], fd.legs[-2])

    for i, fdsi in enumerate(fds):
        for j in range(i + 1, len(fds)):
            if fdsi is not None and fds[j] is not None and fdsi.is_isomorphic(fds[j]):
                logging.debug(f"removing isomorphic diagrams {i} and {j}")
                fds[j] = None
    # remove Nones
    fds = [fd for fd in fds if fd is not None]
    logging.debug(f"return_topologies({incoming}, {outgoing}, {loops})")
    return FeynML(diagrams=fds)


def add_leg(fd: FeynmanDiagram, sense):
    fds = []
    # fd.render(debug=True)
    for i, _ in enumerate(fd.vertices):
        fd_new = fd.deepcopy()
        fd_new.add(Leg(**pdgid_param(None), sense=sense, target=fd_new.vertices[i].id))
        fds.append(fd_new)
    for i, _ in enumerate(fd.legs):
        fd_new = fd.deepcopy()
        fd_new.emission(fd_new.legs[i], Leg(**pdgid_param(None), sense=sense))
        fds.append(fd_new)
    for i, _ in enumerate(fd.propagators):
        fd_new = fd.deepcopy()
        fd_new.emission(fd_new.propagators[i], Leg(**pdgid_param(None), sense=sense))
        fds.append(fd_new)
    # for i in fds:
    #    i.render(debug=True)
    return fds
