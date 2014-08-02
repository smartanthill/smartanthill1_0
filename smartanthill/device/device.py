# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# from twisted.internet.defer import inlineCallbacks
import re
from base64 import b64decode
from os import environ, makedirs
from os.path import dirname, isdir, join
from shutil import copyfile, rmtree
from tempfile import mkdtemp

from twisted.internet import utils
from twisted.python.constants import ValueConstant
from twisted.python.failure import Failure
from twisted.python.util import sibpath

from smartanthill.device.board.base import BoardFactory
from smartanthill.device.operation.base import OperationType
from smartanthill.exception import DeviceUnknownOperation
from smartanthill.log import Logger


class Device(object):

    def __init__(self, id_, options):
        self.log = Logger("device.%d" % id_)
        self.id_ = id_
        self.options = options
        self.board = BoardFactory.newBoard(options['boardId'])
        self.operations = set([OperationType.PING,
                               OperationType.LIST_OPERATIONS])

        if "operationIds" in options:
            for cdc in options['operationIds']:
                self.operations.add(OperationType.lookupByValue(cdc))

        self.log.info("Allowed operations: %s" % ([o.name for o in
                                                   self.operations]))

    def get_name(self):
        return self.options.get(
            "name", "Device #%d, %s" % (self.id_, self.board.get_name()))

    # @inlineCallbacks
    # def verify_operations(self):
    #     result = yield self.launch_operation(OperationType.LIST_OPERATIONS)
    #     for cdc in result:
    #         self.operations.add(OperationType.lookupByValue(cdc))
    #     self.operations = frozenset(self.operations)

    def launch_operation(self, type_, data=None):
        assert isinstance(type_, ValueConstant)
        if type_ in self.operations:
            return self.board.launch_operation(self.id_, type_, data)
        raise DeviceUnknownOperation(type_.name, self.id_)

    def upload_firmware(self, firmware):
        tmp_dir = mkdtemp()
        platformioini_path = sibpath(
            dirname(__file__),
            join("cc", "embedded", "platformio.ini")
        )

        # show Alias: uploader

        # prepare temporary PlatformIO project
        pioenv_dir = join(tmp_dir, ".pioenvs", self.board.get_id())
        if not isdir(pioenv_dir):
            makedirs(pioenv_dir)
        copyfile(platformioini_path, join(tmp_dir, "platformio.ini"))
        with open(join(pioenv_dir, "firmware.%s" % firmware['type']),
                  "w") as f:
            f.write(b64decode(firmware['firmware']))

        defer = utils.getProcessOutput(
            "platformio",
            args=("run", "-e", self.board.get_id(), "-t", "uploadlazy",
                  "--upload-port", firmware['serialport']),
            env=environ,
            path=tmp_dir
        )
        defer.addBoth(self._on_uploadfw_output, tmp_dir)
        return defer

    def _on_uploadfw_output(self, result, tmp_dir):
        self.log.debug(result)
        rmtree(tmp_dir)
        if isinstance(result, Failure):
            return result

        match = re.search(
            r"(Done, (\d+) bytes total|(\d+) bytes of flash written)",
            result
        )
        if match:
            return {
                "result": "%s bytes of flash has been written" % match.group(2)
            }
        raise Exception(result)
