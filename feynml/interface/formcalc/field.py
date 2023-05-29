import re
from dataclasses import dataclass


@dataclass
class Field:
    i: int

    def __str__(self):
        """
        Example

        >>> Field.from_str(str(Field(1))) == Field(1)
        True
        """
        return f"Field[{self.i}]"

    @classmethod
    def re(cls):
        return r"\s*Field\[(\d+)\]\s*"

    @classmethod
    def n(cls):
        return 1

    @classmethod
    def from_str(cls, field: str):
        """
        Example

        >>> str(Field.from_str("Field[1]"))
        'Field[1]'
        """
        res = re.search(Field.re(), field)
        return Field(int(res.group(1)))
