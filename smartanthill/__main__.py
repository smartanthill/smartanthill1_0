# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import sys

from twisted.scripts import twistd


def main():
    sys.argv[1:1] = ["--nodaemon", "smartanthill"]
    twistd.run()


if __name__ == "__main__":
    sys.exit(main())
