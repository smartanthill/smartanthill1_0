# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

import os.path
import sys

from twisted.python.filepath import FilePath
from twisted.python.util import sibpath

from smartanthill.exception import ConfigKeyError
from smartanthill.util import load_config, merge_nested_dicts, singleton


def get_baseconf():
    return load_config(sibpath(__file__, "config_base.json"))


@singleton
class ConfigProcessor(dict):

    def __init__(self, datadir, user_options):
        self._data = get_baseconf()
        self.process_datadir_conf(datadir)
        self.process_user_options(user_options)

        dict.__init__(self, self._data)

    def process_datadir_conf(self, datadir_path):
        dataconf_path = FilePath(os.path.join(datadir_path, "config.json"))
        if not dataconf_path.exists() or not dataconf_path.isfile():
            return
        self._data = merge_nested_dicts(self._data,
                                        load_config(dataconf_path.path))

    def process_user_options(self, options):
        useropts = frozenset([v.split("=")[0][2:] for v in sys.argv
                              if v[:2] == "--" and "=" in v])
        for k in useropts.intersection(frozenset(options)):
            _dyndict = options[k]
            for p in reversed(k.split('.')):
                _dyndict = {p: _dyndict}
            self._data = merge_nested_dicts(self._data, _dyndict)

    def get(self, key_path, default=None):
        try:
            value = self
            for k in key_path.split("."):
                value = value[k]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise ConfigKeyError(key_path)
