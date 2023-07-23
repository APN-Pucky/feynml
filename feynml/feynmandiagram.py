import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Union

import cssutils
import numpy as np
import smpl_doc.doc as doc
from cssselect import GenericTranslator, SelectorError
from lxml import etree
from smpl_util.util import withify

from feynml.head import Head
from feynml.id import Identifiable
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.sheet import SheetHandler
from feynml.styled import CSSSheet, Styled
from feynml.vertex import Vertex
from feynml.xml import XML

from .type import get_default_sheet

# We don't want to see the cssutils warnings, since we have custom properties
cssutils.log.setLevel(logging.CRITICAL)


@withify()
@dataclass
class FeynmanDiagram(SheetHandler, XML, Styled, Identifiable):
    class Meta:
        name = "diagram"

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

    parent_fml = None

    sheet: CSSSheet = field(
        default_factory=lambda: cssutils.parseString(""),
        metadata={
            "name": "sheet",
            "xml_attribute": True,
            "type": "Attribute",
            "namespace": "",
        },
    )

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

    def has_id(self, id):
        for l in [self.propagators, self.vertices, self.legs]:
            for a in l:
                if a.id == id:
                    return True
        return False

    def get(self, lmbda):
        ret = []
        for l in [self.propagators, self.vertices, self.legs]:
            for a in l:
                try:
                    if lmbda(a):
                        ret.append(a)
                except Exception:
                    pass
        return ret

    def get_point(self, idd):
        for v in self.vertices:
            if v.id == idd:
                return v
        for leg in self.legs:
            if leg.id == idd:
                return leg
        return None

    def get_vertex(self, idd):
        for v in self.vertices:
            if v.id == idd:
                return v
        return None

    def get_leg(self, idd):
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
        """
        Get the bounding box of the diagram, i.e. the smallest rectangle that contains all vertices and legs.

        Returns:
            (min_x, min_y, max_x, max_y): The bounding box
        """
        min_x = np.inf
        min_y = np.inf
        max_x = -np.inf
        max_y = -np.inf
        for v in [*self.vertices, *self.legs]:
            if v.x is None or v.y is None:
                warnings.warn(
                    f"Vertex or leg {v}"
                    + v.id
                    + " has no position, skipping it in bounding box"
                )
                continue
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)
        return min_x, min_y, max_x, max_y

    @doc.append_doc(Head.get_style)
    def get_style(self, obj, xml: XML = None) -> cssutils.css.CSSStyleDeclaration:
        # as of now, we don't have any xpath/styles from the fml itself
        # if self.parent_fml is not None:
        #    return super().get_style(obj, self.parent_fml)
        if xml is not None:
            return super().get_style(obj, xml)
        else:
            return super().get_style(obj, self)

    def get_sheets(self):
        if self.parent_fml is not None:
            return self.parent_fml.get_sheets() + [self.sheet]
        else:
            return super().get_sheets() + [self.sheet]

    def get_sheet(self):
        return self.sheet

    def with_sheet(self, sheet):
        self.sheet = sheet
        return self

    def has_vertex(self, vertex):
        return vertex in self.vertices

    def has_vertex_id(self, vertexid):
        return self.get_vertex(vertexid) is not None

    def has_leg(self, leg):
        return leg in self.legs

    def has_propagator(self, propagator):
        return propagator in self.propagators

    def has(self, obj):
        return self.has_vertex(obj) or self.has_leg(obj) or self.has_propagator(obj)
