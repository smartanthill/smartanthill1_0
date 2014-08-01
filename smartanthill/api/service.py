# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.python.constants import FlagConstant
from twisted.python.reflect import namedModule

from smartanthill.api.handler import APIHandlerBase
from smartanthill.configprocessor import ConfigProcessor
from smartanthill.exception import APIRequiredParams, APIUnknownRequest
from smartanthill.service import SAMultiService


class APIService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._handlers = []

    def startService(self):
        self.autoload_handlers()

        for _name, _options in self.options.items():
            if not _options.get("enabled", False):
                continue
            path = "smartanthill.api.%s" % _name
            service = namedModule(path).makeService("api.%s" % _name, _options)
            service.setServiceParent(self)

        SAMultiService.startService(self)

    def add_handler(self, handler):
        assert issubclass(handler, APIHandlerBase)
        assert handler not in self._handlers
        self._handlers.append(handler)

    def autoload_handlers(self):
        services = ConfigProcessor().get("services")
        services = sorted(services.items(), key=lambda s: s[1]['priority'])
        for (name, sopt) in services:
            if not sopt.get("enabled", False):
                continue
            try:
                handlers = namedModule(
                    "smartanthill.%s.api" % name).get_handlers()
            except (ImportError, AttributeError):
                continue

            for handler in handlers:
                if handler.KEY and handler.PERMISSION:
                    self.log.info("Auto-loaded '%s:%s' handler" % (
                        handler.PERMISSION.name, handler.KEY))
                    self.add_handler(handler)

    def request(self, action, key, data):
        assert isinstance(action, FlagConstant)
        self.log.info("Received '%s' request with key '%s' and data=%s" %
                      (action.name, key, data))
        params = data.keys()
        for hclass in self._handlers:
            hobj = hclass(action, key)
            if not hobj.match():
                continue
            elif not hobj.check_params(params):
                raise APIRequiredParams(", ".join(hobj.REQUIRED_PARAMS), key)
            return hobj.handle(data)
        raise APIUnknownRequest(action.name, key)


def makeService(name, options):
    return APIService(name, options)
