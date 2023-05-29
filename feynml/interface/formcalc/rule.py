import re
from dataclasses import dataclass
from typing import Union

from feynml.interface.formcalc.fermion import Fermion
from feynml.interface.formcalc.field import Field
from feynml.interface.formcalc.particle import Particle
from feynml.interface.formcalc.vector import Vector


@dataclass
class Rule:
    lhs: Field
    rhs: Union[Particle, str]

    def __str__(self):
        return f"{self.lhs} -> {self.rhs}"

    @classmethod
    def re(cls):
        return (
            r"\s*("
            + Field.re()
            + r")\s*->\s*"
            + r"(("
            + Vector.re()
            + r")|("
            + Fermion.re()
            + r")|F(?!\[))\s*"
        )

    @classmethod
    def n(cls):
        """
        Example

        >>> Rule.n() == Rule.re().count('(') - Rule.re().count('(?')
        True
        """
        return 1 + Field.n() + 1 + (1 + Vector.n() + 1 + Fermion.n())

    @classmethod
    def from_str(cls, rule: str):
        """
        Example

        >>> str(Rule.from_str("Field[1] -> V[1]"))
        'Field[1] -> V[1]'

        >>> str(Rule.from_str('Field[1] -> F[1, {1, SequenceForm["Col", 1]}]'))
        'Field[1] -> F[1, {1, SequenceForm["Col", 1]}]'

        >>> str(Rule.from_str('Field[4] -> V[5, {SequenceForm["Glu", 4]}]'))
        'Field[4] -> V[5, {SequenceForm["Glu", 4]}]'
        """
        res = re.search(cls.re(), rule)
        lhs = Field.from_str(res.group(1))
        rhs = res.group(Field.n() + 2)
        if res.group(Field.n() + 3) is not None:
            rhs = Vector.from_str(rhs)
        elif res.group(Field.n() + Vector.n() + 4) is not None:
            rhs = Fermion.from_str(rhs)
        else:
            rhs = str(rhs)
        return Rule(lhs, rhs)
