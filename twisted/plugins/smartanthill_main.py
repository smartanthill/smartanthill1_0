# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.application.service import ServiceMaker

SmartAnthill = ServiceMaker(
    "smartanthill",
    "smartanthill.service",
    "An intelligent micro-oriented networking system",
    "smartanthill")
