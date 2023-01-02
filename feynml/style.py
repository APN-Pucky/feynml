import logging
from dataclasses import dataclass, field
from typing import Optional

import cssutils
from xsdata.formats.converter import Converter, converter

from smpl_util.util import withify
from smpl_doc.doc import deprecated

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

    def get_style(self, key=None):
        if self.style is None:
            return None
        if key is None:
            return self.style
        else:
            return self.style.getProperty(key)

    @deprecated("0.0.0", "use put_styles")
    def put_style(self, key, value):
        return self.put_styles(**{key: value})

    def put_styles(self, **kwargs):
        if self.style is not None:
            for key, value in kwargs.items():
                self.style.setProperty(key, value)
        return self

    def with_style(self, style):
        if style is not None:
            self.style = cssutils.parseStyle(style)
        return self

    def with_class(self, clazz):
        self.clazz = clazz
        return self
