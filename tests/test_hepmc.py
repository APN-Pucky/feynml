import pyhepmc

from pyfeyn2.interface.hepmc import event_to_feynman


def test_hepmc():
    with pyhepmc.open("tests/example.HepMC") as f:
        for event in f:
            event_to_feynman(event)
            break


test_hepmc()
