import re
from dataclasses import dataclass

from feynml.vertex import Vertex as FMLVertex


@dataclass
class Vertex:
    i: int
    j: int

    def to_feynml(self) -> FMLVertex:
        return FMLVertex(id="v" + "_" + str(self.i) + "_" + str(self.j))

    def __str__(self):
        """
        Example

        >>> Vertex.from_str(str(Vertex(1,1))) == Vertex(1,1)
        True
        """
        return f"Vertex[{self.i}][{self.j}]"

    @classmethod
    def re(cls):
        return r"\s*Vertex\[(\d+)\]\[(\d+)\]\s*"

    @classmethod
    def n(cls):
        return 2

    @classmethod
    def from_str(cls, vertex: str):
        """
        Example

        >>> str(Vertex.from_str("Vertex[1][1]"))
        'Vertex[1][1]'
        """
        res = re.search(cls.re(), vertex)
        return Vertex(int(res.group(1)), int(res.group(2)))
