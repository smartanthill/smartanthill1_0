# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import sys
import traceback

from twisted.application.service import Service
from twisted.python import log

from smartanthill.configparser import Config
from smartanthill.exceptions import ConfigKeyError


class Logger(object):

    LEVELS = {
        'FATAL': 0,
        'ERROR': 1,
        'WARN': 2,
        'INFO': 3,
        'DEBUG': 4
    }

    def __init__(self, system="-"):
        self.system = system.name if isinstance(system, Service) else system
        try:
            self._current_level = self.LEVELS[Config()['logger.level']]
        except (ConfigKeyError, KeyError):
            self._current_level = self.LEVELS['INFO']

    def _levelid_to_str(self, id_):
        for k, v in self.LEVELS.iteritems():
            if v == id_:
                return k

    def _msg(self, *msg, **kwargs):
        _system = self.system
        if kwargs['_anthill_loglevel'] > self._current_level:
            return
        elif kwargs['_anthill_loglevel'] != 3:
            _system = "%s.%s" % (
                self._levelid_to_str(kwargs['_anthill_loglevel']).lower(),
                _system)

        params = dict(system=_system)
        params.update(kwargs)
        if kwargs['_anthill_loglevel'] == 0:
            log.err(*msg, **params)
            traceback.print_stack()
        else:
            log.msg(*msg, **params)

    def debug(self, *msg, **kwargs):
        kwargs['_anthill_loglevel'] = self.LEVELS['DEBUG']
        self._msg(*msg, **kwargs)

    def info(self, *msg, **kwargs):
        kwargs['_anthill_loglevel'] = self.LEVELS['INFO']
        self._msg(*msg, **kwargs)

    def warn(self, *msg, **kwargs):
        kwargs['_anthill_loglevel'] = self.LEVELS['WARN']
        self._msg(*msg, **kwargs)

    def error(self, *msg, **kwargs):
        kwargs['_anthill_loglevel'] = self.LEVELS['ERROR']
        self._msg(*msg, **kwargs)

    def fatal(self, *msg, **kwargs):
        kwargs['_anthill_loglevel'] = self.LEVELS['FATAL']
        self._msg(*msg, **kwargs)
        sys.exit()
