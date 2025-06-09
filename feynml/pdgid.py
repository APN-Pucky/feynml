from dataclasses import dataclass, field
from typing import Optional, Union

from smpl.util import withify
from feynmodel.feyn_model import FeynModel

from feynml.id import Identifiable
from feynml.particle import Particle


PDGID_PARAM = Union[int, str, None]


def is_pdgid_param(p):
    return isinstance(p, int) or isinstance(p, str) or p is None


def pdgid_param(p: PDGID_PARAM) -> dict:
    if p is None:
        return {"type": "line"}
    elif isinstance(p, int):
        return {"pdgid": p}
    elif isinstance(p, str):
        return {"name": p}
    else:
        raise ValueError("Invalid input type")


def to_pdgid(p: PDGID_PARAM) -> int:
    return PDG(**pdgid_param(p)).pdgid


# u = 2
# d = 1
# g = 21
# gamma = 22
# e = 11
# TODO continue here and allow this?


@withify()
@dataclass
class PDG(Identifiable):
    pdgid: Optional[int] = field(
        default=None, metadata={"name": "pdgid", "namespace": "", "type": "Attribute"}
    )
    """PDG ID of the particle"""
    name: Optional[str] = field(default=None, metadata={"type": "Element"})
    """Name of the particle"""
    texname: Optional[str] = field(default=None, metadata={"type": "Element"})
    """LaTeX name of the particle"""
    type: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Type of the particle, e.g. fermion, boson, etc."""

    # particle: Optional[Particle] = field(default=None, metadata={"type": "Ignore"})
    # """Particle object from the particle package"""

    # _particle: Optional[Particle] = field(default=None, metadata={"type": "Ignore"})
    # """Particle object from the particle package"""

    def _sync(self, feynmodel: FeynModel = None):
        """Sync the particle with the pdgid, name and type."""
        particle = None
        if self.pdgid is not None:
            if feynmodel is not None:
                particle = Particle.fromfeynmodel(self.pdgid, feynmodel)
            else:
                particle = Particle.frompdg(self.pdgid)
        if self.name is not None:
            if self.name == "ghG" or self.name == "gh" or self.name == "ghost":
                self.particle = None
                self.pdgid = None
                self.type = "ghost"
                return
            if self.name == "ghG~" or self.name == "gh~" or self.name == "anti ghost":
                self.particle = None
                self.pdgid = None
                self.type = "anti ghost"
                return
            particle = Particle.fromname(self.name)

        if particle is not None:
            if self.texname is None:
                self.texname = particle.texname
            if self.name is None:
                self.name = particle.name
            if self.pdgid is None:
                self.pdgid = particle.pdgid
            if self.type is None:
                self.type = particle.get_type()

    def is_anti_fermion(self):
        """Return True if the particle is an anti fermion, False otherwise."""
        return self.type == "anti fermion"

    def is_fermion(self):
        """Return True if the particle is a fermion, False otherwise."""
        return self.type == "fermion"

    def is_any_fermion(self):
        """Return True if the particle is a fermion or anti fermion, False otherwise."""
        return self.type == "fermion" or self.type == "anti fermion"

    def is_anti(self):
        """Return True if the particle is an anti particle, False otherwise."""
        return self.pdgid < 0  # TODO use pdg option?

    def __post_init__(self):
        super().__post_init__()
        self._sync()

    def with_pdgid(
        self,
        pdgid: int = None,
        type: str = None,
        name: str = None,
        feynmodel: FeynModel = None,
        sync=True,
    ):
        self.pdgid = pdgid
        self.name = name
        self.type = type
        if sync:
            self._sync(feynmodel=feynmodel)
        return self
