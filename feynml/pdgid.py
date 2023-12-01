import warnings
from dataclasses import dataclass, field
from typing import Optional

from particle import Particle
from smpl_util.util import withify

from feynml.id import Identifiable

from .particles import get_either_particle


@withify()
@dataclass
class PDG(Identifiable):
    pdgid: Optional[int] = field(
        default=None, metadata={"name": "pdgid", "namespace": "", "type": "Attribute"}
    )
    """PDG ID of the particle"""
    name: Optional[str] = field(default=None, metadata={"type": "Element"})
    """Name of the particle"""
    type: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Type of the particle, e.g. fermion, boson, etc."""

    # TODO check SUSY
    particle: Optional[Particle] = field(default=None, metadata={"type": "Ignore"})
    """Particle object from the particle package"""

    def _sync(self):
        """Sync the particle with the pdgid, name etc."""
        if self.pdgid is not None:
            self.particle = Particle.from_pdgid(self.pdgid)
            self.name = self.particle.name
        elif self.name is not None:
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
            self.particle = get_either_particle(
                programmatic_name=self.name,
                name=self.name,
                evtgen_name=self.name,
                html_name=self.name,
                latex_name=self.name,
            )
            if self.particle is None:
                raise ValueError(f"Particle {self.name} not found")
            self.pdgid = int(self.particle.pdgid)

        if self.pdgid is not None:
            tmptype = self.type
            # TODO infere type from pdgid
            if self.pdgid in range(1, 7):
                self.type = "fermion"
            elif -self.pdgid in range(1, 7):
                self.type = "anti fermion"
            elif self.pdgid == 22:
                self.type = "photon"
            elif self.pdgid == 21:
                self.type = "gluon"
            elif self.pdgid in range(11, 19):
                self.type = "fermion"
            elif -self.pdgid in range(11, 19):
                self.type = "anti fermion"
            elif abs(self.pdgid) == 24:
                self.type = "boson"
            elif self.pdgid == 23:
                self.type = "boson"
            elif self.pdgid == 25:
                self.type = "higgs"
            elif self.pdgid == 2212:  # proton
                self.type = "baryon"
            elif self.pdgid == -2212:  # anti proton
                self.type = "anti baryon"
            elif self.pdgid == 111:  # pion
                self.type = "meson"
            elif abs(self.pdgid) == 211:  # pion
                self.type = "meson"
            elif self.pdgid < 1000000 and self.pdgid > 100:
                if self.particle.pdgid.J == 0:
                    self.type = "line"
                elif self.particle.pdgid.J == 1:
                    self.type = "line"
                elif self.particle.pdgid.J == 0.5:
                    self.type = "fermion"
                elif self.particle.pdgid.J == 1.5:
                    self.type = "fermion"
            elif self.pdgid > -1000000 and self.pdgid < -100:
                if self.particle.pdgid.J == 0:
                    self.type = "line"
                elif self.particle.pdgid.J == 1:
                    self.type = "line"
                elif self.particle.pdgid.J == 0.5:
                    self.type = "anti fermion"
                elif self.particle.pdgid.J == 1.5:
                    self.type = "anti fermion"
            else:
                warnings.warn(
                    f"Inferring type from pdgid not implemented for pdgid {self.pdgid} "
                )
                self.type = "line"
            if tmptype is not None and tmptype != "" and self.type != tmptype:
                warnings.warn(
                    f"Type {tmptype} is not consistent with pdgid {self.pdgid}, which is {self.type}. Using {tmptype} now."
                )
                self.type = tmptype

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

    # def with_pdgid(self, pdgid):
    #    self.pdgid = pdgid
    #    self._sync()
    #    return self

    # def with_name(self, name):
    #    self.name = name
    #    self._sync()
    #    return self
