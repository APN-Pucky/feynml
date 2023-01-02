import logging
from typing import List

import cssutils

cssutils.log.setLevel(logging.CRITICAL)

default_sheet = cssutils.parseString(
    """
        /*************************************************************************/ 
        /* Diagram */
        /*************************************************************************/

        diagram {
            direction: right;
            layout : neato;
        }

        /*************************************************************************/ 
        /* Vertex */
        /*************************************************************************/

        [shape=dot] {
            symbol : dot;
        }
        [shape=empty] {
            symbol : empty;
        }
        [shape=square] {
            symbol : square;
        }
        [shape=cross] {
            symbol : cross;
        }
        [shape=blob] {
            symbol : blob;
        }

        /*************************************************************************/
        /* Propagator */
        /*************************************************************************/

        /* General */
        [type=fermion] {
            line: fermion;
            arrow-sense: 1;
        }
        [type="anti fermion"] {
            line: anti fermion;
            arrow-sense: -1;
        }
        [type=boson] {
            line: boson;
            arrow-sense: 0;
        }
        [type=vector] {
            line: vector;
            arrow-sense: 0;
        }
        [type=scalar] {
            line: scalar;
            arrow-sense: 0;
        }
        [type=majorana] {
            line: majorana;
        }
        [type=anti majorana] {
            line: anti majorana;
        }
        /* SM */
        [type=photon] {
            line: photon;
            arrow-sense: 0;
        }
        [type=higgs] {
            line: higgs;
            arrow-sense: 0;
        }
        [type=gluon] {
            line: gluon;
            arrow-sense: 0;
            xamp : 0.025;
            yamp : 0.035;
            nloops : 7;
        }
        [type=ghost] {
            line: ghost;
            arrow-sense: 0;
        }
        /* BSM */
        [type=graviton] {
            line: graviton;
            arrow-sense: 0;
        }
        [type=gluino] {
            line: gluino;
            arrow-sense: 0;
            xamp : 0.025;
            yamp : 0.035;
            nloops : 7;
        }
        [type=squark]  {
            line: squark;
            arrow-sense: 1;
        }
        [type=slepton] {
            line: slepton;
            arrow-sense: 1;
        }
        [type=anti squark]  {
            line: anti squark;
            arrow-sense: -1;
        }
        [type=anti slepton] {
            line: anti slepton;
            arrow-sense: -1;
        }
        [type=gaugino] {
            line: gaugino;
            arrow-sense: 0;
        }
        [type=neutralino] {
            line: neutralino;
            arrow-sense: 0;
        }
        [type=chargino] {
            line: chargino;
            arrow-sense: 0;
        }
        [type=higgsino] {
            line: higgsino;
            arrow-sense: 0;
        }
        [type=gravitino] {
            line: gravitino;
            arrow-sense: 0;
        }
        /* util */
        [type=phantom] {
            line: phantom;
            arrow-sense: 0;
        }
        [type=line] {
            line: line;
            arrow-sense: 0;
        }
        """
)


def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return default_sheet


def get_types() -> List[str]:
    """Return the default types."""
    ret = []
    for rule in default_sheet:
        if rule.type == rule.STYLE_RULE and rule.selectorText.startswith("[type="):
            ret += [rule.selectorText.split("=")[1].strip('"]')]
    return sorted(ret)


def get_shapes() -> List[str]:
    """Return the default shapes."""
    ret = []
    for rule in default_sheet:
        if rule.type == rule.STYLE_RULE and rule.selectorText.startswith("[shape="):
            ret += [rule.selectorText.split("=")[1].strip('"]')]
    return sorted(ret)
