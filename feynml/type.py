from typing import List

# from warnings import deprecated
from smpl.doc import deprecated

import cssutils

from feynml import shape, sheet


@deprecated("Use :func:`feynml.sheet.get_default_sheet` instead.")
def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return sheet.get_default_sheet()


@deprecated("Use :func:`feynml.shape.get_shapes` instead.")
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
