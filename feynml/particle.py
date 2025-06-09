from enum import Enum
from typing import Optional
from dataclasses import dataclass, field
import warnings

from smpl.util import withify

from feynmodel.feyn_model import FeynModel

from feynml.particles import get_either_particle, get_particle_and_name_from_pdgid


class ParticleType(Enum):
    """Enum for particle types"""

    FERMION = "fermion"
    ANTI_FERMION = "anti fermion"
    PHOTON = "photon"
    GLUON = "gluon"
    BOSON = "boson"
    HIGGS = "higgs"
    BARYON = "baryon"
    ANTI_BARYON = "anti baryon"
    MESON = "meson"
    GAUGINO = "gaugino"
    SLEPTON = "slepton"
    SQUARK = "squark"
    GLUINO = "gluino"
    NONE = "line"


@withify()
@dataclass
class Particle:
    pdgid: Optional[int] = field(
        default=None, metadata={"name": "pdgid", "namespace": "", "type": "Attribute"}
    )
    """PDGID of the particle"""
    name: Optional[str] = field(default=None, metadata={"type": "Element"})
    """Name of the particle"""
    mass: Optional[float] = field(default=None, metadata={"type": "Element"})
    """Mass of the particle"""
    charge: Optional[float] = field(default=None, metadata={"type": "Element"})
    """Charge of the particle"""
    spin: Optional[int] = field(default=None, metadata={"type": "Element"})
    """Spin of the particle"""
    texname: Optional[str] = field(default=None, metadata={"type": "Element"})

    def get_type(self) -> str:
        return self.get_particletype().value

    def get_particletype(self) -> ParticleType:
        if self.pdgid in range(1, 7):
            return ParticleType.FERMION
        elif -self.pdgid in range(1, 7):
            return ParticleType.ANTI_FERMION
        elif self.pdgid == 22:
            return ParticleType.PHOTON
        elif self.pdgid == 21:
            return ParticleType.GLUON
        elif self.pdgid in range(11, 19):
            return ParticleType.FERMION
        elif -self.pdgid in range(11, 19):
            return ParticleType.ANTI_FERMION
        elif abs(self.pdgid) == 24:
            return ParticleType.BOSON
        elif self.pdgid == 23:
            return ParticleType.BOSON
        elif self.pdgid == 25:
            return ParticleType.HIGGS
        elif self.pdgid == 2212:  # proton
            return ParticleType.BARYON
        elif self.pdgid == 2112:  # neutron
            return ParticleType.BARYON
        elif self.pdgid == -2212:  # anti proton
            return ParticleType.ANTI_BARYON
        elif self.pdgid == 111:  # pion
            return ParticleType.MESON
        elif abs(self.pdgid) == 211:  # pion
            return ParticleType.MESON
        elif abs(self.pdgid) in [
            1000022,
            1000023,
            1000024,
            1000025,
            1000035,
            1000037,
        ]:
            return ParticleType.GAUGINO
        elif abs(self.pdgid) in [
            1000011,
            1000012,
            1000013,
            1000014,
            1000015,
            1000016,
        ]:
            return ParticleType.SLEPTON
        elif abs(self.pdgid) in [
            2000011,
            2000012,
            2000013,
            2000014,
            2000015,
            2000016,
        ]:
            return ParticleType.SLEPTON
        elif abs(self.pdgid) in [
            1000001,
            1000002,
            1000003,
            1000004,
            1000005,
            1000006,
        ]:
            return ParticleType.SQUARK
        elif abs(self.pdgid) in [
            2000001,
            2000002,
            2000003,
            2000004,
            2000005,
            2000006,
        ]:
            return ParticleType.SQUARK
        elif abs(self.pdgid) in [1000021]:
            return ParticleType.GLUNINO
        elif abs(self.pdgid) > 9000000:
            return ParticleType.NONE
        elif self.pdgid < 1000000 and self.pdgid > 100:
            if self.spin == 1:
                return ParticleType.NONE
            elif self.spin == 3:
                return ParticleType.NONE
            elif self.spin == 2:
                return ParticleType.FERMION
            elif self.spin == 4:
                return ParticleType.FERMION
        elif self.pdgid > -1000000 and self.pdgid < -100:
            if self.spin == 1:
                return ParticleType.NONE
            elif self.spin == 3:
                return ParticleType.NONE
            elif self.spin == 2:
                return ParticleType.ANTI_FERMION
            elif self.spin == 4:
                return ParticleType.ANTI_FERMION
        else:
            warnings.warn(
                f"Inferring type from pdgid not implemented for pdgid {self.pdgid} in {self}"
            )
            return ParticleType.NONE

    # creator function static
    @staticmethod
    def fromfeynmodel(pdgid: int, fm: FeynModel) -> "Particle":
        """Create a Particle from a FeynModel"""
        p = fm.get_particle(pdg_code=pdgid)
        return Particle(
            pdgid=pdgid,
            name=p.name,
            mass=p.mass,
            charge=p.charge,
            spin=p.spin,
            texname=p.texname,
        )

    @staticmethod
    def frompdg(pdgid: int) -> "Particle":
        """Create a Particle from a PDG"""
        particle, name = get_particle_and_name_from_pdgid(pdgid)
        theid = pdgid
        return Particle(
            pdgid=theid,
            name=name,
            mass=particle.mass,
            charge=particle.pdgid.charge,
            spin=round(particle.pdgid.J * 2 + 1)
            if theid != 25
            else 0,  # particle bug https://github.com/scikit-hep/particle/pull/673
            texname=particle.latex_name,
        )

    @staticmethod
    def fromname(name: str) -> "Particle":
        """Create a Particle from a name"""
        particle = get_either_particle(
            programmatic_name=name,
            name=name,
            evtgen_name=name,
            html_name=name,
            latex_name=name,
        )
        theid = int(particle.pdgid)
        return Particle(
            pdgid=theid,
            name=name,
            mass=particle.mass,
            charge=particle.pdgid.charge,
            spin=round(particle.pdgid.J * 2 + 1)
            if theid != 25
            else 0,  # particle bug https://github.com/scikit-hep/particle/pull/673
            texname=particle.latex_name,
        )
