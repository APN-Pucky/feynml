import re
from dataclasses import dataclass

from feynml.interface.formcalc.sequenceform import SequenceForm


@dataclass
class Fermion:
    sign: int
    type: int
    i: int
    sequenceform: SequenceForm

    def __str__(self):
        return f"{'-' if self.sign < 0 else ''}F[{self.type}, {{{self.i}, {self.sequenceform}}}]"

    @classmethod
    def re(cls):
        return r"\s*(-?F)\[(\d+),\s*\{(\d+),\s*(" + SequenceForm.re() + r")\}\]\s*"

    @classmethod
    def n(cls):
        """
        Example

        >>> Fermion.n() == Fermion.re().count('(') - Fermion.re().count('(?')
        True
        """
        return 1 + 1 + 1 + 1 + SequenceForm.n()

    @classmethod
    def from_str(cls, fermion: str):
        """
        Example

        >>> str(Fermion.from_str('F[1, {1, SequenceForm[\"Col\", 1]}]'))
        'F[1, {1, SequenceForm["Col", 1]}]'

        >>> str(Fermion.from_str('-F[1, {1, SequenceForm[\"Col\", 1]}]'))
        '-F[1, {1, SequenceForm["Col", 1]}]'
        """
        res = re.search(cls.re(), fermion)
        sign = -1 if res.group(1) == "-F" else 1
        return Fermion(
            sign,
            int(res.group(2)),
            int(res.group(3)),
            SequenceForm.from_str(res.group(4)),
        )
