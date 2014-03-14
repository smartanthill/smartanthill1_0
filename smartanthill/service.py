# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.application.service import MultiService
from twisted.python import usage
from twisted.python.filepath import FilePath
from twisted.python.reflect import namedAny
from twisted.python.util import sibpath

from smartanthill import __banner__, __version__
from smartanthill.configparser import Config
from smartanthill.log import Logger
from smartanthill.util import load_config

BASECONF_PATH = sibpath(__file__, "config_base.json")


class SAMultiService(MultiService):

    def __init__(self, name, options=None):
        MultiService.__init__(self)
        self.setName(name)
        self.log = Logger(name)
        self.options = options

    def startService(self):
        MultiService.startService(self)
        if self.name != "sas":
            self.log.info("Service has been started with options '%s'" %
                          self.options)

    def stopService(self):
        MultiService.stopService(self)
        self.log.info("Service has been stopped.")


class SmartAnthillService(SAMultiService):

    INSTANCE = None

    def __init__(self, name, options):
        self.config = Config(BASECONF_PATH, options)
        SAMultiService.__init__(self, name, options)
        SmartAnthillService.INSTANCE = self
        self.datadir = options['data']

    @staticmethod
    def instance():
        return SmartAnthillService.INSTANCE

    def startService(self):
        self.log.info(__banner__)
        self.log.debug("Initial configuration: %s." % self.config)

        self.preload_subservices(self.config['services'])

        SAMultiService.startService(self)
        self.log.info("SmartAnthill %s (%s) starting up." % (__version__,
                                                             self.datadir))
        r = self.getServiceNamed("device").get_device(128).launch_operation(
            "readanalogpin", "A0")
        r.addCallback(lambda r: self.log.info(r))

    def preload_subservices(self, services):
        services = sorted(services.items(), key=lambda s: s[1]['priority'])
        for (name, sopt) in services:
            if not sopt['enabled']:
                continue

            path = "smartanthill.%s.service" % name
            service = namedAny(path).makeService(name, sopt['options'])
            service.setServiceParent(self)


class Options(usage.Options):
    optParameters = [["data", "d", None, "The path to working data directory"]]

    compData = usage.Completions(optActions={"data": usage.CompleteDirs()})

    longdesc = "SmartAnthill System is an intelligent micro-oriented "\
        "networking system (version %s)" % __version__

    skip_defconf_opts = ('services',)

    def __init__(self):
        self._gather_baseparams(load_config(BASECONF_PATH))
        usage.Options.__init__(self)

    def _gather_baseparams(self, baseconf, path=None):
        for k, v in baseconf.iteritems():
            argname = path + '.' + k if path else k
            # print argname, v, type(v)
            if isinstance(v, dict):
                self._gather_baseparams(v, argname)
            else:
                if k in self.skip_defconf_opts:
                    continue
                self.optParameters.append([argname, None, v, None, type(v)])

    def postOptions(self):
        if not self['data']:
            raise usage.UsageError("Please specify the path(--data=)"
                                   " to working directory")
        data_path = FilePath(self['data'])
        if not data_path.exists() or not data_path.isdir():
            raise usage.UsageError("The path to the working data directory"
                                   " is invalid")
        elif data_path.getPermissions().user.shorthand() != 'rwx':
            raise usage.UsageError("You don't have 'read/write/execute'"
                                   " permissions to working data directory")


def makeService(options):
    return SmartAnthillService("sas", options)
