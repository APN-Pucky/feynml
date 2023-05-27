import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional

import cssutils
from smpl_doc import doc
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from feynml.feynmandiagram import FeynmanDiagram
from feynml.head import Head
from feynml.meta import Meta
from feynml.styled import CSSSheet
from feynml.xml import XML

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


feynml_version = version("feynml")


@dataclass
class FeynML(XML):
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

    def get_diagram(self, idd):
        for d in self.diagrams:
            if d.id == idd:
                return d
        return None

    @doc.append_doc(Head.get_style_property)
    def get_style_property(self, obj, name):
        self.head.style.get_style_property(obj, name, xml=self)
        return self

    @doc.append_doc(Head.get_style)
    def get_style(self, obj):
        self.head.style.get_style(obj, xml=self)
        return self

    @doc.append_doc(Head.add_rule)
    def add_rule(self, rule: str):
        self.head.add_rule(rule)
        return self

    @doc.append_doc(Head.add_rules)
    def add_rules(self, rules: str):
        self.head.add_rules(rules)
        return self

    @doc.append_doc(Head.with_rule)
    def with_rule(self, rule: str):
        self.head.with_rule(rule)
        return self

    @doc.append_doc(Head.with_rules)
    def with_rules(self, rules: str):
        self.head.with_rules(rules)
        return self
