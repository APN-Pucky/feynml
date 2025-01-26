from dataclasses import dataclass

from smpl_util.util import withify

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
