from particle import PDGID, Particle
from particle.converters.bimap import DirectionalMaps

PDG2LaTeXNameMap, LaTeX2PDGNameMap = DirectionalMaps(
    "PDGID", "LaTexName", converters=(PDGID, str)
)

PDG2Name2IDMap, PDGID2NameMap = DirectionalMaps(
    "PDGName", "PDGID", converters=(str, PDGID)
)


def get_name(pid: int) -> str:
    """
    Get the latex name of a particle.

    Args:
        pid (int) : PDG Monte Carlo identifier for the particle.

    Returns:
        str: Latex name.

    Examples:
        >>> get_name(21)
        'g'
        >>> get_name(1000022)
        '\\\\tilde{\\\\chi}_{1}^{0}'
    """
    global PDG2LaTeXNameMap
    pdgid = PDG2LaTeXNameMap[pid]
    return pdgid


def get_particle(**kwargs) -> Particle:
    try:
        (particle,) = Particle.finditer(
            **kwargs
        )  # throws an error if < 1 or > 1 particle is found
        return particle
    except ValueError:
        return None


name_cache = {}


def get_either_particle(cache=True, **kwargs) -> Particle:
    global name_cache
    if cache:
        if str(kwargs) in name_cache:
            return name_cache[str(kwargs)]
    for k, v in kwargs.items():
        p = get_particle(**{k: v})
        if p is not None:
            if cache:
                name_cache[str(kwargs)] = p
            return p

    if cache:
        name_cache[str(kwargs)] = None
    return None
