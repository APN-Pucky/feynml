import copy
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
        return (
            [
                p
                for p in self.propagators
                if p.source == vertex.id or p.target == vertex.id
            ]
            + [leg for leg in self.legs if leg.target == vertex.id]
            + [leg for leg in self.legs if leg.id == vertex.id]
        )

    def get_neighbours(self, vertex):
        return [v for v in self.vertices if self.are_neighbours(vertex, v)] + [
            l for l in self.legs if self.are_neighbours(vertex, l)
        ]

    def are_neighbours(self, vertex1, vertex2):
        return any(
            [
                p
                for p in self.propagators
                if (p.source == vertex1.id and p.target == vertex2.id)
                or (p.source == vertex2.id and p.target == vertex1.id)
            ]
        ) or any(
            [
                l
                for l in self.legs
                if (l.id == vertex1.id and l.target == vertex2.id)
                or (l.id == vertex2.id and l.target == vertex1.id)
            ]
        )

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

    def get_incoming(self):
        return [leg for leg in self.legs if leg.is_incoming()]

    def get_outgoing(self):
        return [leg for leg in self.legs if leg.is_outgoing()]

    def get_unpositioned_vertices(self):
        return [v for v in self.vertices if v.x is None or v.y is None]

    def get_loose_vertices(self):
        return [v for v in self.vertices if not self.get_connections(v)]

    def get_fermion_factor(self, fd):
        # TODO assert same legs!
        perms = 0
        fl1 = sorted(self.get_fermion_line_ends())
        fl2 = sorted(fd.get_fermion_line_ends())
        # find fl1[0][0] in fl2
        for fl1i in range(len(fl1)):
            for fl1j in [0, 1]:
                for i in range(len(fl2)):
                    for j in [0, 1]:
                        if i != fl1i and fl2[i][j].id == fl1[fl1i][fl1j].id:
                            perms += 1
                            fl2[fl1i][fl1j], fl2[i][j] = fl2[i][j], fl2[fl1i][fl1j]
        # print(perms)
        return (-1) ** perms

    def get_fermion_line_ends(self):
        fl = self.get_fermion_lines()
        ret = [[f[0], f[-1]] for f in fl]
        return ret

    def get_fermion_lines(self):
        ret = []
        for leg in self.legs:
            if leg.is_outgoing() and leg.is_fermion():
                ret.append(self.follow_anti_fermion_line(leg))
            if leg.is_incoming() and leg.is_anti_fermion():
                ret.append(self.follow_anti_fermion_line(leg))
        # assert elements in total list are unique, every element can only be in one fermion line
        # assert len([y for r in ret for y in r]) == len(set([y for r in ret for y in r]))
        return ret

    def follow_anti_fermion_line(self, leg):
        # assert leg.is_anti_fermion()
        chain = []
        chain.append(leg)
        v = None
        if isinstance(leg, Leg):
            if leg.is_incoming() and leg.is_fermion():
                return chain
            if leg.is_outgoing() and leg.is_fermion():
                v = self.get_vertex(leg.target)
            if leg.is_incoming() and leg.is_anti_fermion():
                v = self.get_vertex(leg.target)
            if leg.is_outgoing() and leg.is_anti_fermion():
                return chain
        elif isinstance(leg, Propagator):
            if leg.is_fermion():
                v = self.get_vertex(leg.source)
            elif leg.is_anti_fermion():
                v = self.get_vertex(leg.target)
            else:
                raise Exception(
                    "Propagator not connected to leg"
                )  # when hit change to check full chain
        else:
            raise Exception("Unknown leg type")

        chain.append(v)
        # TODO handle case where there are mutliple fermions ( i.e. checkc the flow)
        cs = self.get_connections(v)
        for c in cs:
            if c != leg and c.is_any_fermion():
                return chain + self.follow_anti_fermion_line(c)
            if c != leg and c in chain:
                return chain
        # TODO needs to handle loops and stop if already in chain
        raise Exception("Could not find fermion line end")

    def has_pdgid(self, pdgid):
        for p in [*self.propagators, *self.legs]:
            if p.pdgid == pdgid:
                return True
        return False

    def get_leg_by_pdgid(self, pdgid):
        for leg in self.legs:
            if leg.pdgid == pdgid:
                return leg
        return None

    def copy(self, new_vertex_ids=True, new_leg_ids=True, new_propagator_ids=True):
        copy = self.deepcopy()
        id_map = {}
        # Now generate new ids for all elements
        for v in copy.vertices:
            oid = v.id
            if new_vertex_ids:
                v = v.with_new_id()
            id_map[oid] = v.id
        for l in copy.legs:
            oid = l.id
            if new_leg_ids:
                l = l.with_new_id()
            id_map[oid] = l.id
        for p in copy.propagators:
            oid = p.id
            if new_propagator_ids:
                p = p.with_new_id()
            id_map[oid] = p.id
        # Now replace all ids in the diagram
        for l in copy.legs:
            l.target = id_map[l.target]
        for p in copy.propagators:
            p.source = id_map[p.source]
            p.target = id_map[p.target]
        return copy

    def deepcopy(self):
        savesheets = self.sheet
        self.sheet = None
        ret = copy.deepcopy(self)
        self.sheet = savesheets
        ret.sheet = cssutils.parseString(self.sheet.cssText)
        return ret

    def conjugated(
        self, new_vertex_ids=True, new_leg_ids=True, new_propagator_ids=True
    ):
        return self.copy(
            new_vertex_ids=new_vertex_ids,
            new_leg_ids=new_leg_ids,
            new_propagator_ids=new_propagator_ids,
        )._conjugate()

    def _conjugate(self):
        for leg in self.legs:
            leg.conjugate()
        for propagator in self.propagators:
            propagator.conjugate()
        return self

    def render(
        self, render="tikz", show=True, file=None, auto_position=True, deepcopy=True
    ):
        import pyfeyn2.render.all as renderall
        from pyfeyn2.auto.bend import auto_bend
        from pyfeyn2.auto.label import auto_label
        from pyfeyn2.auto.position import (
            auto_align_legs,
            auto_vdw,
            feynman_adjust_points,
        )

        # deepcopy to avoid modifying the original diagram
        if deepcopy:
            fd = self.deepcopy()
        else:
            fd = self
        if auto_position:
            # remove all unpositioned vertices
            fd = auto_align_legs(
                fd,
                incoming=[(0, i) for i in np.linspace(0, 10, len(self.get_incoming()))],
                outgoing=[
                    (10, i) for i in np.linspace(0, 10, len(self.get_outgoing()))
                ],
            )
            p = [v for v in fd.vertices if v.x is None or v.y is None]
            if len(p) > 0:
                fd = auto_vdw(fd, points=p)
        auto_label([*fd.propagators, *fd.legs])
        fd = auto_bend(fd)
        renderer = renderall.renderer_from_string(render)
        renderer(fd).render(show=show, file=file)

    def _ipython_display_(self):
        try:
            self.render(show=True)
        except ImportError as e:
            warnings.warn("Could not import pyfeyn2, cannot render diagram")
            pass
        return self
