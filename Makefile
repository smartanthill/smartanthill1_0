.PHONY: docs

all: docs
	@# do nothing yet

docs:
	$(MAKE) -C docs/ html
