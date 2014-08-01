# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.application.service import ServiceMaker

SmartAnthill = ServiceMaker(
    "smartanthill-cc",
    "smartanthill.cc.service",
    "SmartAnthill Cloud Compiler",
    "smartanthill-cc")
