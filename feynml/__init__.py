"""
FeynML is a Python package for creating Feynman diagrams in the FeynML format.
"""

from importlib.metadata import version

package = "feynml"

__version__ = version(package)

from .connector import Connector
from .feynmandiagram import FeynmanDiagram
from .feynml import FeynML
from .head import Head
from .leg import Leg
from .meta import Meta
from .pdgid import PDG
from .point import Point
from .propagator import Propagator
from .styled import Styled
from .vertex import Vertex
