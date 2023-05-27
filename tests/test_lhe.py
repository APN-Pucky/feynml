import pylhe

from feynml.interface.lhe import lhe_event_to_feynman, lhe_to_feynml


def test_lhe_to_feynman():
    events = pylhe.read_lhe("tests/example.lhe")
    for event in events:
        lhe_event_to_feynman(event)
        break


def test_lhe_to_feynml():
    fml = lhe_to_feynml("tests/example.lhe")
    print(fml.to_xml())


test_lhe_to_feynman()
test_lhe_to_feynml()
