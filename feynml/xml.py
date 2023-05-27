from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


class XML:
    def to_xml(self) -> str:
        """Return self as XML."""
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(self)

    @classmethod
    def from_xml(cls, xml: str):
        """Load self from XML."""
        parser = XmlParser()
        return parser.from_string(xml, cls)
