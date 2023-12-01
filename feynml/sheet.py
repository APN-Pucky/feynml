import logging
import warnings
from typing import List

import cssutils
from cssselect import GenericTranslator, SelectorError
from lxml import etree

from feynml.id import Identifiable
from feynml.styled import Styled
from feynml.xml import XML

cssutils.log.setLevel(logging.CRITICAL)

default_sheet = cssutils.parseString(
    """
        /*************************************************************************/
        /* Diagram */
        /*************************************************************************/

        diagram {
            direction : right;
            layout : neato;
        }

        /*************************************************************************/
        /* Vertex */
        /*************************************************************************/

        [shape=dot] {
            symbol : dot;
        }
        [shape=empty] {
            symbol : empty;
        }
        [shape=blob] {
            symbol : blob;
        }
        [shape=star] {
            symbol : star;
        }

        [shape=square] {
            symbol : square;
        }
        [shape=triangle] {
            symbol : triangle;
        }
        [shape=diamond] {
            symbol : diamond;
        }
        [shape=pentagon] {
            symbol : pentagon;
        }
        [shape=hexagon] {
            symbol : hexagon;
        }

        [shape=triagram] {
            symbol : triagram;
        }
        [shape=tetragram] {
            symbol : tetragram;
        }
        [shape=pentagram] {
            symbol : pentagram;
        }

        [shape=cross] {
            symbol : cross;
        }
        [shape=triacross] {
            symbol : triacross;
        }
        [shape=pentacross] {
            symbol : pentacross;
        }
        [shape=hexacross] {
            symbol : pentacross;
        }
        
        

        /*************************************************************************/
        /* Propagator */
        /*************************************************************************/

        /* General */
        [type=meson] {
            line: meson;
            arrow-sense: 0;
            double-distance: 3;
        }
        [type=baryon] {
            line: baryon;
            arrow-sense: 1;
            double-distance: 3;
        }
        [type="anti baryon"] {
            line: anti baryon;
            arrow-sense: -1;
            double-distance: 3;
        }
        [type=fermion] {
            line: fermion;
            arrow-sense: 1;
        }
        [type="anti fermion"] {
            line: anti fermion;
            arrow-sense: -1;
        }
        [type=boson] {
            line: boson;
            arrow-sense: 0;
        }
        [type=vector] {
            line: vector;
            arrow-sense: 0;
        }
        [type=scalar] {
            line: scalar;
            arrow-sense: 0;
        }
        [type=majorana] {
            line: majorana;
        }
        [type=anti majorana] {
            line: anti majorana;
        }
        /* SM */
        [type=photon] {
            line: photon;
            arrow-sense: 0;
        }
        [type=higgs] {
            line: higgs;
            arrow-sense: 0;
        }
        [type=gluon] {
            line: gluon;
            arrow-sense: 0;
            xamp : 0.025;
            yamp : 0.035;
            nloops : 7;
        }
        [type=ghost] {
            line: ghost;
            arrow-sense: 1;
        }
        [type=anti ghost] {
            line: ghost;
            arrow-sense: -1;
        }
        /* BSM */
        [type=graviton] {
            line: graviton;
            arrow-sense: 0;
        }
        [type=gluino] {
            line: gluino;
            arrow-sense: 0;
            xamp : 0.025;
            yamp : 0.035;
            nloops : 7;
        }
        [type=squark]  {
            line: squark;
            arrow-sense: 1;
        }
        [type=slepton] {
            line: slepton;
            arrow-sense: 1;
        }
        [type=anti squark]  {
            line: anti squark;
            arrow-sense: -1;
        }
        [type=anti slepton] {
            line: anti slepton;
            arrow-sense: -1;
        }
        [type=gaugino] {
            line: gaugino;
            arrow-sense: 0;
        }
        [type=neutralino] {
            line: neutralino;
            arrow-sense: 0;
        }
        [type=chargino] {
            line: chargino;
            arrow-sense: 0;
        }
        [type=higgsino] {
            line: higgsino;
            arrow-sense: 0;
        }
        [type=gravitino] {
            line: gravitino;
            arrow-sense: 0;
        }
        /* util */
        [type=phantom] {
            line: phantom;
            arrow-sense: 0;
        }
        [type=line] {
            line: line;
            arrow-sense: 0;
        }
        """
)


def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return default_sheet


class SheetHandler:
    """Sheet class."""

    default_sheet: cssutils.css.CSSStyleSheet = get_default_sheet()

    def get_sheets(self) -> List[cssutils.css.CSSStyleSheet]:
        """Return the sheet."""
        return [self.default_sheet]

    def get_sheet(self) -> cssutils.css.CSSStyleSheet:
        """Return the sheet."""
        return self.default_sheet

    def with_sheet(self, sheet):
        """Return the object with the sheet."""
        self.default_sheet = sheet
        return self

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

    def get_style_property(self, obj, property_name, xml: XML = None) -> str:
        """
        Get a style property of an object.
        """
        style = self.get_style(obj, xml=xml)
        p = style.getProperty(property_name)
        if p is None:
            return None
        else:
            return p.value

    def _get_obj_style(
        self, obj: Identifiable, xml: XML = None
    ) -> cssutils.css.CSSStyleDeclaration:
        if xml is not None:
            document = etree.XML(xml.to_xml().encode("ascii"))
        else:
            warnings.warn("No XML provided, using empty XML")
            document = etree.XML("<feynml></feynml>")

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
        sheets = self.get_sheets()
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
        self.get_sheet().add(rule)
        return self

    def add_rules(self, rules: str):
        """
        Add rules to the style.
        """
        self.with_sheet(
            cssutils.parseString(
                self.get_sheet().cssText.decode("utf-8") + "\n" + rules
            )
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
        self.with_sheet(cssutils.parseString(rules))
        return self
