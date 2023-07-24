def test_import_feynml():
    import feynml

    fd = feynml.FeynmanDiagram().add(
        feynml.Vertex(),
        feynml.Propagator(),
        feynml.Vertex(),
    )
    assert fd is not None


def test_from_feynml():
    from feynml import FeynmanDiagram, Propagator, Vertex

    fd = FeynmanDiagram().add(
        Vertex(),
        Propagator(),
        Vertex(),
    )
    assert fd is not None
