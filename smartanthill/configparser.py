# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import os.path
import sys

from twisted.python.filepath import FilePath

from smartanthill.exception import ConfigKeyError
from smartanthill.util import load_config, merge_nested_dicts, singleton


@singleton
class Config(object):

    def __init__(self, baseconf_path, user_options):
        # parse base conf
        self._config = load_config(baseconf_path)

        self.parse_datadir_conf(user_options['data'])
        self.parse_user_options(user_options)

    def parse_datadir_conf(self, datadir_path):
        dataconf_path = FilePath(os.path.join(datadir_path, "config.json"))
        if not dataconf_path.exists() or not dataconf_path.isfile():
            return
        self._config = merge_nested_dicts(self._config,
                                          load_config(dataconf_path.path))

    def parse_user_options(self, options):
        baseopts = frozenset([v[0] for v in options.optParameters if v[0] !=
                              "data"])
        useropts = frozenset([v.split("=")[0][2:] for v in sys.argv
                              if v[:2] == "--" and "=" in v])
        for k in useropts.intersection(baseopts):
            _dyndict = options[k]
            for p in reversed(k.split('.')):
                _dyndict = {p: _dyndict}
            self._config = merge_nested_dicts(self._config, _dyndict)

    def get(self, key_path, default=None):
        try:
            value = self._config
            for k in key_path.split("."):
                value = value[k]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise ConfigKeyError(key_path)

    def __getitem__(self, key_path):
        return self.get(key_path)

    def __str__(self):
        return str(self._config)
