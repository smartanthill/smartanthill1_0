.PHONY: all docs clean-doc clean-py pushrtfd buildfw debug-demo test clean

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

buildfw:
	cd embedded/firmware; platformio run

debug-demo:
	smartanthill --datadir=examples/blink/data --logger.level=DEBUG

test:
	tox

clean: clean-doc clean-py
