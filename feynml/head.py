import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree

from feynml.id import Identifiable
from feynml.leg import Leg
from feynml.link import Link
from feynml.meta import Meta as alias_meta
from feynml.propagator import Propagator
from feynml.styled import CSSSheet, Styled
from feynml.types import get_default_sheet
from feynml.vertex import Vertex
from feynml.xml import XML


@dataclass
class Head:
    class Meta:
        name = "head"

    metas: List[alias_meta] = field(
        default_factory=list,
        metadata={"name": "meta", "namespace": ""},
    )
    links: List[Link] = field(
        default_factory=list,
        metadata={"name": "link", "namespace": ""},
    )
    cached_links = {}
    title: Optional[str] = field(default=None, metadata={"type": "Element"})

    # description: Optional[str] = field(default="", metadata={"type": "Element"})

    # style: Optional[str] = field(default="", metadata={"type": "Element"})
    style: CSSSheet = field(
        default_factory=lambda: cssutils.parseString(""),
        metadata={
            "name": "style",
            "type": "Element",
        },
    )

    def get_link_dict(self, cached=True, cache=True):
        """
        Return a dictionary of resolved links.

        If cached is True, then the cached resolved links are returned.
        """
        ret = {}
        for m in self.links:
            if m.ref in self.cached_links and cached:
                ret[m.ref] = self.cached_links[m.ref]
            else:
                ret[m.ref] = io.read(m.href)
                if cache:
                    self.cached_links[m.ref] = ret[m.ref]
        return ret

    def get_meta_dict(self):
        """
        Return a dictionary of meta tags.
        """
        return {m.name: m.content for m in self.metas}

    def get_style_property(self, obj, property_name, xml: XML = None):
        """
        Get a style property of an object.
        """
        style = self.get_style(obj, xml=xml)
        p = style.getProperty(property_name)
        if p is None:
            return None
        else:
            return p.value

    def get_style(self, obj, xml: XML = None) -> cssutils.css.CSSStyleDeclaration:
        """
        Get the style of an object.

        This is prefered over accessing the style attribute directly, since it includes class and pdgid definitions.
        """
        # selectorText is string
        css = []
        # global style
        if isinstance(obj, Identifiable):
            css += [self._get_obj_style(obj, xml=xml)]
        if isinstance(obj, Styled):
            # specific attribute style
            css += [obj.style]
        return cssutils.css.CSSStyleDeclaration(
            cssText=";".join([c.cssText for c in css])
        )

    def _get_obj_style(
        self, obj: Identifiable, xml: XML = None
    ) -> cssutils.css.CSSStyleDeclaration:
        if xml is not None:
            document = etree.XML(xml.to_xml().encode("ascii"))
        else:
            warnings.warn("No XML provided, using empty XML")
            document = etree.XML("")

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
        for k, v in self.get_link_dict().items():
            if k == "stylesheet":
                sheets += [v]
        if self.external_sheet:
            sheets += [self.external_sheet]
        sheets += [self.sheet]
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

    def add_rule(self, rule: str):
        """
        Add a rule to the style.
        """
        self.style.add(rule)
        return self

    def add_rules(self, rules: str):
        """
        Add rules to the style.
        """
        self.style = cssutils.parseString(
            self.style.cssText.decode("utf-8") + "\n" + rules
        )
        return self

    def with_rule(self, rule: str):
        """
        Replace rules of the style.
        """
        return self.with_rules(rule)

    def with_rules(self, rules: str):
        """
        Replace rules of the style.
        """
        self.style = cssutils.parseString(rules)
        return self
