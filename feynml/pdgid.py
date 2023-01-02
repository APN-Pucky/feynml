import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from feynml.id import Identifiable
from feynml.style import Bending, Labeled, Styled, Texted

from particles import get_either_particle
from types import get_default_sheet
from smpl_doc.doc import deprecated
from smpl_util.util import withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


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
            else:
                warnings.warn(
                    f"Inferring type from pdgid not implemented for pdgid {self.pdgid} "
                )
                self.type = "line"
            if tmptype is not None and self.type != tmptype:
                warnings.warn(
                    f"Type {tmptype} is not consistent with pdgid {self.pdgid}, using {self.type} instead. Using {tmptype} now."
                )
                self.type = tmptype

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

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_pdgig(self, *args, **kwargs):
        return self.with_pdgid(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_type(self, *args, **kwargs):
        return self.with_type(*args, **kwargs)

    @deprecated(version="2.0.7.1", reason="Use with...().")
    def set_name(self, *args, **kwargs):
        return self.with_name(*args, **kwargs)
