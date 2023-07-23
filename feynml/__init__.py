"""
FeynML is a Python package for creating Feynman diagrams in the FeynML format.
"""

from importlib.metadata import version

package = "feynml"

__version__ = version(package)

from .feynmandiagram import FeynmanDiagram
from .leg import Leg
from .pdgid import PDG
from .propagator import Propagator
from .vertex import Vertex
