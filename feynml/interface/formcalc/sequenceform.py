import re
from dataclasses import dataclass


@dataclass
class SequenceForm:
    s: str
    i: int

    def __str__(self):
        return f'SequenceForm["{self.s}", {self.i}]'

    @classmethod
    def re(cls):
        return r"\s*SequenceForm\[\"(\w+)\",\s*(\d+)\]\s*"

    @classmethod
    def n(cls):
        return 1 + 1

    @classmethod
    def from_str(cls, sequenceform: str):
        """
        Example

        >>> str(SequenceForm.from_str('SequenceForm[\"Col\", 1]'))
        'SequenceForm["Col", 1]'
        """
        res = re.search(cls.re(), sequenceform)
        return SequenceForm(res.group(1), int(res.group(2)))
