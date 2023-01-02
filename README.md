# PyFeyn2

Forked from <https://pyfeyn.hepforge.org/> 

FeynML from <https://feynml.hepforge.org/>

PyFeyn is a Python-language based system for drawing Feynman diagrams. It was inspired by the C++ FeynDiagram system, and aims to provide the same functionality and quality of output as that, with the added benefits of a modern interpreted language, an improved interface and output direct to both EPS and PDF. Behind the scenes, PyFeyn uses the excellent PyX system - you can use PyX constructs in PyFeyn diagrams if you want, too.

[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/smpl.svg)

| [Stable][doc stable]        | [Test][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]   | [![test][a t image]][a t link]     |
| [![Coverage Status][c s i]][c s l]   | [![Coverage Status][c t i]][c t l] |
| [![Codacy Badge][cc s c i]][cc s c l] | [![Codacy Badge][cc c i]][cc c l]  |
| [![Codacy Badge][cc s q i]][cc s q l] | [![Codacy Badge][cc q i]][cc q l]  |
| [![Documentation][rtd s i]][rtd s l] | [![Documentation][rtd t i]][rtd t l]|

## Dependencies

*   libmagickwand-dev (to display pdfs in a jupyter-notebook, might require a policy change of the imagemagick config for PDFs, see Troubleshooting)
*   ghostscript
*   latexmk
*   (feynmp-auto/feynmf)

## Installation

```sh
poerty install --with docs --with dev
poetry shell
```

## Documentation

*   <https://pyfeyn2.readthedocs.io/en/stable/>
*   <https://apn-pucky.github.io/pyfeyn2/index.html>

## Similar Feynman diagram rendering project:

*   <https://github.com/ndeutschmann/qgraf-xml-drawer>
*   <https://github.com/GkAntonius/feynman>
*   <https://github.com/JP-Ellis/tikz-feynman>
*   <https://pyfeyn.hepforge.org/> 
*   <https://feynml.hepforge.org/>
*   <http://www.feyndiagram.com/>

Several of these are integrated into pyfeyn2.

## Troubleshooting

*   [ImageMagick security policy 'PDF' blocking conversion]( https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion )

## Development


### package/python structure:

*   <https://mathspp.com/blog/how-to-create-a-python-package-in-2022>
*   <https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/>

[doc stable]: https://apn-pucky.github.io/pyfeyn2/index.html
[doc test]: https://apn-pucky.github.io/pyfeyn2/test/index.html

[pypi image]: https://badge.fury.io/py/pyfeyn2.svg
[pypi link]: https://pypi.org/project/pyfeyn2/
[pypi versions]: https://img.shields.io/pypi/pyversions/pyfeyn2.svg

[a s image]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/stable.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/stable.yml
[a t link]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml
[a t image]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml/badge.svg

[cc s q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44?branch=stable
[cc s q l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/pyfeyn2&amp;utm_campaign=Badge_Grade?branch=stable
[cc s c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44?branch=stable
[cc s c l]: https://www.codacy.com/gh/APN-Pucky/smpl/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/pyfeyn2&utm_campaign=Badge_Coverage?branch=stable

[cc q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44
[cc q l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/pyfeyn2&amp;utm_campaign=Badge_Grade
[cc c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44
[cc c l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/pyfeyn2&utm_campaign=Badge_Coverage

[c s i]: https://coveralls.io/repos/github/APN-Pucky/pyfeyn2/badge.svg?branch=stable
[c s l]: https://coveralls.io/github/APN-Pucky/pyfeyn2?branch=stable
[c t l]: https://coveralls.io/github/APN-Pucky/pyfeyn2?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/pyfeyn2/badge.svg?branch=master

[rtd s i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=stable
[rtd s l]: https://pyfeyn2.readthedocs.io/en/stable/?badge=stable
[rtd t i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=latest
[rtd t l]: https://pyfeyn2.readthedocs.io/en/latest/?badge=latest
