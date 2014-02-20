.PHONY: docs

all: docs
	@# do nothing yet

docs:
	$(MAKE) -C docs/ html

pushrtfd:
	curl -X POST http://readthedocs.org/build/smartanthill

inobuild:
	mkdir -p /tmp/{inotmp,inotmp/lib,inotmp/src}
	cp -R smartanthill/embedded/firmware/ /tmp/inotmp/src/
	mv /tmp/inotmp/src/smartanthill.c /tmp/inotmp/src/smartanthill.ino
	#cd /tmp/inotmp/; ino build --verbose
	cd /tmp/inotmp/; ino build

inoupload: inobuild
	cd /tmp/inotmp/; ino upload
