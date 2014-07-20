.PHONY: all docs clean-doc clean-py pushrtfd buildfw debug-demo debug-dashboard build-dashboard test clean

all: docs

docs:
	$(MAKE) -C docs/ html

clean-doc:
	rm -R docs/_build

clean-py:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	rm twisted/plugins/dropin.cache

clean-dashboard:
	cd smartanthill/dashboard/site; grunt clean 

pushrtfd:
	curl -X POST http://readthedocs.org/build/smartanthill

build-firmware:
	cd embedded/firmware; platformio run -t upload

debug-demo:
	smartanthill --workspacedir=examples/arduino-router/workspace --logger.level=DEBUG

debug-dashboard:
	cd smartanthill/dashboard/site; grunt serve

build-dashboard:
	cd smartanthill/dashboard/site; grunt build

test:
	tox
	cd smartanthill/dashboard/site; grunt test

clean: clean-doc clean-py clean-dashboard
