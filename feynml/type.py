from typing import List

import cssutils
import smpl_doc.doc as doc

from feynml import shape, sheet


@doc.deprecated("0.1.7", "Use :func:`feynml.sheet.get_default_sheet` instead.")
def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return sheet.get_default_sheet()


@doc.deprecated("0.1.7", "Use :func:`feynml.shape.get_shapes` instead.")
def get_shapes() -> List[str]:
    """Return the default shapes."""
    return shape.get_shapes()


def get_types() -> List[str]:
    """Return the default types."""
    ret = []
    for rule in sheet.get_default_sheet():
        if rule.type == rule.STYLE_RULE and rule.selectorText.startswith("[type="):
            ret += [rule.selectorText.split("=")[1].strip('"]')]
    return sorted(ret)
