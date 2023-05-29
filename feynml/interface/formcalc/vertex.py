import re
from dataclasses import dataclass


@dataclass
class Vertex:
    i: int
    j: int

    def __str__(self):
        """
        Example

        >>> Vertex.from_str(str(Vertex(1,1))) == Vertex(1,1)
        True
        """
        return f"Vertex[{self.i}][{self.j}]"

    @classmethod
    def re():
        return r"\s*Vertex\[(\d+)\]\[(\d+)\]\s*"

    @classmethod
    def n():
        return 2

    @classmethod
    def from_str(cls, vertex: str):
        """
        Example

        >>> Vertex.from_str("Vertex[1][1]")
        Vertex(1,1)
        """
        res = re.search(cls.re(), vertex)
        return Vertex(int(res.group(1)), int(res.group(2)))
