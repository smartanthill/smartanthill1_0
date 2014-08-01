# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from os.path import join

from twisted.application.internet import TCPServer  # pylint: disable=E0611
from twisted.python.log import NullFile
from twisted.python.util import sibpath
from twisted.web import server, static

from smartanthill.dashboard.api import REST
from smartanthill.log import Logger
from smartanthill.service import SAMultiService


class DashboardSite(server.Site):

    def _openLogFile(self, path):
        log = Logger("dashboard.http")

        def wrapper(msg):
            log.debug(msg.strip())

        nf = NullFile()
        nf.write = wrapper
        return nf


class DashboardService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)

    def startService(self):
        root = static.File(sibpath(__file__, join("site", "dist")))
        root.putChild("api", REST())
        TCPServer(
            self.options['port'],
            DashboardSite(root, logPath="/dev/null")).setServiceParent(self)

        SAMultiService.startService(self)


def makeService(name, options):
    return DashboardService(name, options)
