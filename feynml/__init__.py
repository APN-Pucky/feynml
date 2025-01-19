"""
FeynML is a Python package for creating Feynman diagrams in the FeynML format.
"""

from importlib.metadata import version
from .connector import Connector as Connector
from .feynmandiagram import FeynmanDiagram as FeynmanDiagram
from .feynml import FeynML as FeynML
from .head import Head as Head
from .leg import Leg as Leg
from .meta import Meta as Meta
from .momentum import Momentum as Momentum
from .pdgid import PDG as PDG
from .point import Point as Point
from .propagator import Propagator as Propagator
from .styled import Styled as Styled
from .vertex import Vertex as Vertex

package = "feynml"

__version__ = version(package)
