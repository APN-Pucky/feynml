import copy
import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Union

import networkx as nx
import cssutils
import numpy as np
import smpl.doc as doc

# from warnings import deprecated
from smpl.doc import deprecated
from smpl.util import withify

from feynmodel.feyn_model import FeynModel

from feynml.connector import Connector
from feynml.head import Head
from feynml.id import Identifiable
from feynml.leg import Leg
from feynml.pdgid import is_pdgid_param, pdgid_param, to_pdgid
from feynml.propagator import Propagator
from feynml.sheet import SheetHandler
from feynml.styled import CSSSheet, Styled
from feynml.vertex import Vertex
from feynml.xml import XML

from .log import debug

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

    def get_vertex_index(self, vertex: Union[Vertex, int]) -> int:
        if isinstance(vertex, Vertex):
            vertex = vertex.id
        for i, v in enumerate(self.vertices):
            if v.id == vertex:
                return i

    def is_isomorphic(self, fd: "FeynmanDiagram"):
        G1 = self.to_graph()
        G2 = fd.to_graph()
        return nx.is_isomorphic(
            G1,
            G2,
            node_match=lambda a1, a2: a1["sense"] == a2["sense"]
            and a1["lid"] == a2["lid"],
        )

    def to_graph(self):
        G = nx.Graph()
        for v in self.vertices:
            G.add_node(v.id, sense=None, lid=None)
        # G.add_node("incoming", sense="incoming", lid=0)
        # G.add_node("outgoing", sense="outgoing", lid=0)
        n_in = 0
        n_out = 0
        for leg in self.legs:
            if leg.is_incoming():
                n_in += 1
                G.add_node(leg.id, sense="incoming", lid=n_in)
                # G.add_edge(l.id, "incoming")
                G.add_edge(leg.id, leg.target)
            else:
                n_out += 1
                G.add_node(leg.id, sense="outgoing", lid=n_out)
                # G.add_edge(l.id, "outgoing")
                G.add_edge(leg.target, leg.id)
        for p in self.propagators:
            G.add_edge(p.source, p.target)
        return G

    def get_number_of_incoming(self):
        return len([leg for leg in self.legs if leg.is_incoming()])

    def get_number_of_outgoing(self):
        return len([leg for leg in self.legs if leg.is_outgoing()])

    def to_matrix(self):
        # Create a square matrix of arrays of size len(vert) + incoming + outgoing category
        li = self.get_number_of_incoming()
        lo = self.get_number_of_outgoing()
        lv = len(self.vertices) + li + lo
        mat = np.frompyfunc(list, 0, 1)(np.empty((lv, lv), dtype=object))
        for p in self.propagators:
            i = self.get_vertex_index(p.source) + li
            j = self.get_vertex_index(p.target) + li
            mat[i, j].append(p.pdgid)

        for i, leg in enumerate([leg for leg in self.legs if leg.is_incoming()]):
            j = self.get_vertex_index(leg.target) + li
            mat[i, j].append(leg.pdgid)
        for j, leg in enumerate([leg for leg in self.legs if leg.is_outgoing()]):
            i = self.get_vertex_index(leg.target) + li
            mat[i, -j - 1].append(leg.pdgid)
        # util data
        # mat[0,0] = [li]
        # mat[-1,-1] = [lo]
        return mat

    @staticmethod
    def from_matrix(matrix, li, lo):
        fd = FeynmanDiagram()
        # li = matrix[0,0][0]
        # lo = matrix[-1,-1][0]
        matrix[0, 0] = []
        matrix[-1, -1] = []
        lv = len(matrix)
        for _ in range(lv - li - lo):
            fd.add(Vertex())
        for i in range(li, lv - lo):
            for j in range(li, lv - lo):
                for id in matrix[i, j]:
                    fd.add(
                        Propagator(pdgid=id).connect(
                            fd.vertices[i - li], fd.vertices[j - li]
                        )
                    )
        # We need to keep the leg order
        for ii in range(li):
            for i in range(li, lv - lo):
                for id in matrix[ii, i]:
                    fd.add(
                        Leg(pdgid=id, sense="incoming").with_target(fd.vertices[i - li])
                    )
        for jj in range(lo):
            for i in range(li, lv - lo):
                for id in matrix[i, -jj - 1]:
                    fd.add(
                        Leg(pdgid=id, sense="outgoing").with_target(fd.vertices[i - li])
                    )
        return fd

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

    def remove(self, *fd_all: List[Union[Propagator, Vertex, Leg]]):
        for a in fd_all:
            if isinstance(a, Propagator):
                self.propagators.remove(a)
            elif isinstance(a, Vertex):
                self.vertices.remove(a)
            elif isinstance(a, Leg):
                self.legs.remove(a)
            else:
                raise Exception("Unknown type: " + str(type(a)) + " " + str(a))
        return self
        return self

    def has_id(self, id):
        for le in [self.propagators, self.vertices, self.legs]:
            for a in le:
                if a.id == id:
                    return True
        return False

    def get(self, lmbda):
        ret = []
        for le in [self.propagators, self.vertices, self.legs]:
            for a in le:
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

    def get_connections(self, vertex: Vertex) -> List[Connector]:
        return (
            [
                p
                for p in self.propagators
                if p.source == vertex.id or p.target == vertex.id
            ]
            + [leg for leg in self.legs if leg.target == vertex.id]
            + [leg for leg in self.legs if leg.id == vertex.id]  # This seems od!
        )

    def get_neighbours(self, vertex):
        return [v for v in self.vertices if self.are_neighbours(vertex, v)] + [
            le for le in self.legs if self.are_neighbours(vertex, le)
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
                le
                for le in self.legs
                if (le.id == vertex1.id and le.target == vertex2.id)
                or (le.id == vertex2.id and le.target == vertex1.id)
            ]
        )

    @deprecated("use remove(propagator) instead")
    def remove_propagator(self, propagator):
        self.propagators.remove(propagator)
        return self

    def insert_tadpole(
        self,
        leg_or_propagator: Union[Leg, Propagator],
        new_propagator: Union[None, int] = None,
    ):
        v1, l1, s1, e1 = self.emission(
            leg_or_propagator=leg_or_propagator, new=new_propagator
        )
        v2, l2, s2, e2 = self.emission(leg_or_propagator=e1, new=new_propagator)
        v = self.merge_vertices(v1, v2)
        p = self.merge_legs(l1, l2)
        return v, p

    def insert_bubble(
        self,
        leg_or_propagator: Union[Leg, Propagator],
        new_propagator1: Union[None, int, Propagator] = None,
        new_propagator2: Union[None, int, Propagator] = None,
    ):
        """
        Adds a bubble loop to a propagator or leg.

        TODO add ascii example diagram here for documentation (also emission() etc.)
        TODO add tests, needs testing
        """
        v1, l1, s1, e1 = self.emission(
            leg_or_propagator=leg_or_propagator, new=new_propagator1
        )
        v2, l2, s2, e2 = self.emission(
            leg_or_propagator=e1, new=new_propagator1, start=new_propagator2
        )
        np = self.merge(l1, l2)
        return v1, v2, np, s2, s1, e2

    def insert_vertex_loop(self, vertex: Vertex, *new_propagators):
        if new_propagators is None or len(new_propagators) == 0:
            new_propagators = [None] * len(self.get_connections(vertex))
        else:
            new_propagators = list(new_propagators)
        # should cover insert_triangle, insert_box, pentagram, ...
        assert len(new_propagators) == len(self.get_connections(vertex))
        new_vertices = [None] * len(new_propagators)
        # Add new vertices
        for i in range(len(new_propagators)):
            new_vertices[i] = Vertex()
            self.add(new_vertices[i])
            if new_propagators is None or isinstance(new_propagators[i], (int, str)):
                new_propagators[i] = Propagator(**pdgid_param(new_propagators[i]))
            self.add(new_propagators[i])

        for i, op in enumerate(self.get_connections(vertex)):
            op.replace_vertex(vertex, new_vertices[i])
            new_propagators[i].with_source(new_vertices[i])
            new_propagators[i - 1].with_target(new_vertices[i])
        self.remove(vertex)
        return new_vertices, new_propagators

    def merge(self, *obj):
        """
        Merges objects together
        """
        if len(obj) == 2 and isinstance(obj[0], Leg) and isinstance(obj[1], Leg):
            return self.merge_legs(obj[0], obj[1])
        else:
            vs = True
            for v in obj:
                if not isinstance(v, Vertex):
                    vs = False
            if vs:
                return self.merge_vertices(obj)

    def merge_legs(self, leg1, leg2):
        """
        Merges two legs to a single propagator.
        """
        assert self.has(leg1) and self.has(leg2)
        new_propagator = Propagator(
            pdgid=leg1.pdgid, source=leg1.target, target=leg2.target
        )  # Maybe we want to copy more properties
        self.add(new_propagator)
        self.remove(leg1)
        self.remove(leg2)
        return new_propagator

    def merge_vertices(self, *vertices, tadpole=False) -> Vertex:
        """
        Merges vertices to a single vertex.
        """
        # We keep the first vertex and its properties
        v0 = vertices[0]
        # We need to remove propagators between two vertices that are replaced (unless it should become a tadpole)
        if not tadpole:
            for p in self.propagators:
                for v1 in vertices:
                    for v2 in vertices:
                        if v1 != v2 and p.connects(v1, v2, directional=True):
                            self.remove(p)
        for v in vertices[1:]:
            for c in self.get_connections(v):
                c.replace_vertex(v, v0)
            self.remove(v)
        return v0

    def decay(self, leg: Leg, *new_legs):
        assert self.has(leg)
        self.add(v := Vertex())
        if leg.is_outgoing():
            self.add(p := Propagator(pdgid=leg.pdgid, source=leg.target, target=v))
        elif leg.is_incoming():
            self.add(p := Propagator(pdgid=leg.pdgid, source=v, target=leg.target))
        else:
            raise Exception("Leg is not incoming or outgoing")
        r_legs = [None] * len(new_legs)
        for i, ls in enumerate(new_legs):
            r_legs[i] = Leg(**pdgid_param(ls), target=v, sense=leg.sense)
            self.add(r_legs[i])
        self.remove(leg)
        return v, p, r_legs

    def emission(
        self,
        leg_or_propagator: Union[Leg, Propagator],
        new: Union[Leg, int, None] = None,
        start=None,
        end=None,
        sense="outgoing",
        position_ratio=0.5,
        inplace=True,
    ):
        """

        Args:
            inplace: If true keeps the original propagator/leg line, else the new intermediate Vertex can be located anywhere.
            position_ratio: The position of the new vertex on the line between the source and target of the propagator/leg.
        """
        x = None
        y = None
        sx = None
        sy = None
        tx = None
        ty = None
        if isinstance(leg_or_propagator, Propagator):
            sx, tx, sy, ty = (
                self.get_vertex(leg_or_propagator.source).x,
                self.get_vertex(leg_or_propagator.target).x,
                self.get_vertex(leg_or_propagator.source).y,
                self.get_vertex(leg_or_propagator.target).y,
            )
        elif isinstance(leg_or_propagator, Leg):
            sx, tx, sy, ty = (
                leg_or_propagator.x,
                self.get_vertex(leg_or_propagator.target).x,
                leg_or_propagator.y,
                self.get_vertex(leg_or_propagator.target).y,
            )
        else:
            raise NotImplementedError("Only Propagator and Leg are supported")
        if sx is not None and sy is not None and tx is not None and ty is not None:
            if inplace:
                x = sx * (1.0 - position_ratio) + tx * (0.0 - position_ratio)
                y = sy * (1.0 - position_ratio) + ty * (0.0 - position_ratio)
        new_vert = Vertex(x=x, y=y)
        self.add(new_vert)
        if new is None or is_pdgid_param(new):
            new = Leg(**pdgid_param(new), sense=sense, target=new_vert)
        elif isinstance(new, Leg):
            new.with_target(new_vert)
        self.add(new)

        startid = leg_or_propagator.pdgid
        if start is not None and is_pdgid_param(start):
            startid = to_pdgid(start)
            start = None

        endid = leg_or_propagator.pdgid
        if end is not None and is_pdgid_param(end):
            endid = to_pdgid(end)
            end = None

        if start is None:
            if isinstance(leg_or_propagator, Leg) and leg_or_propagator.is_outgoing():
                # Continue Leg as Propagator
                start = Propagator(pdgid=startid, source=leg_or_propagator.target)
                self.add(start)
            else:
                start = copy.deepcopy(leg_or_propagator).with_new_id()
                # replace leg_or_propagator with new leg (with out changing the order!)
                if isinstance(leg_or_propagator, Leg):
                    self.legs[self.legs.index(leg_or_propagator)] = start
                elif isinstance(leg_or_propagator, Propagator):
                    if leg_or_propagator in self.propagators:
                        self.propagators.remove(leg_or_propagator)
                    self.add(start)
                else:
                    raise Exception("Unknown leg_or_propagator type")
            start.with_pdgid(**pdgid_param(startid))

        if end is None:
            if isinstance(leg_or_propagator, Leg) and leg_or_propagator.is_incoming():
                # Continue Leg as Propagator
                end = Propagator(pdgid=endid, target=leg_or_propagator.target)
                self.add(end)
            else:
                end = copy.deepcopy(leg_or_propagator).with_new_id()
                if isinstance(leg_or_propagator, Leg):
                    self.legs[self.legs.index(leg_or_propagator)] = end
                elif isinstance(leg_or_propagator, Propagator):
                    if (
                        leg_or_propagator in self.propagators
                    ):  # could already be removed
                        self.propagators.remove(leg_or_propagator)
                    self.add(end)
                else:
                    raise Exception("Unknown leg_or_propagator type")
            end.with_pdgid(**pdgid_param(endid))

        start.with_target(
            new_vert
        )  # It does not matter if we have a Leg or Propagator as start
        if isinstance(end, Propagator):
            end.with_source(new_vert)
        elif isinstance(end, Leg):
            end.with_target(new_vert)
        else:
            assert False  # we should never get here

        return new_vert, new, start, end

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

    def get_externals_size(self):
        return len(self.get_incoming()), len(self.get_outgoing())

    def get_unpositioned_vertices(self):
        return [v for v in self.vertices if v.x is None or v.y is None]

    def get_loose_vertices(self):
        return [v for v in self.vertices if not self.get_connections(v)]

    def get_fermion_factor(self, fd):
        # TODO assert same legs!
        perms = 0
        fl1 = sorted(self.get_fermion_line_ends())
        debug(f"{fl1=}")
        fl2 = sorted(fd.get_fermion_line_ends())
        debug(f"{fl2=}")
        # find fl1[0][0] in fl2
        for fl1i in range(len(fl1)):
            for fl1j in [0, 1]:
                for i in range(len(fl2)):
                    for j in [0, 1]:
                        if i != fl1i and fl2[i][j].id == fl1[fl1i][fl1j].id:
                            perms += 1
                            fl2[fl1i][fl1j], fl2[i][j] = fl2[i][j], fl2[fl1i][fl1j]
        debug(f"{perms=}")
        return (-1) ** perms

    def get_fermion_line_ends(self):
        """ """
        fl = self.get_fermion_lines()
        ret = [[f[0], f[-1]] for f in fl]
        return ret

    def get_fermion_lines(self):
        """ """
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
        # TODO handle case where there are multiple fermions ( i.e. checkc the flow)
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

    def scale_positions(self, scale):
        """Scale the positions of the vertices and legs."""
        for v in self.vertices:
            if v.x is not None:
                v.x *= scale
            if v.y is not None:
                v.y *= scale
        for le in self.legs:
            if le.x is not None:
                le.x *= scale
            if le.y is not None:
                le.y *= scale
        return self

    def is_valid(self, fm: FeynModel, only_vertex=False):
        # first check that the propagator and leg pdgids are also in the model
        if not only_vertex:
            for p in self.propagators:
                if not fm.has_particle(name=p.name, pdg_code=p.pdgid):
                    return False
            for le in self.legs:
                if not fm.has_particle(name=le.name, pdg_code=le.pdgid):
                    return False
        for v in self.vertices:
            if self.find_vertex_in_model(v, fm) is None:
                return False

        return True

    def find_vertex_in_model(self, vertex: Vertex, model: FeynModel):
        """
        Finds the model vertex corresponding to the given FeynmanDiagram vertex

        Note: Sorting is to check for the correct particles in a vertex given they can be in any order and have duplicates
        """
        assert vertex in self.vertices
        cons = np.array(self.get_connections(vertex))
        # debug(f"{cons=}")
        pdg_ids_list = []

        # correct for incoming vs outgoing fermion struct
        for c in cons:
            p = c.pdgid
            if c.is_any_fermion():
                if c.goes_into(vertex):
                    p = -p
            pdg_ids_list += [p]
        pdg_ids_array = np.array(pdg_ids_list)

        sort_mask = np.argsort(pdg_ids_array)
        particles = pdg_ids_array[sort_mask]
        scons = cons[sort_mask]
        # debug(f"{scons=}")
        ret = None
        for v in model.vertices:
            if len(v.particles) != len(particles):
                continue
            model_particle_ids = np.array([p.pdg_code for p in v.particles])
            model_sort_mask = np.argsort(model_particle_ids)
            # By sorting based on the indices we reproduce the order of the particles in the vertex
            inverted_model_sort_mask = np.argsort(model_sort_mask)
            sorted_model_particle_ids = model_particle_ids[model_sort_mask]
            if np.array_equal(sorted_model_particle_ids, particles):
                vc = []
                for i, _ in enumerate(model_particle_ids):
                    con = scons[inverted_model_sort_mask[i]]
                    vc.append(con)
                v.connections = vc
                ret = v
                break

        # Make sure all connections are in the vertex
        if ret is not None:
            for c in cons:
                assert c in ret.connections
        # debug(f"{ret=}")
        return ret

    def copy(self, new_vertex_ids=True, new_leg_ids=True, new_propagator_ids=True):
        copy = self.deepcopy()
        id_map = {}
        # Now generate new ids for all elements
        for v in copy.vertices:
            oid = v.id
            if new_vertex_ids:
                v = v.with_new_id()
            id_map[oid] = v.id
        for le in copy.legs:
            oid = le.id
            if new_leg_ids:
                le = le.with_new_id()
            id_map[oid] = le.id
        for p in copy.propagators:
            oid = p.id
            if new_propagator_ids:
                p = p.with_new_id()
            id_map[oid] = p.id
        # Now replace all ids in the diagram
        for le in copy.legs:
            le.target = id_map[le.target]
        for p in copy.propagators:
            p.source = id_map[p.source]
            p.target = id_map[p.target]
        return copy

    def fastcopy(self):
        # get the matrix representation of the diagram
        mat = self.to_matrix()
        # create a new diagram from the matrix
        return FeynmanDiagram.from_matrix(
            mat, li=self.get_number_of_incoming(), lo=self.get_number_of_outgoing()
        )

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
        """
        Warning: This does not mathematically conjugate the diagram, but only switches directions.
        Differences to the mathematical conjugation are missing complex conjugation of i's and wrong momenta for e.g. 3g-vertex.
        """
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
        self,
        render="tikz",
        show=True,
        file=None,
        auto_position=True,
        auto_position_legs=True,
        deepcopy=True,
        source=False,
        debug=False,
    ):
        try:
            import pyfeyn2.render.all as renderall
            from pyfeyn2.auto import auto_default
        except ImportError as e:
            warnings.warn("Could not import pyfeyn2, cannot render diagram" + str(e))
            return

        # deepcopy to avoid modifying the original diagram
        if deepcopy:
            fd = self.deepcopy()
        else:
            fd = self
        fd = auto_default(
            fd,
            auto_position=auto_position,
            auto_position_legs=auto_position_legs,
            debug=debug,
        )

        renderer_class = renderall.renderer_from_string(render)
        renderer = renderer_class(fd)
        if source:
            print(renderer.get_src())
        renderer.render(show=show, file=file)

    def _ipython_display_(self):
        self.render(show=True)
        return self
