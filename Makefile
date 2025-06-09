livehtml:
	hatch run hatch-test:$(MAKE) -C docs livehtml

html:
	hatch run hatch-test:$(MAKE) -C docs html

pdf:
	hatch run hatch-test:$(MAKE) -C docs latexpdf

doc: html

install:
	hatch env create
	python3 -m pip install --user . --break-system-packages

build:
	hatch build

test:
	rm -f .coverage coverage.xml
	hatch test -c
	coverage xml

commit:
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean:
	rm -r docs/build docs/source/_autosummary
	rm -r .eggs .pytest_cache *.egg-info dist build


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
