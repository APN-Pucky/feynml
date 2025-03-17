"""
Generate a list of topologies with incoming/outgoing number of legs and loops.
"""

import logging
from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML
from feynml.leg import Leg
from feynml.topology import three


def generate_topologies(incoming: int, outgoing: int, loops: int = 0):
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
        fd_new.add(Leg(sense=sense, target=fd_new.vertices[i].id))
        fds.append(fd_new)
    for i, _ in enumerate(fd.legs):
        fd_new = fd.deepcopy()
        fd_new.emission(fd_new.legs[i], Leg(sense=sense))
        fds.append(fd_new)
    for i, _ in enumerate(fd.propagators):
        fd_new = fd.deepcopy()
        fd_new.emission(fd_new.propagators[i], Leg(sense=sense))
        fds.append(fd_new)
    # for i in fds:
    #    i.render(debug=True)
    return fds
