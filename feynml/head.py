import logging
import warnings
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import List, Optional, Union

import cssutils
import smpl_io.io as io
from cssselect import GenericTranslator, SelectorError
from lxml import etree

from feynml.id import Identifiable
from feynml.leg import Leg
from feynml.link import Link
from feynml.meta import Meta as alias_meta
from feynml.propagator import Propagator
from feynml.sheet import SheetHandler
from feynml.styled import CSSSheet, Styled
from feynml.type import get_default_sheet
from feynml.vertex import Vertex
from feynml.xml import XML


@dataclass
class Head(SheetHandler):
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

    def get_sheets(self):
        sheets = []
        sheets += super().get_sheets()
        for k, v in self.get_link_dict().items():
            if k == "stylesheet":
                sheets += [v]
        sheets += [self.style]
        return sheets

    def get_sheet(self):
        return self.style

    def with_sheet(self, sheet):
        self.style = sheet
        return self
