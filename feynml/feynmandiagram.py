import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from smpl_util.util import withify
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from feynml.id import Identifiable
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.styled import CSSSheet, Styled
from feynml.vertex import Vertex

from .types import get_default_sheet

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


@withify()
@dataclass
class FeynmanDiagram(Styled, Identifiable):
    class Meta:
        name = "diagram"

    default_style: Optional[bool] = field(
        default=True,
        metadata={"name": "default_style", "xml_attribute": True, "type": "Attribute"},
    )

    propagators: List[Propagator] = field(
        default_factory=list,
        metadata={"name": "propagator", "type": "Element", "namespace": ""},
    )
    vertices: List[Vertex] = field(
        default_factory=list,
        metadata={"name": "vertex", "type": "Element", "namespace": ""},
    )
    legs: List[Leg] = field(
        default_factory=list,
        metadata={"name": "leg", "type": "Element", "namespace": ""},
    )

    sheet: CSSSheet = field(
        default_factory=lambda: cssutils.parseString(""),
        metadata={
            "name": "style",
            "xml_attribute": True,
            "type": "Attribute",
            "namespace": "",
        },
    )
    # external_sheet is used to store the sheet from the file
    # so that we can use it to update the sheet.
    # It is not saved to the fml file.
    external_sheet: CSSSheet = None

    def add(self, *fd_all: List[Union[Propagator, Vertex, Leg]]):
        for a in fd_all:
            if isinstance(a, Propagator):
                self.propagators.append(a)
            elif isinstance(a, Vertex):
                self.vertices.append(a)
            elif isinstance(a, Leg):
                self.legs.append(a)
            else:
                raise Exception("Unknown type: " + str(type(a)) + " " + str(a))
        return self

    def get_vertex(self, idd):
        for v in self.vertices:
            if v.id == idd:
                return v
        for leg in self.legs:
            if leg.id == idd:
                return leg
        return None

    def get_connections(self, vertex):
        return [
            p
            for p in self.propagators
            if p.source == vertex.id or p.target == vertex.id
        ] + [leg for leg in self.legs if leg.target == vertex.id]

    def remove_propagator(self, propagator):
        self.propagators.remove(propagator)
        return self

    def get_bounding_box(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for v in self.vertices:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)
        for leg in self.legs:
            min_x = min(min_x, leg.x)
            min_y = min(min_y, leg.y)
            max_x = max(max_x, leg.x)
            max_y = max(max_y, leg.y)
        return min_x, min_y, max_x, max_y

    def add_rule(self, rule: str):
        self.sheet.add(rule)
        return self

    def add_rules(self, rules: str):
        self.sheet = cssutils.parseString(
            self.sheet.cssText.decode("utf-8") + "\n" + rules
        )
        return self

    def with_rule(self, rule: str):
        return self.with_rules(rule)

    def with_rules(self, rules: str):
        self.sheet = cssutils.parseString(rules)
        return self

    def get_style_property(self, obj, property_name):
        style = self.get_style(obj)
        p = style.getProperty(property_name)
        if p is None:
            return None
        else:
            return p.value

    def get_style(self, obj) -> cssutils.css.CSSStyleDeclaration:
        """Get the style of an object.

        This is prefered over accessing the style attribute directly, sicne it includes class and pdgid definitions.
        """
        # selectorText is string
        css = []
        # global style
        if isinstance(obj, Identifiable):
            css += [self._get_obj_style(obj)]
        if isinstance(obj, Styled):
            # specific attribute style
            css += [obj.style]
        return cssutils.css.CSSStyleDeclaration(
            cssText=";".join([c.cssText for c in css])
        )

    def _get_obj_style(self, obj: Identifiable) -> cssutils.css.CSSStyleDeclaration:
        document = etree.XML(self.to_xml().encode("ascii"))

        def lambdaselector(s, obj=obj, document=document):
            try:
                expression = GenericTranslator().css_to_xpath(s)
            except SelectorError:
                warnings.warn("Invalid selector: " + s)
                return False
            return obj.id in [e.get("id") for e in document.xpath(expression)]

        return self._get_style(lambdaselector)

    def _get_style(self, lambdaselector) -> cssutils.css.CSSStyleDeclaration:

        ret = []
        sheets = []
        if self.default_style:
            sheets += [get_default_sheet()]
        sheets += [self.sheet]
        if self.external_sheet:
            sheets += [self.external_sheet]
        for sheet in sheets:
            idd = []
            cls = []
            rest = []
            glob = []
            for rule in sheet:
                if rule.type == rule.STYLE_RULE:
                    s = rule.selectorText
                    if lambdaselector(s):
                        if s.startswith("#"):
                            idd.append(rule)
                        elif s.startswith("["):
                            rest.append(rule)
                        elif s.startswith(":"):
                            rest.append(rule)
                        elif s.startswith("*"):
                            glob.append(rule)
                        elif "." in s:
                            cls.append(rule)
                        else:
                            rest.append(rule)
            ret += reversed(idd + cls + rest + glob)
        # sort rules by priority
        return cssutils.css.CSSStyleDeclaration(
            cssText=";".join([r.style.cssText for r in ret])
        )

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
