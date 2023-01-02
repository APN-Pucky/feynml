import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from particle import Particle
from xsdata.formats.converter import Converter, converter
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


from smpl_doc.doc import deprecated
from smpl_util.util import withify

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)

@withify()
@dataclass
class Labeled:
    label: Optional[str] = field(
        default=None, metadata={"xml_attribute": True, "type": "Attribute"}
    )
    """Label the object"""



CSSString = cssutils.css.CSSStyleDeclaration
CSSSheet = cssutils.css.CSSStyleSheet


class CSSStringConverter(Converter):
    @staticmethod
    def deserialize(value: str, **kwargs) -> CSSString:
        return cssutils.parseStyle(value)

    @staticmethod
    def serialize(value: CSSString, **kwargs) -> str:
        return value.cssText.replace("\n", " ")


class CSSSheetConverter(Converter):
    @staticmethod
    def deserialize(value: str, **kwargs) -> CSSSheet:
        return cssutils.parseString(value)

    @staticmethod
    def serialize(value: CSSSheet, **kwargs) -> str:
        return value.cssText.decode("utf-8")  # .replace("\n", " ")


converter.register_converter(CSSString, CSSStringConverter())
converter.register_converter(CSSSheet, CSSSheetConverter())


@dataclass
class Styled:
    style: CSSString = field(
        default_factory=lambda: cssutils.parseStyle(""),
        metadata={"name": "style", "xml_attribute": True, "type": "Attribute"},
    )
    """CSS style string."""

    clazz: Optional[str] = field(
        default=None,
        metadata={"name": "class", "xml_attribute": True, "type": "Attribute"},
    )
    """CSS class string."""

    def raw_style(self):
        return self.style.cssText.replace("\n", " ")

    def put_style(self, key, value):
        if self.style is not None:
            self.style.setProperty(key, value)
        return self

    def with_style(self, style):
        if style is not None:
            self.style = cssutils.parseStyle(style)
        return self

    def with_class(self, clazz):
        self.clazz = clazz
        return self
