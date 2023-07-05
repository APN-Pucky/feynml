import logging
import os
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional

import smpl_io.io as io

from feynml.feynmandiagram import FeynmanDiagram
from feynml.head import Head
from feynml.id import Identifiable
from feynml.meta import Meta
from feynml.sheet import SheetHandler
from feynml.styled import CSSSheet
from feynml.xml import XML

feynml_version = version("feynml")


@dataclass
class FeynML(SheetHandler, XML):
    class Meta:
        name = "feynml"

    version: Optional[str] = field(
        default=feynml_version, metadata={"name": "version", "type": "Attribute"}
    )

    # post init to check version
    def __post_init__(self):
        if self.version < feynml_version:
            warnings.warn(
                f"FeynML version {self.version} is older than this parser {feynml_version}."
            )
        elif self.version > feynml_version:
            warnings.warn(
                f"FeynML version {self.version} is newer than this parser {feynml_version}."
            )

        self.head.metas.append(Meta("feynml", version("feynml")))
        for d in self.diagrams:
            d.parent_fml = self

    head: Optional[Head] = field(
        default_factory=lambda: Head(),
        metadata={"name": "head", "namespace": "", "type": "Element"},
    )

    diagrams: List[FeynmanDiagram] = field(
        default_factory=list,
        metadata={"name": "diagram", "type": "Element", "namespace": ""},
    )

    def get_root(self):
        return self.head.root

    def with_root(self, root):
        self.head.root = root
        return self

    def get_diagram(self, idd):
        for d in self.diagrams:
            if d.id == idd:
                return d
        return None

    def get_style(self, obj, xml=None):
        if xml is None:
            xml = self
        for d in self.diagrams:
            if isinstance(obj, Identifiable):
                if d.has_id(obj.id):
                    return d.get_style(obj, xml)
        return self.head.get_style(obj, xml)

    def get_sheets(self):
        return self.head.get_sheets()

    def get_sheet(self):
        return self.head.get_sheet()

    def with_sheet(self, sheet):
        self.head.with_sheet(sheet)
        return self

    @classmethod
    def from_xml_file(cls, file: str):
        """Load self from XML file."""
        # get parent directory of file
        r = cls.from_xml(io.read(file))
        # check if file exists
        if os.path.isfile(file):
            r.head.root = os.path.dirname(file) + "/"
        elif file.startswith("http"):
            # remove last file in url
            r.head.root = "/".join(file.split("/")[:-1]) + "/"
        return r
