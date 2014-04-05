# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# pylint: disable=R0904

from twisted.application.service import MultiService
from twisted.python import usage
from twisted.python.filepath import FilePath
from twisted.python.reflect import namedAny

from smartanthill import __banner__, __version__
from smartanthill.config import Config, get_baseconf
from smartanthill.log import Logger


class SAMultiService(MultiService):

    def __init__(self, name, options=None):
        MultiService.__init__(self)
        self.setName(name)
        self.options = options
        self.log = Logger(self.name)

        self._started = False
        self._onstarted = []

    def startService(self):
        MultiService.startService(self)

        infomsg = "Service has been started"
        if not self.options or isinstance(self.options, usage.Options):
            self.log.info(infomsg)
        else:
            self.log.info(infomsg + " with options '%s'" % self.options)

        self._started = True
        for callback in self._onstarted:
            callback()

    def stopService(self):
        MultiService.stopService(self)
        self.log.info("Service has been stopped.")

    def on_started(self, callback):
        if self._started:
            callback()
        else:
            self._onstarted.append(callback)


class SmartAnthillService(SAMultiService):

    INSTANCE = None

    def __init__(self, name, options):
        SmartAnthillService.INSTANCE = self
        self.datadir = options['datadir']
        self.config = Config(self.datadir, options)
        SAMultiService.__init__(self, name, options)

    @staticmethod
    def instance():
        return SmartAnthillService.INSTANCE

    def startService(self):
        self.log.debug("Initial configuration: %s." % self.config)

        self._preload_subservices(self.config['services'])

        SAMultiService.startService(self)
        self.log.info(__banner__.replace(
            "#data#", self.options['datadir']))

    def _preload_subservices(self, services):
        services = sorted(services.items(), key=lambda s: s[1]['priority'])
        for (name, sopt) in services:
            if "enabled" not in sopt or not sopt['enabled']:
                continue
            path = "smartanthill.%s.service" % name
            service = namedAny(path).makeService(name, sopt['options'])
            service.setServiceParent(self)


class Options(usage.Options):
    optParameters = [["datadir", "d", ".",
                      "The path to working data directory"]]

    compData = usage.Completions(optActions={"datadir": usage.CompleteDirs()})

    longdesc = "SmartAnthill is an intelligent micro-oriented "\
        "networking system (version %s)" % __version__

    allowed_defconf_opts = ("logger.level",)

    def __init__(self):
        self._gather_baseparams(get_baseconf())
        usage.Options.__init__(self)

    def _gather_baseparams(self, baseconf, path=None):
        for k, v in baseconf.iteritems():
            argname = path + "." + k if path else k
            # print argname, v, type(v)
            if isinstance(v, dict):
                self._gather_baseparams(v, argname)
            else:
                if argname not in self.allowed_defconf_opts:
                    continue
                self.optParameters.append([argname, None, v, None, type(v)])

    def postOptions(self):
        if not self['datadir']:
            raise usage.UsageError("Please specify the path(--datadir=)"
                                   " to working directory")
        datadir_path = FilePath(self['datadir'])
        if not datadir_path.exists() or not datadir_path.isdir():
            raise usage.UsageError("The path to the working data directory"
                                   " is invalid")
        elif datadir_path.getPermissions().user.shorthand() != 'rwx':
            raise usage.UsageError("You don't have 'read/write/execute'"
                                   " permissions to working data directory")
        self['datadir'] = datadir_path.path


def makeService(options):
    return SmartAnthillService("sas", options)
