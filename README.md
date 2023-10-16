# FeynML

FeynML from <https://feynml.hepforge.org/>

FeynML is a project to develop an XML dialect for describing Feynman diagrams as used in quantum field theory calculations. The primary aim is to unambiguously describe the structure of a diagram in XML, giving a de facto representation for diagram structure which can be easily translated into another representation.

[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/feynml.svg) [![DOI](https://zenodo.org/badge/584503197.svg)](https://zenodo.org/badge/latestdoi/584503197)


[![test][a t image]][a t link]     [![Coverage Status][c t i]][c t l] [![Codacy Badge][cc c i]][cc c l]  [![Codacy Badge][cc q i]][cc q l]  [![Documentation][rtd t i]][rtd t l] [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/APN-Pucky/pyhep-2023/final)

## Installation
```sh
pip install [--user] feynml
```

or from cloned source:

```sh
poerty install --with docs --with dev
poetry shell
```

## Documentation

*   <https://pyfeyn2.readthedocs.io/en/stable/feynml/>
*   <https://apn-pucky.github.io/pyfeyn2/feynml/index.html>

## Related:

*   <https://github.com/APN-Pucky/pyfeyn2>


## Development


### package/python structure:

*   <https://mathspp.com/blog/how-to-create-a-python-package-in-2022>
*   <https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/>


[pypi image]: https://badge.fury.io/py/feynml.svg
[pypi link]: https://pypi.org/project/feynml/
[pypi versions]: https://img.shields.io/pypi/pyversions/feynml.svg

[a t link]: https://github.com/APN-Pucky/feynml/actions/workflows/test.yml
[a t image]: https://github.com/APN-Pucky/feynml/actions/workflows/test.yml/badge.svg


[cc q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44
[cc q l]: https://www.codacy.com/gh/APN-Pucky/feynml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/feynml&amp;utm_campaign=Badge_Grade
[cc c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44
[cc c l]: https://www.codacy.com/gh/APN-Pucky/feynml/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/feynml&utm_campaign=Badge_Coverage

[c t l]: https://coveralls.io/github/APN-Pucky/feynml?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/feynml/badge.svg?branch=master

[rtd t i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=latest
[rtd t l]: https://pyfeyn2.readthedocs.io/en/latest/?badge=latest
