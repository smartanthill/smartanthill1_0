# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import sys

from twisted.scripts import twistd


def main():
    sys.argv = [sys.argv[0], "--nodaemon", "smartanthill"] + sys.argv[1:]
    twistd.run()


if __name__ == "__main__":
    main()
