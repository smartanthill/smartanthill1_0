.PHONY: docs

all: docs
	@# do nothing yet

docs:
	$(MAKE) -C docs/ html

pushrtfd:
	curl -X POST http://readthedocs.org/build/smartanthill
