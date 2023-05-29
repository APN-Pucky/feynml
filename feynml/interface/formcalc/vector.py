import re
from dataclasses import dataclass
from typing import Optional

from feynml.interface.formcalc.particle import Particle
from feynml.interface.formcalc.sequenceform import SequenceForm


@dataclass
class Vector(Particle):
    i: int
    sequenceform: Optional[SequenceForm] = None

    def get_pdgid(self) -> int:
        if self.i == 1:
            return 22
        if self.i == 2:
            return 23  # TODO check
        if self.i == 3:
            return 24  # TODO check
        if self.i == 5:
            return 21
        return 0

    def __str__(self):
        if self.sequenceform is not None:
            return f"V[{self.i}, {{{self.sequenceform}}}]"
        else:
            return f"V[{self.i}]"

    @classmethod
    def re(cls):
        return r"\s*V\[(\d+)(,\s*{(" + SequenceForm.re() + r")})?\]\s*"
        # return r"\s*V\[(\d+)\]\s*"

    @classmethod
    def n(cls):
        return 1 + 1 + 1 + SequenceForm.n()

    @classmethod
    def from_str(cls, vector: str):
        """
        Example

        >>> str(Vector.from_str('V[1, {SequenceForm[\"Col\", 1]}]'))
        'V[1, {SequenceForm["Col", 1]}]'
        >>> str(Vector.from_str('V[1]'))
        'V[1]'
        """
        res = re.search(cls.re(), vector)
        if res.group(3) is not None:
            return Vector(int(res.group(1)), SequenceForm.from_str(res.group(3)))
        else:
            return Vector(int(res.group(1)))
