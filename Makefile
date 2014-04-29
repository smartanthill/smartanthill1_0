.PHONY: all docs clean-doc clean-py pushrtfd inobuild inoupload debug-demo test clean

all: docs

docs:
	$(MAKE) -C docs/ html

clean-doc:
	rm -R docs/_build

clean-py:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	rm twisted/plugins/dropin.cache

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

test:
	tox -e docs,lint
	trial --temp-directory=/tmp/_trial_temp smartanthill

clean: clean-doc clean-py
