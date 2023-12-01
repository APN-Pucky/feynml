#####################################################
#                                                   #
#  Source file of the MadFeynML plugin              #
#                                                   #
#              authors: APN-Pucky,                  #
#                                                   #
#                                                   #
#####################################################

import madgraph

import feynml

# from ... import interface as madfeynml_interface
from . import exporter as madfeynml_exporter

##import Resummation.resummation_exporters as resummation_exporters

# Three types of functionality are allowed in a plugin
#   1. new output mode
#   2. new cluster support
#   3. new interface

# 1. Define new output mode
#    example: new_output = {'myformat': MYCLASS}
#    madgraph will then allow the command "output myformat PATH"
#    MYCLASS should inherated of the class madgraph.iolibs.export_v4.VirtualExporter
new_output = {"feynml": madfeynml_exporter.MadFeynMLExporter}
# new_output = None

# 2. Define new way to handle the cluster.
#    example new_cluster = {'mycluster': MYCLUSTERCLASS}
#    allow "set cluster_type mycluster" in madgraph
#    MYCLUSTERCLASS should inherated from madgraph.various.cluster.Cluster
new_cluster = {}

# 3. Define a new interface (allow to add/modify MG5 command)
#    This can be activated via ./bin/mg5_aMC --mode=PLUGINNAME
## Put None if no dedicated command are required
# new_interface = madgraph.interface.master_interface.MasterCmd # madfeynml_interface.MadFeynMLInterface
new_interface = {}


########################## CONTROL VARIABLE ####################################
__author__ = "Alexander Puck Neuwirth"
__email__ = "alexander@neuwirth-informatik.de"
__version__ = feynml.__version__
minimal_mg5amcnlo_version = (3, 5, 0)
maximal_mg5amcnlo_version = (3, 5, 1000)
latest_validated_version = (3, 5, 1)
