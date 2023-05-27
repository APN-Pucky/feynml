from typing import List

from feynml import sheet


def get_shapes() -> List[str]:
    """Return the default shapes."""
    ret = []
    for rule in sheet.get_default_sheet():
        if rule.type == rule.STYLE_RULE and rule.selectorText.startswith("[shape="):
            ret += [rule.selectorText.split("=")[1].strip('"]')]
    return sorted(ret)
