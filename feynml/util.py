from smpl_doc.doc import deprecated


def id_wrap(idd, id_type=""):
    """
    Wrap a id in the format expected by feynml.

    Args:
        idd: The id.

    Returns:
        The wrapped id.

    Examples:
        >>> id_wrap(1)
        '1'
        >>> id_wrap(-1)
        'm1'
    """
    return id_type + str(round(idd)).replace("-", "m")


def vertex_id_wrap(idd):
    """
    Wrap a vertex id in the format expected by feynml.

    Args:
        idd: The id of the vertex.

    Returns:
        The wrapped id.

    Examples:
        >>> vertex_id_wrap(1)
        'Vertex1'
        >>> vertex_id_wrap(-1)
        'Vertexm1'
    """
    return id_wrap(idd, "Vertex")


def leg_id_wrap(idd):
    """
    Wrap a leg id in the format expected by feynml.

    Args:
        idd: The id of the leg.

    Returns:
        The wrapped id.

    Examples:
        >>> leg_id_wrap(1)
        'Leg1'
        >>> leg_id_wrap(-1)
        'Legm1'
    """
    return id_wrap(idd, "Leg")


def propagator_id_wrap(idd):
    """
    Wrap a propagator id in the format expected by feynml.

    Args:
        idd: The id of the propagator.

    Returns:
        The wrapped id.

    Examples:
        >>> propagator_id_wrap(1)
        'Propagator1'
        >>> propagator_id_wrap(-1)
        'Propagatorm1'
    """
    return id_wrap(idd, "Propagator")
