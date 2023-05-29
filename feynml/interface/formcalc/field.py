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
    def re():
        return r"\s*Field\[(\d+)\]\s*"

    @classmethod
    def n():
        return 1

    @classmethod
    def from_str(cls, field: str):
        """
        Example

        >>> Field.from_str("Field[1]")
        Field(1)
        """
        res = re.search(cls.re(), field)
        return Field(int(res.group(1)))
