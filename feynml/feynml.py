import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from feynml.feynmandiagram import FeynmanDiagram
from xsdata.formats.converter import Converter, converter
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from smpl_doc.doc import deprecated
from smpl_util.util import withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


feynml_version = "0.0"


@dataclass
class Tool:
    class Meta:
        name = "tool"

    name: Optional[str] = field(default="feynml", metadata={"type": "Element"})
    version: Optional[str] = field(
        default=version("feynml"), metadata={"type": "Element"}
    )


@dataclass
class Meta:
    class Meta:
        name = "meta"

    name: Optional[str] = field(default="", metadata={"type": "Attribute"})
    content: Optional[str] = field(default="", metadata={"type": "Attribute"})


alias_meta = Meta


@dataclass
class Head:
    class Meta:
        name = "head"

    metas: List[alias_meta] = field(
        default_factory=list,
        metadata={"name": "meta", "namespace": ""},
    )
    description: Optional[str] = field(default="", metadata={"type": "Element"})

    style: Optional[str] = field(default="", metadata={"type": "Element"})


@dataclass
class FeynML:
    class Meta:
        name = "feynml"

    version: Optional[str] = field(
        default=feynml_version, metadata={"name": "version", "type": "Attribute"}
    )

    # post init to check version
    def __post_init__(self):
        if self.version < feynml_version:
            warnings.warn("FeynML version is older than this parser.")
        elif self.version > feynml_version:
            warnings.warn("FeynML version is newer than this parser.")

        self.head.metas.append(Meta("feynml", version("feynml")))

    head: Optional[Head] = field(
        default=Head(), metadata={"name": "head", "namespace": "", "type": "Element"}
    )

    diagrams: List[FeynmanDiagram] = field(
        default_factory=list,
        metadata={"name": "diagram", "type": "Element", "namespace": ""},
    )

    def get_diagram(self, idd):
        for d in self.diagrams:
            if d.id == idd:
                return d
        return None

    def to_xml(self) -> str:
        """Return self as XML."""
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(self)

    @classmethod
    def from_xml(cls, xml: str):
        """Load self from XML."""
        parser = XmlParser()
        return parser.from_string(xml, cls)
