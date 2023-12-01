#####################################################
#                                                   #
#  Source file of the Matrix Elements exports for   #
#  the MadFeynML MG5aMC plugin.                         #
#                                                   #
#####################################################

import copy
import itertools
import logging
import os
import re
import shutil
import subprocess
from collections import defaultdict
from math import fmod

import madgraph.core.color_algebra as color
import madgraph.core.helas_objects as helas_objects
import madgraph.iolibs.drawing_eps as draw
import madgraph.iolibs.file_writers as writers
import madgraph.iolibs.files as files
import madgraph.iolibs.group_subprocs as group_subprocs
import madgraph.iolibs.helas_call_writers as helas_call_writers
import madgraph.iolibs.template_files as Template
import madgraph.iolibs.ufo_expression_parsers as parsers

from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML
from feynml.head import Head
from feynml.leg import Leg
from feynml.meta import Meta
from feynml.propagator import Propagator
from feynml.vertex import Vertex

plugin_path = os.path.dirname(os.path.realpath(__file__))

import madgraph.iolibs.export_fks as export_fks
from madgraph import MG5DIR, InvalidCmd, MadGraph5Error
from madgraph.core.drawing import DiagramDrawer, DrawOption
from madgraph.iolibs.export_v4 import ProcessExporterFortran

logger = logging.getLogger("MadFeynML_plugin.MEExporter")

pjoin = os.path.join


class MadFeynMLExporterError(MadGraph5Error):
    """Error from the Resummation MEs exporter."""


class MadFeynMLExporter(ProcessExporterFortran, DiagramDrawer):

    ## check status of the directory. Remove it if already exists
    # check = True
    ## Language type: 'v4' for f77 'cpp' for C++ output
    # exporter = 'v4'
    ## Output type:
    ##[Template/dir/None] copy the Template, just create dir  or do nothing
    # output = 'Template'
    ## Decide which type of merging if used [madevent/madweight]
    # grouped_mode = False
    ## if no grouping on can decide to merge uu~ and u~u anyway:
    # sa_symmetry = False

    ##template_path = pjoin(plugin_path,'MadFeynMLTemplate')

    def __init__(self, *args, **opts):
        """Possibly define extra instance attribute for this daughter class."""
        print("Initializing MadFeynMLExporter...")
        print("args: " + str(args))
        print("opts: " + str(opts))

        oo = args[1]["output_options"]

        if "draw" in oo and oo["draw"]:
            self.draw = True
        else:
            self.draw = False

        return super(MadFeynMLExporter, self).__init__(*args, **opts)

    def generate_subprocess_directory(self, matrix_elements, helicity_model, me=None):
        """Additional actions needed for setup of Template"""
        super(MadFeynMLExporter, self).generate_subprocess_directory(
            matrix_elements, helicity_model, me
        )

        print("Drawing Feynman Diagrams...")

        if isinstance(matrix_elements, helas_objects.HelasMultiProcess):
            self.matrix_elements = matrix_elements.get("matrix_elements")
        elif isinstance(matrix_elements, group_subprocs.SubProcessGroup):
            self.config_maps = matrix_elements.get("diagram_maps")
            self.matrix_elements = matrix_elements.get("matrix_elements")
        elif isinstance(matrix_elements, helas_objects.HelasMatrixElementList):
            self.matrix_elements = matrix_elements
        elif isinstance(matrix_elements, helas_objects.HelasMatrixElement):
            self.matrix_elements = helas_objects.HelasMatrixElementList(
                [matrix_elements]
            )
        if not self.matrix_elements:
            raise MadGraph5Error("No matrix elements to export")

        # print("matrix_elements: " + self.matrix_elements)
        dirpath = pjoin(
            self.dir_path,
            "SubProcesses",
            "P%s" % self.matrix_elements[0].get("processes")[0].shell_string(),
        )
        try:
            os.mkdir(dirpath)
        except os.error as error:
            logger.warning(error.strerror + " " + dirpath)
        fml = self.diagrams_to_feynml(self.matrix_elements)
        f = pjoin(dirpath, "madgraph.fml")
        os.chdir(dirpath)
        print("#matrix_elements: " + str(len(self.matrix_elements)))
        print("Writing FeynML to " + f)
        with open(f, "w") as file:
            file.write(fml.to_xml())

        if self.draw:
            print("Drawing FeynML")
            for i, d in enumerate(fml.diagrams):
                d.render(
                    file=f.replace(".fml", f"{i}"),
                    render="tikz",
                    auto_position_legs=False,
                )

        return 0
        super(MadFeynMLExporter, self).draw_feynman_diagrms(matrix_element)

    def diagrams_to_feynml(self, matrix_elements: helas_objects.HelasMatrixElementList):
        fds = []
        for ime, matrix_element in enumerate(matrix_elements):
            for d in matrix_element.get("base_amplitude").get("diagrams"):
                fds += [
                    self.diagram_to_feynman(
                        d, model=matrix_element.get("processes")[0].get("model")
                    )
                ]
        fml = FeynML(
            diagrams=fds,
            head=Head(
                metas=[
                    Meta(name="renderer", content="tikz"),
                    Meta(name="creator", content="pyfeyn2"),
                    Meta(name="tool", content="pyfeyn2.interface.madgraph.plugin"),
                    Meta(name="description", content="Generated by MadGraph5"),
                    Meta(name="title", content="MadFeynML Feynman Diagrams"),
                ]
            ),
        )
        print(fml)
        return fml

    def diagram_to_feynman(self, diagram, model=None) -> FeynmanDiagram:
        print(repr(diagram))
        print("diagram: " + str(diagram))
        print("verices: " + str(diagram["vertices"]))
        print("orders: " + str(diagram["orders"]))
        diag = self.convert_diagram(
            diagram, model, amplitude=True, opt=DrawOption()
        )  # TODO check amplitude = True
        print(*diag.vertexList)
        print(*diag.lineList)
        fd = FeynmanDiagram()

        def v_to_id(v):
            # check if has attr lines
            if hasattr(v, "lines"):
                return "v" + "v".join(["v" + str(l.number) for l in v.lines])
            else:
                return "v" + "v".join(
                    ["v" + str(l.get("number")) for l in v.get("legs")]
                )

        # add Vertices
        vids = []
        for i, v in enumerate(diagram["vertices"]):
            print(v)
            vid = v_to_id(v)
            fd.add(Vertex(vid))
            vids += [vid]
        # incoming = {}
        # conns = defaultdict(lambda : [])
        # for v in diagram['vertices']:
        #    for l in v['legs']:
        #        if l['state'] == False:
        #            incoming += (l['id'], v)
        #        else:
        #            conns[l['id'] + "_" + l['number']] += [(v , l['id'])]

        # for i in incoming:
        #    fd.add(Leg("l"+str(i),pdgid=i, target="v"+str([i]['id']), sense="incoming"))

        for line in diag.lineList:
            print(line)
            id = line.id
            endid = v_to_id(line.end)
            beginid = v_to_id(line.begin)
            if model.get_particle(abs(id)).get("self_antipart"):
                id = abs(id)
            if not endid in vids:
                o = Leg(
                    id="l" + str(line.number),
                    external=str(line.number),
                    pdgid=id,
                    target=str(beginid),
                    sense="outgoing" if line.state else "incoming",
                    x=line.end.pos_x * 10,
                    y=line.end.pos_y * 10,
                )
            elif beginid not in vids:
                o = Leg(
                    id="l" + str(line.number),
                    external=str(line.number),
                    pdgid=id,
                    target=str(endid),
                    sense="outgoing" if line.state else "incoming",
                    x=line.begin.pos_x * 10,
                    y=line.begin.pos_y * 10,
                )
            else:
                # propagator
                o = Propagator(
                    id="p" + str(line.number),
                    pdgid=id,
                    source=str(beginid),
                    target=str(endid),
                )
            fd.add(o)
            # pprint(vars(l))
            print(o)
            # print(str(l.begin))
            # print(str(l.end))
            # pprint(vars(l))
            # print(str(l.begin))
            # print(str(l.end))

        return fd
