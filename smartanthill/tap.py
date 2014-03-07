# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.application.service import MultiService
from twisted.python import usage
from twisted.python.filepath import FilePath
from twisted.python.util import sibpath

from smartanthill import __banner__, __version__
from smartanthill.configparser import Config
from smartanthill.log import Logger
from smartanthill.util import load_config, load_service

BASECONF_PATH = sibpath(__file__, "config_base.json")


class SmartAnthillService(MultiService):

    def __init__(self, user_options):
        MultiService.__init__(self)
        self.setName("sas")
        self.datadir = user_options['data']
        self.config = Config(BASECONF_PATH, user_options)
        self.log = Logger(self)

    def startService(self):
        self.log.debug("Initial configuration: %s." % self.config)

        self.start_sas_services(self.config['services'])

        MultiService.startService(self)
        self.log.info("SmartAnthill %s (%s) starting up." % (__version__,
                                                             self.datadir))

        # self.litemq.produce("network", "client->control",
        #                     {"cdc": 0x8C, "source": 0, "destination": 128,
        #                      "data": [13,1], "ack": True})

    def start_sas_services(self, services):
        for k, v in services.iteritems():
            if not v['enabled']:
                continue
            setattr(self, k, load_service(self, k, v['options']))
            self.addService(getattr(self, k))


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
    print __banner__

    return SmartAnthillService(options)
