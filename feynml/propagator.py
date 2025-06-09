from dataclasses import dataclass

from smpl.util import withify

from feynml.connector import Connector
from feynml.line import Line
from feynml.vertex import Vertex


@withify()
@dataclass
class Propagator(Line, Connector):
    def conjugate(self):
        """Return the conjugate of the propagator."""
        tar = self.target
        src = self.source
        return self.with_target(src).with_source(
            tar
        )  # this is inprinciple the same as negating the id

    def connects(self, v1: Vertex, v2: Vertex, directional=False):
        """Return True if the propagator connects to the vertex, False otherwise."""
        return (v1.id == self.source and v2.id == self.target) or (
            not directional and v2.id == self.source and v1.id == self.target
        )

    def replace_vertex(self, old_vertex: Vertex, new_vertex: Vertex):
        """Replace the old vertex with the new vertex"""
        hit = False
        if self.source == old_vertex.id:
            hit = True
            self.with_source(new_vertex)
        if self.target == old_vertex.id:
            hit = True
            self.with_target(new_vertex)
        if not hit:
            raise ValueError("Vertex not found in propagator")
        return self
