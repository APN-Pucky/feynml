from feynml.interface.madgraph.ps import ps_to_feynml


def test_load_ps_lo():
    fml = ps_to_feynml("tests/interface/lo.ps")
    assert fml is not None
    assert len(fml.diagrams) == 2


def test_load_ps_born():
    fml = ps_to_feynml("tests/interface/born.ps")
    assert fml is not None
    assert len(fml.diagrams) == 3


def test_load_ps_born_matrix():
    fml = ps_to_feynml("tests/interface/born_matrix.ps")
    assert fml is not None
    assert len(fml.diagrams) == 1


def test_load_ps_matrix_1():
    fml = ps_to_feynml("tests/interface/matrix_1.ps")
    assert fml is not None
    assert len(fml.diagrams) == 6 + 6 + 4


def test_load_ps_matrix_2():
    fml = ps_to_feynml("tests/interface/matrix_2.ps")
    assert fml is not None
    assert len(fml.diagrams) == 5


def test_load_ps_loop_matrix():
    fml = ps_to_feynml("tests/interface/loop_matrix.ps")
    assert fml is not None
    assert len(fml.diagrams) == 6 + 5
