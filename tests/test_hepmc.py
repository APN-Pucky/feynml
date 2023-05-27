import pyhepmc

from feynml.interface.hepmc import hepmc_event_to_feynman, hepmc_to_feynml


def test_hepmc_to_feynman():
    with pyhepmc.open("tests/example.HepMC") as f:
        for event in f:
            hepmc_event_to_feynman(event)
            break


def test_hepmc_to_feynml():
    hepmc_to_feynml("tests/example.HepMC")


test_hepmc_to_feynman()
