from pprint import pprint

import cssutils

css = """
body, html { color: blue }
h1, h2 { font-size: 1.5em; color: red}
h3, h4, h5 { font-size: small; }
"""

dct = {}
sheet = cssutils.parseString(css)

for rule in sheet:
    selector = rule.selectorText
    styles = rule.style.cssText
    dct[selector] = styles


pprint(dct)
