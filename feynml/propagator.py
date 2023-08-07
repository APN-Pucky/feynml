from dataclasses import dataclass

from smpl_util.util import withify

from feynml.connector import Connector
from feynml.line import Line


@withify()
@dataclass
class Propagator(Line, Connector):
    def goes_into(self, vertex):
        """Return True if the propagator goes into the vertex, False otherwise."""
        return self.target == vertex.id

    def goes_out_of(self, vertex):
        """Return True if the propagator goes out of the vertex, False otherwise."""
        return self.target == vertex.id

    def conjugate(self):
        """Return the conjugate of the propagator."""
        tar = self.target
        src = self.source
        return self.with_target(src).with_source(
            tar
        )  # this is inprinciple the same as negating the id
