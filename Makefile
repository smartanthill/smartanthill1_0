.PHONY: all docs clean clean-doc clean-pyc pylint pushrtfd inobuild inoupload debug-demo

all: docs

docs:
	$(MAKE) -C docs/ html

clean: clean-doc clean-pyc

clean-doc:
	rm -R docs/_build

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

pylint:
	@pylint --rcfile ./.pylintrc smartanthill

pushrtfd:
	curl -X POST http://readthedocs.org/build/smartanthill

inobuild:
	mkdir -p /tmp/{inotmp,inotmp/lib,inotmp/src}
	cp -R embedded/firmware/ /tmp/inotmp/src/
	mv /tmp/inotmp/src/smartanthill.c /tmp/inotmp/src/smartanthill.ino
	#cd /tmp/inotmp/; ino build --verbose
	cd /tmp/inotmp/; ino build

inoupload: inobuild
	cd /tmp/inotmp/; ino upload

debug-demo:
	cd examples/blink/data; twistd -n smartanthill --logger.level=DEBUG


