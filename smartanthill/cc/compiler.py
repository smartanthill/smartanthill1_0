# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from base64 import b64encode
from os import environ
from os.path import getsize, isdir, isfile, join

from platformio.util import get_pioenvs_dir
from twisted.internet import utils
from twisted.internet.defer import Deferred
from twisted.python import log
from twisted.python.util import sibpath

from smartanthill import FIRMWARE_VERSION


class PlatformIOBuilder(object):

    def __init__(self, pioenvs_dir, environment):
        self.pioenvs_dir = pioenvs_dir
        self.env_name = environment

        self._defer = Deferred()
        self._defines = []

        self.append_define("VERSION_MAJOR", FIRMWARE_VERSION[0])
        self.append_define("VERSION_MINOR", FIRMWARE_VERSION[1])

    def get_env_dir(self):
        return join(get_pioenvs_dir(), self.env_name)

    def get_firmware_path(self):
        if not isdir(self.get_env_dir()):
            return None
        for ext in ["bin", "hex"]:
            firm_path = join(self.get_env_dir(), "firmware." + ext)
            if not isfile(firm_path):
                continue
            return firm_path
        return None

    def append_define(self, name, value=None):
        self._defines.append((name, value))

    def run(self):
        newenvs = dict(
            PIOENVS_DIR=self.pioenvs_dir,
            PIOSRCBUILD_FLAGS=self._get_srcbuild_flags()
        )

        output = utils.getProcessOutput(
            "platformio", args=("run", "-e", self.env_name),
            env=environ.update(newenvs),
            path=sibpath(__file__, "embedded")
        )
        output.addCallbacks(self._on_run_callback, self._on_run_errback)
        return self._defer

    def _get_srcbuild_flags(self):
        flags = ""
        for d in self._defines:
            if d[1] is not None:
                flags += "-D%s=%s" % (d[0], d[1])
            else:
                flags += "-D%s" % d[0]
        return flags

    def _on_run_callback(self, result):
        log.msg(result)
        fw_path = self.get_firmware_path()
        if not isfile(fw_path) or "Error" in result:
            return self._defer.errback(Exception(result))

        result = dict(
            version=".".join([str(s) for s in FIRMWARE_VERSION]),
            size=getsize(fw_path),
            type=fw_path[-3:],
            firmware=b64encode(open(fw_path).read())
        )
        self._defer.callback(result)

    def _on_run_errback(self, failure):
        self._defer.errback(failure)
