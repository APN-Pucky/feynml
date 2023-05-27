import logging
from dataclasses import dataclass, field
from typing import Optional

import cssutils
from smpl_doc.doc import deprecated
from xsdata.formats.converter import Converter, converter

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)

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

    @deprecated("0.0.0", "use with_style_property")
    def put_style(self, key, value):
        return self.put_styles(**{key: value})

    @deprecated("0.0.0", "use with_style_properties")
    def put_styles(self, **kwargs):
        if self.style is not None:
            for key, value in kwargs.items():
                self.style.setProperty(key, value)
        return self

    def get_style_property(self, key):
        if self.style is None:
            return None
        if self.style.getProperty(key) is not None:
            return self.style.getProperty(key).value
        else:
            return None

    def with_style_property(self, key, value):
        if self.style is not None:
            self.style.setProperty(key, value)
        return self

    def with_style_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.with_style_property(key, value)
        return self

    def with_style(self, style):
        if style is not None:
            self.style = cssutils.parseStyle(style)
        return self

    def with_class(self, clazz):
        self.clazz = clazz
        return self

    def with_color(self, color):
        return self.with_style_property("color", color)
